# Aggregate menu API cost (diagnostic only)

Apply after `menu-input-timing.patch` and rebuild x64 Unix win32u. Stage in a
separate rc1-derived runtime; do not change the production runtime.

Set LIGHTROOM_OMARCHY_INPUT_TIMING=1 and LIGHTROOM_OMARCHY_INPUT_COST=1, with
`LRCC_WINEDEBUG=-all,+timestamp,warn+key,warn+menu,err+all`, in the copied private
fixture. The added counters cover only the main-thread interval between posting
WM_SYSCHAR and the next PeekMessage entry. Four wrappers count and time
EnableMenuItem, CheckMenuItem, ThunkedMenuItemInfo and DrawMenuBar. Each interval
emits one LR_COST row, including wall and thread CPU time. No per-call output,
menu strings, document contents or API behavior changes are added.

API measurements include timer overhead and exclude entry/exit through the
Windows/Unix syscall boundary. They are inclusive if an instrumented API nests
another. Counters do not cover every Win32 API. The separate `menu-api-bench.c`
in the main Lightroom repository measures complete representative API calls,
including the boundary; it is synthetic, not an exact application replay.

This diagnostic was exercised in `lightroom-omarchy-proton-menu-cost`, whose
x64 Unix win32u hash is
`a7c39b7d9310ea9d4c874ad8ef6fbabfbfe2815dc8e5a7d722eec15c25cdefd9`.
It is not a performance fix and is not included in rc1.
