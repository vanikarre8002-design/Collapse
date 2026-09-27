"""
FLAKY TEST #2 — time-based race.

True cause: `place_order()` stamps `created_at = round(time.time(), 4)`.
Two `place_order()` calls placed microseconds apart can return the
exact same float value. This test asserts the two timestamps always
differ, which is not guaranteed.

Deterministic reproduction: monkeypatch time.time() to return the
same fixed value on both calls -> fails 10/10. Monkeypatch it to
return two distinct increasing values -> passes 10/10. (Person A's
`prove` engine implements this as the "fixed time" lever.)

See GROUND_TRUTH.md for the full writeup. Do not "fix" this by
adding sleep() between the two calls — that hides the bug, it
doesn't fix it, and TEST_POLICY.md forbids it.
"""
from shoplite import inventory
from shoplite.cart import Cart
from shoplite.orders import place_order


def test_two_orders_have_distinct_timestamps():
    inventory.reset_inventory()

    cart1 = Cart()
    cart1.add_item("sku-001", "Wireless Mouse", 25.0, quantity=1)
    order1 = place_order(cart1, {"sku-001": 1})

    cart2 = Cart()
    cart2.add_item("sku-003", "USB-C Cable", 9.99, quantity=1)
    order2 = place_order(cart2, {"sku-003": 1})

    # BUG: time.time() resolution is not fine enough to guarantee
    # these differ when both calls happen this close together.
    assert order1.created_at != order2.created_at
