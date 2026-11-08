from hypothesis import given, strategies as st
from food_delivery import parse_order, delivery_eta, coupon_discount

# Mixed inputs: text, None, numbers (the functions receive raw user input)
anything = st.one_of(st.text(), st.none(), st.integers(), st.floats())


@given(st.text() | st.none())
def test_parse_order_no_crash(s):
    try:
        parse_order(s)
    except Exception as e:
        assert False, f"parse_order crashed with: {e!r}"


@given(st.text() | st.none())
def test_delivery_eta_no_crash(s):
    try:
        delivery_eta(s)
    except Exception as e:
        assert False, f"delivery_eta crashed with: {e!r}"


@given(st.text() | st.none())
def test_coupon_discount_no_crash(s):
    try:
        coupon_discount(s)
    except Exception as e:
        assert False, f"coupon_discount crashed with: {e!r}"


# ---- Extra property checks: outputs must also be sane, not just crash-free ----

@given(anything)
def test_parse_order_output_is_valid(s):
    result = parse_order(s)
    assert isinstance(result, dict)
    for name, qty in result.items():
        assert isinstance(name, str) and name != ""
        assert isinstance(qty, int) and qty > 0


@given(anything)
def test_delivery_eta_output_is_valid(s):
    result = delivery_eta(s)
    assert result is None or (isinstance(result, int) and result >= 15)


@given(anything)
def test_coupon_discount_output_is_valid(s):
    result = coupon_discount(s)
    assert isinstance(result, int) and 0 <= result <= 100


# ---- Known-good inputs must still work after hardening ----

def test_valid_inputs_still_work():
    assert parse_order("pizza:2,burger:1") == {"pizza": 2, "burger": 1}
    assert delivery_eta("4.5") == 33
    assert coupon_discount("SAVE50") == 50
    assert coupon_discount("save20") == 20
