"""
FLAKY TEST #4 — Randomness without fixed seed (Layer 4).

True cause: `draw_lucky_discount()` uses `random.random() < 0.5`.
Without a fixed seed (`random.seed(x)`), it randomly fails ~50% of runs.

Deterministic reproduction:
    Lever: fixed seed
    random.seed(42) -> deterministically passes (or fails depending on seed).
"""
import random
from shoplite.promotions import draw_lucky_discount


def test_lucky_draw_applies_discount():
    # BUG: Depends on unseeded global PRNG state.
    # ~50% of runs will return 0.0 and fail this assertion.
    discount = draw_lucky_discount(100.0)
    assert discount == 15.0
