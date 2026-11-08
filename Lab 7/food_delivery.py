import math
import re

MAX_QTY = 999            # sanity cap on quantity per line item
MAX_DISCOUNT = 100       # a coupon can never exceed 100%
_QTY_RE = re.compile(r"[0-9]{1,3}")
_COUPON_RE = re.compile(r"SAVE([0-9]{1,3})")


def parse_order(items_csv):
    """Parse 'name:qty,name:qty' into {name: qty}.

    Returns {} for non-string input or if ANY item is malformed
    (an order is never silently half-parsed).
    """
    if not isinstance(items_csv, str):
        return {}
    order = {}
    for item in items_csv.split(','):
        parts = item.split(':')
        if len(parts) != 2:
            return {}
        name, qty = parts[0].strip(), parts[1].strip()
        if not name or not _QTY_RE.fullmatch(qty):
            return {}
        qty = int(qty)
        if not 1 <= qty <= MAX_QTY:
            return {}
        order[name] = order.get(name, 0) + qty
    return order


def delivery_eta(distance_km):
    """ETA in minutes = 15 + 4 per km. Returns None for invalid distances."""
    if isinstance(distance_km, bool) or distance_km is None:
        return None
    try:
        km = float(distance_km)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(km) or km < 0 or km > 1000:
        return None
    return int(15 + km * 4)


def coupon_discount(code):
    """Return discount percent (0-100) for codes like 'SAVE50'; 0 if invalid."""
    if not isinstance(code, str):
        return 0
    match = _COUPON_RE.fullmatch(code.strip().upper())
    if not match:
        return 0
    value = int(match.group(1))
    return value if value <= MAX_DISCOUNT else 0


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter items as name:qty CSV (e.g. pizza:2,burger:1): ")
    result = parse_order(user_input)
    print("Order:", result if result else "Invalid order format")

    print("\n==== Running delivery_eta ====")
    user_input = input("Enter distance in km (e.g. 4.5): ")
    result = delivery_eta(user_input)
    print("ETA in Minutes:", result if result is not None else "Invalid distance")

    print("\n==== Running coupon_discount ====")
    user_input = input("Enter a coupon code (e.g. SAVE50): ")
    result = coupon_discount(user_input)
    print("Discount:", result)


if __name__ == "__main__":
    main()
