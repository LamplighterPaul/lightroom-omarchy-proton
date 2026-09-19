#!/usr/bin/env python3
"""Report new GE releases without changing the installed Lightroom runtime."""
import json
import argparse
from pathlib import Path
import urllib.request

pin = json.loads(Path(__file__).with_name('upstream.json').read_text())
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
request = urllib.request.Request(
    f"https://api.github.com/repos/{pin['repository']}/releases/latest",
    headers={'Accept': 'application/vnd.github+json', 'User-Agent': pin['name']})
with urllib.request.urlopen(request, timeout=30) as response:
    release = json.load(response)
report = json.dumps({'installed_base': pin['tag'], 'latest': release['tag_name'],
                  'update_available': release['tag_name'] != pin['tag'],
                  'release_url': release['html_url'],
                  'policy': 'Build and validate a candidate before promotion.'}, indent=2)
if args.output:
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix('.tmp')
    temporary.write_text(report + '\n')
    temporary.replace(args.output)
print(report)
