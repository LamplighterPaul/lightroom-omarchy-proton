# Runtime build and packaging

[lightroom-omarchy-proton](../README.md) supplies the runtime for
[omarchy-lightroom-cc](https://github.com/LamplighterPaul/omarchy-lightroom-cc),
which owns setup, desktop integration, launch profiles and diagnostics.

## Current recipe

**11.7-3-rc2** is selected by the companion launcher's performance profile.
[candidates/11.7-3-rc2.json](candidates/11.7-3-rc2.json) pins the GE archive,
SDK, fourteen component hashes and the source patches used for that candidate.
[The rc2 build notes](candidates/11.7-3-rc2.md) document its single driver change
relative to rc1 and the recovery tests.

`upstream.json` still describes the **11.7-2 baseline**, used by the original
build path. The older `validated-build-11.7-1.json`, `validated-build-11.7-2.json`
and rc1 recipe remain historical records. They are not the current performance
profile. The baseline label does not establish that all workflows are stable.

## What the patches provide

- Preserve an explicitly selected Windows username for authenticated-prefix
  migration. Adobe authentication and subscription validation still apply.
- Supply monitor scaling and centered, spaced Windows menu entries. The
  companion launcher applies the Omarchy palette; Adobe's own UI is retained.
- Implement the firewall-rule enumerator expected at startup. This follows the
  empty collection reported by Wine and does not change the host firewall.
- Retain the experimental Direct2D colour-management pass-through needed for
  startup compatibility. It does not implement a correct colour transform.
- Add the UI Automation shutdown export and deferred threadpool close fix.
- Retain the presented photo during the reproduced full-client background fill.
- Recover from the specific stale RandR CRTC query that caused a fatal X11 exit.

The UI Automation export remains a no-op, rather than complete resource cleanup.
Optional menu timing instrumentation is included but disabled unless requested.
The separate experimental directory also contains unpromoted diagnostics and
patches; its contents must not be assumed to be part of rc2.

## Assemble the current candidate

Given the pinned GE archive and a runtime containing the exact rc2 component
bytes:

```sh
python3 omarchy/package.py --archive /path/to/GE-Proton11-7-x86_64.tar.gz \
  --components-from /path/to/tested-rc2-runtime \
  --recipe omarchy/candidates/11.7-3-rc2.json \
  --output /path/to/new/lightroom-omarchy-proton-11.7-3-rc2
```

The packager verifies the archive, components and source patches against the
recipe, extracts a fresh GE distribution and copies the verified components.
It refuses an existing output directory. This assembles a runtime from known
bytes; it does not rebuild all dependencies or promise byte-identical archives.

Place the assembled runtime in the companion launcher's application runtime
directory. Once its prerequisites, including MangoHud, are staged, select the
`performance` profile as described in the
[launcher README](https://github.com/LamplighterPaul/omarchy-lightroom-cc#development-and-testing).
Close Lightroom normally and stop its prefix before switching runtimes. The
launcher rejects a prefix that still has processes from another runtime.

## Source rebuilds

Use a dedicated checkout and the SDK digest pinned in the recipe. The GE base
uses Wine commit `e813ca5771658b00875924ab88d525322e50d39f`. Initialize the required
submodules, run the upstream `patches/protonprep-valve-staging.sh` and check for
failed hunks. That script resets submodule worktrees; do not run it over existing
work. Apply the recipe's base and additional patches in their dependency order.

`compile-components.sh` builds the original baseline components. Rc1's ntdll
and photo-retention changes and rc2's X11 change also require their respective
component targets; see the candidate and experimental notes. The original
`package.py --build` path uses the older baseline recipe. For rc2, assemble with
`--components-from` and its explicit recipe after verifying rebuilt hashes.
Do not copy all outputs from a shared experimental build into a release.

## Updates and reduction work

`check-upstream.py` checks for new GE releases without replacing the active
runtime. Each update needs preparation, patch application, a separate build and
regression checks before selection.

The package still includes the full GE distribution. Xalia and game-specific
ProtonFixes are disabled by the launcher, while UMU continues to provide
Proton's runtime environment and compatibility metadata. A dependency/footprint
audit and measured package reduction remain future work. Keep authentication,
fonts, codecs, graphics and workflow tests in that evaluation.

## Validation boundaries

Photo interaction, scaling, normal restart and injected stale-CRTC recovery have
been exercised on the development setup. **Local import/export and colour
accuracy remain unverified**, as do a fresh Proton-only sign-in, complete editing
and sync coverage, and real sleep/wake recovery. Current measurements and gaps
are maintained in the [companion README](https://github.com/LamplighterPaul/omarchy-lightroom-cc).
Wine-derived patches retain their upstream licenses and notices. Adobe binaries,
credentials and photographs do not belong in this source repository.
