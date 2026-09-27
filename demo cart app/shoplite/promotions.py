import random
from datetime import datetime
import zoneinfo


def draw_lucky_discount(cart_total: float) -> float:
    """Flaky #4 (Randomness): Lucky draw discount.
    If random.random() < 0.5, grants 15% discount.
    Without a fixed seed, tests asserting the discount will flake 50% of the time.
    """
    if random.random() < 0.5:
        return round(cart_total * 0.15, 2)
    return 0.0


def is_same_day_delivery_eligible(order_time: datetime | None = None) -> bool:
    """Flaky #5 (Timezone): Same-day delivery cutoff is 18:00 local time.
    If naive datetime or system local time is used without explicit UTC/tz conversion,
    this returns different results depending on the runner's timezone.
    """
    if order_time is None:
        order_time = datetime.now()
    # Flaky if evaluated without tz awareness across runners
    return order_time.hour < 18
