# COLLAPSE Engine Specification (Person A Handoff)

The 5 engine commands:
1. `detect`: Run every test 10 times; flag tests that both pass and fail.
2. `prove`: For each flagged test, sweep levers (fixed seed, fixed time, test order, timezone).
   Find lever that triggers 10/10 failures, then confirm 10/10 passes without it.
3. `check`: Reject AI cheats (skip, sleep, retry, deleted test, weakened asserts).
4. `verify`: Run 30 times under the trigger + full suite once.
5. `report`: Write `results/summary.json` and `results/REPORT.md`.
