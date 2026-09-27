"""Normal order and inventory tests — reliable baseline that should ALWAYS pass."""

import pytest
from shoplite import inventory
from shoplite.cart import Cart
from shoplite.orders import place_order


@pytest.fixture(autouse=True)
def clean_inventory():
    """Guarantee test isolation for normal inventory tests."""
    inventory.reset_inventory()
    yield
    inventory.reset_inventory()


def test_inventory_get_stock_and_reset():
    assert inventory.get_stock("sku-001") == 10
    inventory.reduce_stock("sku-001", 3)
    assert inventory.get_stock("sku-001") == 7
    inventory.reset_inventory()
    assert inventory.get_stock("sku-001") == 10


def test_inventory_insufficient_stock_raises():
    with pytest.raises(ValueError, match="Insufficient stock"):
        inventory.reduce_stock("sku-002", 999)


def test_inventory_unknown_sku_raises():
    with pytest.raises(KeyError, match="Unknown SKU"):
        inventory.reduce_stock("sku-unknown-999", 1)


def test_place_order_success():
    cart = Cart()
    cart.add_item("sku-001", "Wireless Mouse", 25.0, quantity=2)
    order = place_order(cart, {"sku-001": 2})

    assert order.order_id is not None
    assert len(order.order_id) == 36  # Valid UUID4 string
    assert order.total == 50.0
    assert inventory.get_stock("sku-001") == 8
