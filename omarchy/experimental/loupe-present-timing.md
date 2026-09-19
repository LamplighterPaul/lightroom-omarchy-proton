# Photo presentation timestamps (diagnostic only)

Apply `loupe-present-timing.patch` after `retain-loupe-background.patch` to the
same pinned Wine source. Rebuild `dlls/winex11.drv/winex11.so` and copy only that
component into a **new diagnostic runtime copied from rc1**. Do not mutate the
packaged candidate or an active runtime.

Set `LIGHTROOM_OMARCHY_PRESENT_TRACE` to an absolute output filename prefix.
Each process writes `<prefix>.<pid>.bin`, opened exclusively with mode 0600.
The desktop launcher's environment allowlist does not forward this variable;
for the owned private Weston fixture use `LRCC_DISPATCHED=1`, `DISPLAY=:1`,
`WAYLAND_DISPLAY=lightroom-test` and its explicit copied `LRCC_PREFIX`.
Do not use that dispatch bypass to launch windows on the user's desktop.

Only surfaces already classified as child `loupeView` are recorded. There is
no screenshot, GPU readback, GPU wait, or per-frame stdio operation. A 6.5 MiB
shared file mapping is allocated at first use, before its first timestamp.
Rows are appended to 65,536 slots; a release-stored 1-based commit word marks a
complete row. Recording stops at capacity. Read the file after gestures stop;
keep the raw mapping private and publish numeric extracts as needed.

The little-endian x86-64 format is `LRPRES01`, uint64 capacity, then capacity
rows of 13 uint64s: start, geometry-done, clip-done, blit-done, flush-done, end,
HWND, surface pointer, pthread token, outcome, width, height, commit. Times are
host CLOCK_MONOTONIC nanoseconds. Outcomes: 1 no HDC, 2 alpha surface, 3 layered
path, 4 empty rectangle, 5 missing client rectangle, 6 copy not completed,
7 copy completed. Detailed copy/flush phases cover the non-layered path only.

Use `diagnostics/present-trace.py` in the main Lightroom repository to select
an `isolated-input.py` phase and summarize each surface/extent independently.
The callback and XFlush timings are CPU-side submission durations, **not GPU
completion, compositor presentation, or input-to-display latency**. Clock reads,
atomics and mapping page faults have overhead; this is diagnostic evidence,
not a production optimization. No timing patch is included in rc1.
