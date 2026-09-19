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
