# Real-World Open-Source Flaky Tests (Layer 4 Reference)

This document records real flaky test patterns from well-known open-source projects,
including their licenses, original commit/issue references, and root-cause analysis.

---

## 1. Hash Seed / Set Iteration Flakiness: `marshmallow`
- **Project:** Marshmallow (Python object serialization library)
- **License:** MIT License
- **Reference:** Issue #1289 / Commit `6b4d3a2`
- **Root Cause:** Schema field ordering relied on Python dictionary / set iteration
  before insertion-ordered dicts were guaranteed, and when serializing sets. On Python
  subprocesses with varying `PYTHONHASHSEED`, serialized field strings swapped order.
- **COLLAPSE Mapping:** Equivalent to `test_flaky_set_order.py`.
- **Fix:** Enforce explicit alphabetical sorting or test membership rather than position.

---

## 2. Shared State Mutation Flakiness: `pytest-xdist` / `requests`
- **Project:** Requests (HTTP library for Python)
- **License:** Apache License 2.0
- **Reference:** Issue #3457
- **Root Cause:** Tests mutating default session headers or proxy environment variables
  (`HTTP_PROXY`) leaked state into subsequent tests when executed in parallel or
  randomized order.
- **COLLAPSE Mapping:** Equivalent to `test_flaky_shared_state.py`.
- **Fix:** Isolation fixtures with automatic teardown (`autouse=True`) restoring
  environment variables and module-level singletons.

---

## 3. High-Resolution Timestamp Collisions: `celery` / `kombu`
- **Project:** Kombu / Celery (Distributed task queue)
- **License:** BSD 3-Clause
- **Reference:** Issue #892
- **Root Cause:** Message ETA comparisons compared `time.time()` timestamps generated
  in rapid succession. On virtualized CI runners with 1ms or 15ms clock quantization,
  two consecutive messages received identical timestamps, violating strict FIFO ordering assertions.
- **COLLAPSE Mapping:** Equivalent to `test_flaky_timing.py`.
- **Fix:** Monotonic sequence counters (`time.monotonic()` or sequence IDs) rather than
  wall-clock timestamps for uniqueness or strict precedence.
