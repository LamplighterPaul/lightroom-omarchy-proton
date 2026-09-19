#!/usr/bin/env python3
"""Assemble the full pinned GE stack with source-built Lightroom components.

This is a component rebuild, not a claim that every GE dependency was rebuilt.
The resulting runtime is launched through UMU and Steam Linux Runtime.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / 'omarchy/upstream.json').read_text())

def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive', type=Path, required=True)
parser.add_argument('--build', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
if sha(args.archive) != PIN['sha256']:
    raise SystemExit('Upstream archive checksum mismatch')
if args.output.exists():
    raise SystemExit('Output already exists; choose a new candidate directory')
components = {}
for module in ('advapi32', 'shcore', 'd2d1', 'hnetcfg', 'uiautomationcore'):
    for arch in ('x86_64-windows', 'i386-windows'):
        components[f'files/lib/wine/{arch}/{module}.dll'] = args.build / f'dlls/{module}/{arch}/{module}.dll'
components['files/lib/wine/x86_64-unix/win32u.so'] = args.build / 'dlls/win32u/win32u.so'
for source in components.values():
    if not source.is_file():
        raise SystemExit(f'Missing build output: {source}')
args.output.parent.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='.lightroom-proton-', dir=args.output.parent) as temp:
    with tarfile.open(args.archive) as archive:
        archive.extractall(temp, filter='data')
    candidate = Path(temp) / PIN['archive'].removesuffix('.tar.gz')
    for target, source in components.items():
        shutil.copy2(source, candidate / target)
    provenance = {**PIN, 'build_kind': 'GE binary distribution with source-rebuilt Wine components',
                  'components': {target: sha(source) for target, source in components.items()},
                  'patch_sha256': {name: sha(ROOT / 'omarchy/patches' / name) for name in PIN['patches']},
                  'experimental_colour_passthrough': True}
    (candidate / 'lightroom-omarchy-proton.json').write_text(json.dumps(provenance, indent=2) + '\n')
    (candidate / 'version').write_text(f"{int(time.time())} {PIN['name']}-{PIN['version']}\n")
    manifest = candidate / 'compatibilitytool.vdf'
    manifest.write_text(manifest.read_text().replace(PIN['archive'].removesuffix('.tar.gz'), PIN['name']))
    shutil.copytree(ROOT / 'omarchy', candidate / 'lightroom-source', ignore=shutil.ignore_patterns('__pycache__'))
    candidate.rename(args.output)
print(f'Assembled {args.output}; prefix and desktop entry unchanged.')
