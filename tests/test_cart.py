"""fixture と、状態を持つクラスのテストの例。"""

import pytest


def test_new_cart_is_empty(cart):
    assert cart.total() == 0
    assert cart.item_count() == 0


def test_total_sums_price_times_quantity(filled_cart):
    assert filled_cart.total() == 100 * 3 + 50 * 2


def test_adding_same_item_increases_quantity(cart):
    cart.add_item("りんご", price=100)
    cart.add_item("りんご", price=100, quantity=2)
    assert cart.item_count() == 3


def test_remove_item(filled_cart):
    filled_cart.remove_item("みかん")
    assert filled_cart.total() == 300


def test_remove_missing_item_raises(cart):
    with pytest.raises(KeyError):
        cart.remove_item("存在しない商品")


@pytest.mark.parametrize(("price", "quantity"), [(-1, 1), (100, 0), (100, -1)])
def test_add_item_rejects_invalid_values(cart, price, quantity):
    with pytest.raises(ValueError):
        cart.add_item("りんご", price=price, quantity=quantity)


def test_discount_is_applied_and_rounded_down(filled_cart):
    # 400 円の 15% 引き = 340 円
    assert filled_cart.total(discount_rate=0.15) == 340


def test_discount_rounds_down_fraction(cart):
    cart.add_item("ガム", price=99)
    # 99 * 0.9 = 89.1 → 端数切り捨てで 89
    assert cart.total(discount_rate=0.1) == 89


@pytest.mark.parametrize("rate", [-0.1, 1.1])
def test_invalid_discount_rate_raises(filled_cart, rate):
    with pytest.raises(ValueError):
        filled_cart.total(discount_rate=rate)
