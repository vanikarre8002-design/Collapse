"""
FLAKY TEST #3 — test-order / shared-state dependence.

True cause: `inventory.INVENTORY` is module-level, mutable, shared
state. `reset_inventory()` exists but nothing calls it automatically
before this test. This test assumes sku-002 starts with 5 units in
stock — true only if no earlier test in the run already reduced it.

Deterministic reproduction:
    pytest tests/test_flaky_shared_state.py -v         # default sequential: passes
    pytest tests/ -p randomly -v                        # randomized order: fails when
                                                       # mutating test runs first
"""
from shoplite import inventory
from shoplite.cart import Cart
from shoplite.orders import place_order


def test_keyboard_stock_starts_at_five():
    """BUG: Assumes fresh stock without calling reset_inventory() or
    using an autouse fixture. Fails if another test mutated sku-002 first."""
    assert inventory.get_stock("sku-002") == 5


def test_another_order_reduces_keyboard_stock():
    """Mutates shared module state. When pytest-randomly runs this one
    before `test_keyboard_stock_starts_at_five`, the latter fails."""
    inventory.reset_inventory()
    cart = Cart()
    cart.add_item("sku-002", "Mechanical Keyboard", 120.0, quantity=1)
    place_order(cart, {"sku-002": 1})
    assert inventory.get_stock("sku-002") == 4
