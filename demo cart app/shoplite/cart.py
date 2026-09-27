from dataclasses import dataclass


@dataclass
class LineItem:
    sku: str
    name: str
    unit_price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.unit_price * self.quantity, 2)


class Cart:
    def __init__(self):
        self.items: list[LineItem] = []

    def add_item(self, sku: str, name: str, unit_price: float, quantity: int = 1):
        self.items.append(LineItem(sku, name, unit_price, quantity))

    def subtotal(self) -> float:
        return round(sum(item.subtotal for item in self.items), 2)

    def applied_discounts(self) -> set[str]:
        """Return the set of discount codes that apply to this cart.

        Returns a set (not a list) because discount codes are
        conceptually unordered. A test that assumes stable iteration
        order over this set will flake under Python's hash
        randomization (PYTHONHASHSEED) — see test_flaky_set_order.py.
        """
        codes: set[str] = set()
        if self.subtotal() >= 100.0:
            codes.add("BULK10")
        if len(self.items) >= 3:
            codes.add("MULTIITEM")
        if any(item.quantity >= 5 for item in self.items):
            codes.add("VOLUME")
        return codes

    def total(self) -> float:
        discount_rate = 0.0
        discounts = self.applied_discounts()
        if "BULK10" in discounts:
            discount_rate += 0.10
        if "MULTIITEM" in discounts:
            discount_rate += 0.05
        if "VOLUME" in discounts:
            discount_rate += 0.07
        return round(self.subtotal() * (1 - discount_rate), 2)
