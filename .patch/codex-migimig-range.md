# Migimig range-selective candidate

Base: validated reference 719a1d3a3dd9b043b70b893e16b9decb690eefcc.
This candidate excludes the separate Sync PR178/243 experiment.
Original patch by Claude: Documents/ClaudeTerminal/pour_codex/migimig-1-range-selective.
Original imported commit: 46e1b8e (preserves supplied attribution).

Review found a coverage issue: Unmap invokes BigPageTableOp even for a 4 KiB subrange.
That updates a whole big-page entry but the original journal recorded only the requested bytes.
The regression fixture caches 8192 bytes at GPU 32768, then frees 4096 bytes at GPU 0
through a big-page operation. Original patch incorrectly returns cached 8192; uncached returns 0.
Record coverage rounded to each operation's page granularity fixes this conservatively.

MSVC standalone harness extracts actual cache/journal methods and uses an independent page model
for uncached queries: 100000 deterministic random comparisons, repeated smaller requests,
ring wrap/overflow, adjacent ranges, remaps and partial big-page unmap.
Selective on/off both checksum 693037691; 10000 unrelated map changes incur 0 vs 10000 walks.
This is a focused algorithm check, not a full GPU-thread concurrency or game benchmark.

Build MSVC Release; no rendering settings, shaders, JIT, or existing reference binary altered.
EDEN_NX2_RANGE_SELECTIVE=0 is the diagnostic fallback.
In-game performance and visual validation pending.
