# lightroom-omarchy-proton

A **Lightroom-focused GE-Proton fork for Omarchy**, maintained by
[Paul Zammit](https://github.com/LamplighterPaul). It provides the compatibility
patches and pinned runtime components used to run Adobe Lightroom CC (cloud)
on Linux.

**Start with [omarchy-lightroom-cc](https://github.com/LamplighterPaul/omarchy-lightroom-cc)**
for the launcher, environment setup, desktop integration, performance tools and
validation reports. This repository owns the Proton runtime and build recipes;
the two projects are developed together.

## Current status

**20 September 2026 — 11.7-3-rc2 is the tested runtime selected by the companion
launcher's performance profile.** It is based on **GE-Proton11-7** and runs
through UMU and Steam Runtime 4, without requiring the Steam client.

The current build combines the full pinned GE distribution with fourteen
source-rebuilt Wine components. The authenticated cloud library, photo viewing,
operator-tested basic editing, 2x scaling, themed Windows menus and normal
close/restart work on the development machine. Performance and stability have
improved substantially from the initial standalone Wine experiments.

## Improvements in the combined setup

- **Photo retention:** suppresses the reproduced background repaint that caused
  black flashes while dragging. Controlled captures went from 112/280 blank
  samples with retention disabled to zero with it enabled.
- **Responsiveness:** the companion launcher applies a measured UI-thread
  scheduling hint (about 30% faster keyboard-menu opening in the controlled
  comparison) and disables zoom animation (343 ms to 155–162 ms median settling).
- **Frame pacing:** the measured launcher/limiter configuration produced roughly
  8.33 ms median renderer intervals during sustained private-fixture panning.
  Stalls remain; physical-display 120 FPS is unproven.
- **Startup and shutdown compatibility:** credential-migration support,
  firewall COM enumeration, UI Automation export and deferred threadpool close
  address observed startup and shutdown failures.
- **Display-query recovery in rc2:** handles the stale CRTC query that previously
  terminated the process. An old-build probe reproduced the fatal error;
  patched Lightroom survived eight injected failures and later interactions.

The launcher owns the scheduling, animation, limiter and theme configuration;
this fork supplies the runtime changes. Detailed measurements and limitations
are in the [companion project's status](https://github.com/LamplighterPaul/omarchy-lightroom-cc#current-status)
and [rc2 crash report](https://github.com/LamplighterPaul/omarchy-lightroom-cc/blob/main/docs/randr-recovery-2026-09-20.md).

## Validation gaps

**Local file import and export are unproven.** Basic editing of existing cloud
photos does not validate those workflows, complete tool coverage, edit
persistence or reliable cloud upload.

**Colour accuracy is unproven.** The experimental Direct2D colour-management
pass-through remains in this build. Correct ICC/display transforms, gamut
handling, soft proofing and exported colour fidelity have not been established.
This is not yet a validated professional colour workflow.

Fresh Proton-only installation/sign-in, real sleep/wake recovery, long-session
stability and broader hardware coverage remain open. The working environment
uses a migrated authenticated prefix. Residual menu and photo-loading stalls
remain despite the improvements.

## Build, updates and runtime size

See [the build and packaging guide](omarchy/README.md), the
[rc2 component recipe](omarchy/candidates/11.7-3-rc2.json) and
[rc2 build notes](omarchy/candidates/11.7-3-rc2.md). Candidates are assembled from
verified component bytes; this is not a rebuild of every GE dependency.

The runtime is **still the full GE-Proton package with targeted replacements**.
A footprint/dependency audit and a smaller Lightroom-specific package are future
work. No minimal-runtime or package-size reduction has been demonstrated.
Disabling game-specific helpers or hiding Steam metadata does not by itself
remove the underlying components or prove lower overhead. Trimming must retain
and test the libraries needed for authentication, fonts, codecs and graphics.

The upstream checker reports new GE releases. Updates are prepared and tested
as separate candidates before selection; a running runtime is not automatically
replaced. The older 11.7-2 baseline is still recorded in `omarchy/upstream.json`;
use the explicit rc2 recipe for the current performance configuration.

## Credits and licensing

Built on [GE-Proton](https://github.com/GloriousEggroll/proton-ge-custom),
Valve Proton, Wine, DXVK, vkd3d-proton and UMU. Existing component licenses and
notices remain in place; see [LICENSE](LICENSE), [LICENSE.proton](LICENSE.proton)
and [the companion project's attribution](https://github.com/LamplighterPaul/omarchy-lightroom-cc/blob/main/THIRD_PARTY.md).
The [inherited GE-Proton README](README.upstream.md) is retained as upstream
reference, separate from this project's Lightroom instructions.

This is an independent compatibility project. Adobe binaries, credentials and
photographs are not included. Report Lightroom-specific results in the
[companion issue tracker](https://github.com/LamplighterPaul/omarchy-lightroom-cc/issues)
and runtime/build issues [here](https://github.com/LamplighterPaul/lightroom-omarchy-proton/issues).
