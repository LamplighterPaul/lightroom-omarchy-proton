# Unpromoted diagnostics and candidates

`threadpool-deferred-close.patch` postpones shutdown until bound pool objects
have been released. It addresses the timer-queue assertion seen during Lightroom
exit. Standalone x64/i386 lifetime probes pass. Keep it out of `upstream.json`
until application close/reopen and runtime packaging are validated.

`menu-phase-timing.patch` measures synchronous menu initialization, popup
creation, layout, show and paint. Apply after the current centered-menu patch;
rebuild `dlls/win32u/win32u.so`. Enable only for profiling with
`LIGHTROOM_OMARCHY_MENU_TIMING=1` and Wine `warn+menu` logging. It logs phase names
and durations, never menu labels. These timings exclude input arrival and actual
compositor presentation. It changes no menu behavior and is not a speed fix.

The active runtime manifest does not include either patch.

## Direct2D arc candidate

The Direct2D arc patch is adapted from Wine 11.10, commit
2cac6ccf33c0807f374dc96f5a20e35a2da86157, dlls/d2d1/geometry.c.
It retains Wine's LGPL-2.1-or-later scope. The arc-to-Bezier algorithm is based
on Microsoft's WPF implementation; its MIT notice is in WPF-LICENSE.txt.

This patch compiled for both Windows architectures, but is not installed and
has not passed geometry or Lightroom interaction checks. Keep its build output
separate from the active 11.7-1 baseline.

## Lightroom photo retention candidate

`retain-loupe-background.patch` targets the observed full-client `PATCOPY` from
Lightroom's `loupeView` WM_PAINT handler. It overwrites the displayed photo
between GPU copies on Wine's offscreen X11 path. The opt-in workaround retains
the last presented image for that fill only. Enable with
`LIGHTROOM_OMARCHY_RETAIN_LOUPE=1`; rebuild `dlls/winex11.drv/winex11.so`.

The driver tracks successfully presented native surfaces, clears tracking on
detach/destruction, and checks live native references and presentation ownership.
It caches the DCE's owning HWND when the drawable is assigned, avoiding new
NtUser calls under the GDI/DC lock. The HWND, drawable, origin and full-client
extent must match. Unrelated windows and partial fills remain eligible for GDI
painting. These are implementation constraints; fallback/overlay/lifetime
regression validation is still incomplete. The production manifest is unchanged.

An initial implementation reproduced zero blank framebuffer samples with the
workaround enabled, 112 disabled, and zero enabled again (280 samples per run).
Subsequent revisions remove window lookups from drawing and tighten the cached
window identity. See the application repository's `docs/loupe-retention-2026-09-19.md`
for exact revision coverage. Appearance samples are not FPS measurements.

`x11-pixel-trace.patch` is a separate intrusive diagnostic against the prepared
baseline, not a runtime fix. Do not combine it with the retention patch. Set
`LRCC_PIXEL_TRACE=1`, `DISPLAY=:1`, and `LRCC_PIXEL_TRACE_TRIGGER` to a private
control-file path. Creating the file enables a fixed (1400,700) destination
pixel read; removing it disables reads. File contents select `b` before GPU
copy, `a` after, `s` XSync after, `t` PatBlt only, or another/empty value for all
instrumented phases. It refuses other X displays, but the operator must still
verify that :1 belongs to private Weston. It can hide or worsen flicker and
must never be used as a performance benchmark. Both patches retain Wine's
LGPL-2.1-or-later scope.
