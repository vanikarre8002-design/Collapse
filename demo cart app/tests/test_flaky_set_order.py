"""
FLAKY TEST #1 — set-order / hash-order dependence.

True cause: `Cart.applied_discounts()` returns a `set[str]`. Python
randomizes hash seeds per-process by default (PYTHONHASHSEED), so
set iteration order is not stable across runs. This test indexes
into the set assuming a fixed "first" element — that assumption is
false.

Deterministic reproduction: run with a fixed PYTHONHASHSEED, e.g.
    PYTHONHASHSEED=0 pytest tests/test_flaky_set_order.py -v
    PYTHONHASHSEED=2 pytest tests/test_flaky_set_order.py -v
Different seeds put different elements first — some seeds fail
10/10, some pass 10/10, for the SAME code. That's the proof.

See GROUND_TRUTH.md for the full writeup. Do not "fix" this by
sorting the set only inside the test — fix the assertion itself.
"""
from shoplite.cart import Cart


def test_first_discount_code_is_bulk():
    cart = Cart()
    cart.add_item("sku-002", "Mechanical Keyboard", 50.0, quantity=1)
    cart.add_item("sku-003", "USB-C Cable", 9.99, quantity=1)
    cart.add_item("sku-001", "Wireless Mouse", 45.0, quantity=1)
    # Subtotal = 104.99 -> BULK10 applies. 3 items -> MULTIITEM applies too.
    discounts = cart.applied_discounts()
    # BUG: assumes a set has a stable "first" element. It doesn't.
    assert list(discounts)[0] == "BULK10"
