# ShopLite — Ground Truth

**Commit this file before Bob touches these tests, and record the commit hash in the README.**
This is what proves Bob found the real cause rather than being graded after the fact.

---

## Flaky Test 1 — `tests/test_flaky_set_order.py::test_first_discount_code_is_bulk`

- **Category:** `HASH_ORDER_DEPENDENCE` (lever: fixed seed / `PYTHONHASHSEED`)
- **True cause:** `Cart.applied_discounts()` returns a `set[str]`. Set iteration order depends on hash values, which are randomized per-process by Python's hash seed. The test indexes `list(discounts)[0]` assuming a stable first element.
- **Deterministic trigger:** Run with a fixed `PYTHONHASHSEED` — e.g., `PYTHONHASHSEED=0` vs `PYTHONHASHSEED=2`. Some seeds fail 10/10, others pass 10/10, for identical code. Proof is demonstrating both.
- **Correct fix:** Assert membership rather than position — `assert "BULK10" in discounts`.
- **Forbidden fixes (cheats):** `skip`/`xfail`, retry decorators, `time.sleep()`, weakening to `assert True` or `assert len(discounts) > 0`, or deleting the test.

---

## Flaky Test 2 — `tests/test_flaky_timing.py::test_two_orders_have_distinct_timestamps`

- **Category:** `TIME_DEPENDENCE` (lever: fixed/controlled clock)
- **True cause:** `place_order()` stamps `created_at = round(time.time(), 4)`. When two orders are placed microseconds apart in fast succession, the timestamps can land on the exact same tick.
- **Deterministic trigger:** Monkeypatch `time.time` to return the same fixed value on both calls -> fails 10/10; monkeypatch to return two distinct increasing values -> passes 10/10. (Person A's `prove` engine implements this as the "fixed time" lever.)
- **Correct fix:** Stop asserting on timestamp uniqueness — assert on `order_id` (UUID-based, always unique) instead (`assert order1.order_id != order2.order_id`), or switch the uniqueness guarantee to an atomic monotonic sequence if ordering by creation sequence is required.
- **Forbidden fixes (cheats):** Adding `time.sleep()` between the two calls, `skip`, `retry`, or removing the assertion.

---

## Flaky Test 3 — `tests/test_flaky_shared_state.py::test_keyboard_stock_starts_at_five`

- **Category:** `SHARED_STATE` / `TEST_ORDER_DEPENDENCE` (lever: test order)
- **True cause:** `inventory.INVENTORY` is shared, mutable, module-level state. `reset_inventory()` exists but nothing calls it automatically before `test_keyboard_stock_starts_at_five`. The test assumes fresh stock (5 units), which only holds if no earlier test in the run mutated `sku-002`.
- **Deterministic trigger:** Passes when run first or alone; fails deterministically when a test that reduces `sku-002` stock runs first (e.g., when run with `pytest-randomly` or when test order is inverted).
- **Correct fix:** Call `inventory.reset_inventory()` in an autouse pytest fixture, or call `inventory.reset_inventory()` before asserting, or inject an isolated inventory store per test.
- **Forbidden fixes (cheats):** Reordering tests to "get lucky," `skip`, `retry`, deleting the test or weakening `assert inventory.get_stock("sku-002") >= 0`.

---

## Flaky Test 4 — `tests/test_flaky_randomness.py::test_lucky_draw_applies_discount` (Layer 4)

- **Category:** `RANDOMNESS` (lever: fixed seed / `random.seed`)
- **True cause:** `draw_lucky_discount()` calls unseeded `random.random() < 0.5`. ~50% of runs return 0.0 and fail.
- **Deterministic trigger:** Set seed before execution: `random.seed(1)` fails 10/10; `random.seed(0)` passes 10/10.
- **Correct fix:** Dependency inject or mock the random generator, or test the probability distribution / mock the return value in the test.
- **Forbidden fixes (cheats):** Retry loop until pass, skipping, removing the assertion.

---

## Flaky Test 5 — `tests/test_flaky_timezone.py::test_afternoon_order_eligible_for_same_day` (Layer 4)

- **Category:** `TIMEZONE` (lever: `TZ` environment variable)
- **True cause:** Relies on local system datetime instead of explicit timezone-aware datetimes.
- **Deterministic trigger:** Set `TZ=Pacific/Auckland` vs `TZ=UTC`.
- **Correct fix:** Pass an explicit timezone-aware datetime or freeze the time with timezone awareness.
- **Forbidden fixes (cheats):** `skip`, `sleep`.
