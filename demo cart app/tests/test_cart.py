"""Normal cart tests — reliable baseline that should ALWAYS pass."""

from shoplite.cart import Cart


def test_cart_empty():
    cart = Cart()
    assert cart.subtotal() == 0.0
    assert cart.applied_discounts() == set()
    assert cart.total() == 0.0


def test_subtotal_single_item():
    cart = Cart()
    cart.add_item("sku-001", "Wireless Mouse", 25.0, quantity=2)
    assert cart.subtotal() == 50.0


def test_bulk_discount_applies_over_100():
    cart = Cart()
    cart.add_item("sku-002", "Mechanical Keyboard", 120.0, quantity=1)
    assert "BULK10" in cart.applied_discounts()
    assert cart.total() == 108.0


def test_no_discount_under_threshold():
    cart = Cart()
    cart.add_item("sku-003", "USB-C Cable", 9.99, quantity=1)
    assert cart.applied_discounts() == set()
    assert cart.total() == 9.99


def test_multi_item_discount():
    cart = Cart()
    cart.add_item("sku-001", "Wireless Mouse", 10.0)
    cart.add_item("sku-002", "Mechanical Keyboard", 10.0)
    cart.add_item("sku-003", "USB-C Cable", 10.0)
    assert "MULTIITEM" in cart.applied_discounts()
    assert cart.total() == 28.5  # 30 * 0.95


def test_volume_discount():
    cart = Cart()
    cart.add_item("sku-003", "USB-C Cable", 10.0, quantity=5)
    assert "VOLUME" in cart.applied_discounts()
    assert cart.total() == 46.5  # 50 * 0.93


def test_combined_all_discounts():
    cart = Cart()
    cart.add_item("sku-001", "Wireless Mouse", 50.0, quantity=1)
    cart.add_item("sku-002", "Mechanical Keyboard", 50.0, quantity=1)
    cart.add_item("sku-003", "USB-C Cable", 5.0, quantity=6)
    # Subtotal = 50 + 50 + 30 = 130 (>= 100 -> BULK10)
    # Item count = 3 (>= 3 -> MULTIITEM)
    # Cable qty = 6 (>= 5 -> VOLUME)
    # Total discount rate = 0.10 + 0.05 + 0.07 = 0.22 (22%)
    discounts = cart.applied_discounts()
    assert discounts == {"BULK10", "MULTIITEM", "VOLUME"}
    assert cart.total() == 101.4  # 130 * 0.78
