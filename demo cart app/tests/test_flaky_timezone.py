"""
FLAKY TEST #5 — Timezone dependence (Layer 4).

True cause: Evaluates delivery cutoff hour based on local time.
In UTC or EST, tests running at different times of day or in
different server environments pass or fail.

Deterministic reproduction:
    Lever: TZ environment variable (TZ=UTC vs TZ=America/Los_Angeles).
"""
from datetime import datetime
from shoplite.promotions import is_same_day_delivery_eligible


def test_afternoon_order_eligible_for_same_day():
    # BUG: Relies on system local datetime without explicit timezone pinning.
    # Fails if local machine hour is >= 18.
    assert is_same_day_delivery_eligible() is True
