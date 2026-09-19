# Menu character delivery probe (diagnostic only)

Apply `menu-input-timing.patch` to the pinned Wine source after the existing
menu timing patch. Rebuild `dlls/win32u/win32u.so` and stage only that component
in a new runtime copied from rc1. Do not replace an active or immutable runtime.

The probe logs when a WM_SYSCHAR is returned by PeekMessage, enters the normal
DispatchMessage parameter path, and reaches default WM_SYSCHAR/SC_KEYMENU handling.
It records window handles and message kinds, not menu text or document data.
It also tracks up to 64 PeekMessage calls after posting a menu character,
including entry, driver-event processing and internal queue retrieval.
Enable only in the copied private fixture with LIGHTROOM_OMARCHY_INPUT_TIMING=1,
LIGHTROOM_OMARCHY_MENU_TIMING=1 and WINEDEBUG timestamp/key tracing plus menu
warnings: `LRCC_WINEDEBUG=-all,+timestamp,+pid,+tid,+key,warn+menu,err+all`.
Using only `trace+key` suppresses the probe warnings. The launcher uses LRCC_WINEDEBUG for that setting. Key tracing itself
records key symbols: use only scripted fixture input and keep full logs private.

Wine timestamp logging uses NtGetTickCount, whereas the input/map recorder uses
host CLOCK_MONOTONIC. Calibrate the clock offset before relating these records;
within-log phase differences do not need that offset. Millisecond logging,
stdio and diagnostic scheduling affect timings. This probe is not a performance
optimization and is not part of the normal performance profile.
