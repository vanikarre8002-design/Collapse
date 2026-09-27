"""Shared in-memory inventory store for ShopLite.

NOTE: This module-level dict is intentional shared state — it's what
makes `test_flaky_shared_state.py` order-dependent. Don't "fix" this
by refactoring it away before Bob gets a chance to diagnose it.
"""

INITIAL_STOCK = {
    "sku-001": 10,  # Wireless Mouse
    "sku-002": 5,   # Mechanical Keyboard
    "sku-003": 20,  # USB-C Cable
    "sku-004": 15,  # Laptop Stand
}

INVENTORY = dict(INITIAL_STOCK)


def get_stock(sku: str) -> int:
    return INVENTORY.get(sku, 0)


def reduce_stock(sku: str, qty: int) -> None:
    if sku not in INVENTORY:
        raise KeyError(f"Unknown SKU: {sku}")
    if INVENTORY[sku] < qty:
        raise ValueError(f"Insufficient stock for {sku}: requested {qty}, available {INVENTORY[sku]}")
    INVENTORY[sku] -= qty


def reset_inventory() -> None:
    """Test helper — NOT called automatically by any fixture.
    Tests that assume fresh stock without calling this or using
    an autouse fixture will flake depending on run order.
    """
    INVENTORY.clear()
    INVENTORY.update(INITIAL_STOCK)
