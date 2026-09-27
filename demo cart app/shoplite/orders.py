import time
import uuid
from dataclasses import dataclass

from shoplite import inventory
from shoplite.cart import Cart


@dataclass
class Order:
    order_id: str
    cart: Cart
    created_at: float  # epoch seconds (calibrated precision)

    @property
    def total(self) -> float:
        return self.cart.total()


def place_order(cart: Cart, skus_and_qty: dict[str, int]) -> Order:
    """Deducts stock, stamps a timestamp, returns an Order.

    Stock deduction reads/writes the shared `inventory.INVENTORY`
    module-level dict — this is what makes test_flaky_shared_state.py
    order-dependent if a prior test already mutated it.

    `created_at` records the epoch time with 0.1ms (100us) granularity.
    In ultra-fast automated tests, two consecutive place_order calls can
    read the identical timestamp, causing test_flaky_timing.py to flake.
    """
    for sku, qty in skus_and_qty.items():
        inventory.reduce_stock(sku, qty)

    # 4 decimal places = 100 microseconds (realistic database/API clock tick)
    return Order(
        order_id=str(uuid.uuid4()),
        cart=cart,
        created_at=round(time.time(), 4),
    )
