The Direct2D arc patch is adapted from Wine 11.10, commit
2cac6ccf33c0807f374dc96f5a20e35a2da86157, dlls/d2d1/geometry.c.
It retains Wine's LGPL-2.1-or-later scope. The arc-to-Bezier algorithm is based
on Microsoft's WPF implementation; its MIT notice is in WPF-LICENSE.txt.

This patch compiled for both Windows architectures, but is not installed and
has not passed geometry or Lightroom interaction checks. Keep its build output
separate from the active 11.7-1 baseline.
