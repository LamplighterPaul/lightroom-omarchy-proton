# lightroom-omarchy-proton

Full GE-Proton through UMU/Steam Linux Runtime, with a small Lightroom patch set.
The first build reuses the checksum-pinned GE distribution and rebuilds changed
Wine components in the digest-pinned Steam Runtime SDK. It does not rebuild every
graphics, codec and helper dependency. `upstream.json` records provenance.

Patches preserve an explicitly selected prefix username for credential migration,
implement monitor scaling, and center Lightroom's Windows menu entries with more
spacing. The existing experimental Direct2D colour-management pass-through is
retained for startup compatibility; it is **not a correct colour transform**.

The firewall-rule enumerator is backported from Wine 11.10 commit
`2cac6ccf33c0807f374dc96f5a20e35a2da86157`, `dlls/hnetcfg/policy.c`, with explicit
empty-result counts and output-pointer checks. Lightroom dereferences the
enumerator after the older stub returns no object. This implements the empty
collection already reported by Wine; it does not modify the host firewall.

`LIGHTROOM_OMARCHY_USERNAME` is a migration compatibility setting, not a mechanism
to skip Adobe authentication. Ordinary Proton behaviour remains the default when
it is absent. `LIGHTROOM_OMARCHY_CENTER_MENUS=1` applies only to `lightroom.exe`.
The companion launcher reads Omarchy's current palette before launch and applies
it to Windows menu/dialog colours. Adobe's own interface is not restyled.

Build in a dedicated checkout: initialize submodules, fetch Wine commit
`e813ca5771658b00875924ab88d525322e50d39f` with its parent, run the upstream
`patches/protonprep-valve-staging.sh` and check its log for failed hunks. That
upstream script resets submodule worktrees; never run it over unrelated edits.
Apply the patches in `upstream.json` in order with `git -C wine apply`.
Run `compile-components.sh` inside the pinned SDK with the source and build paths
as arguments. Assemble with `package.py --archive ARCHIVE --build BUILD --output DEST`.

`check-upstream.py` checks GE's latest release without altering a running runtime.
New releases must be prepared, patched, built and tested as separate candidates
before promotion. Authentication, display scale, menu interaction, photo panning,
colour fidelity and restart stability remain release checks.

Wine-derived patches retain LGPL-2.1-or-later licensing and upstream notices.
No Adobe binaries, credentials or photographs belong in this source repository.

## Validated baseline, 19 September 2026

Version 11.7-1 launches the signed-in Lightroom 9.5.1 cloud library through UMU
1.4.4 and Steam Runtime 4. The operator reports stability after the firewall
COM enumerator fix, with 2x scaling and centered Tokyo Night menus. Credential
round-trip and firewall-enumeration probes pass. The manifest of the installed
components is in `validated-build-11.7-1.json`.

Photo panning still stutters and darkens. Neither 60/120 FPS nor colour fidelity
is verified. `experimental/d2d1-arc-geometry.patch` is a compiled but unvalidated
Wine 11.10 backport for curved UI geometry; it is not part of the installed
baseline or active patch list. Do not mix its build outputs into 11.7-1.

The companion launcher and performance tools live in
[omarchy-lightroom-cc](https://github.com/LamplighterPaul/omarchy-lightroom-cc).
Steam is not required. UMU still supplies compatibility metadata to Proton;
removing metadata is not evidence of reduced rendering overhead. Xalia and
per-game ProtonFixes are disabled by the Lightroom launcher. Further trimming
must be measured and preserve authentication, fonts, codecs and graphics.

## 11.7-2 shutdown export

Backports Wine 11.10's non-aborting `UiaDisconnectAllProviders` export. The API-set
probe passes through `ext-ms-win-uiacore-l1-1-2.dll`. Upstream's implementation is
still a no-op; this is not complete UI Automation resource cleanup. Testing the
next shutdown exposed an additional ntdll threadpool assertion (`!pool->shutdown`),
so clean shutdown remains unresolved. Startup/library and scaling still work.

## 11.7-3-rc1 performance candidate

`candidates/11.7-3-rc1.json` pins the exact components tested in the
[retained-photo report](https://github.com/LamplighterPaul/omarchy-lightroom-cc/blob/1cfd30a/docs/loupe-retention-2026-09-19.md).
It combines the 11.7-2 components with deferred threadpool close, optional menu
phase timing and the opt-in X11 photo-background retention patch. The existing
experimental colour pass-through remains unchanged. This is a candidate, not
an update to `upstream.json` or the default runtime.

Assemble from a runtime holding those exact component bytes:

```sh
python3 omarchy/package.py --archive /path/to/GE-Proton11-7-x86_64.tar.gz \
  --components-from /path/to/tested-runtime \
  --recipe omarchy/candidates/11.7-3-rc1.json \
  --output /path/to/new/lightroom-omarchy-proton-11.7-3-rc1
```

The packager verifies the GE archive, every selected component, and every source
patch against the recipe. It extracts a fresh GE distribution and copies only
those verified components. This avoids including an unrelated experiment from
shared build outputs. It does not claim that every GE dependency was rebuilt,
or that the archive is byte-for-byte reproducible. Existing outputs are refused.
The original `--build` mode remains available for a clean baseline build.

The companion launcher's `--runtime lightroom-omarchy-proton-11.7-3-rc1` selects
this staged directory. Its recommended environment enables photo retention;
`LRCC_RETAIN_LOUPE=0` explicitly disables it for comparison. Menu instrumentation
remains off unless `LIGHTROOM_OMARCHY_MENU_TIMING=1` is set. Close all processes
in a prefix before selecting a different runtime; the launcher checks live
Wine mappings to reject a mixed runtime session.
