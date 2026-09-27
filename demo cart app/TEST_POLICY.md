# ShopLite Test Policy

These rules apply to every fix made to a failing or flaky test in this
repository — whether by Bob or by a human engineer. This file exists so Bob's
document-understanding step has real project rules to read and strictly follow.

1. **No Skip / xfail**: Never mark a test `@pytest.mark.skip`, `@pytest.mark.xfail`,
   or "expected failure" to make it stop failing.
2. **No Sleep / Delay Hacks**: Never add `time.sleep()`, artificial delays, retry
   decorators (`pytest-rerunfailures`), or rerun-until-pass loops to hide flakiness.
3. **No Weakening or Deletion**: Never delete a failing test, weaken its assertion
   (e.g., `assert True`, `assert x is not None` instead of exact check), or narrow
   what it checks without an explicit, documented reason.
4. **Address the Root Cause**: A fix must address the root cause identified during
   investigation (e.g. hash order, race conditions, shared state mutation) — not just
   make the symptom disappear.
5. **Mandatory Verification**: A fix counts as complete only after verification:
   the exact failing condition must be reproduced and shown resolved, and the full
   test suite must still pass afterward.
6. **Explicit Honesty**: If a test's behavior is genuinely non-deterministic and
   cannot be made deterministic (e.g. external network failure), that must be
   explicitly documented — it cannot be silently reported as "fixed."
