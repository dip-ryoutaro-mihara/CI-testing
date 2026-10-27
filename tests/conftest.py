"""複数のテストファイルで共有する fixture を置く場所。"""

import pytest

from ci_sample.cart import ShoppingCart


@pytest.fixture
def cart():
    """テストごとに新しい空のカートを渡す（テスト同士が影響し合わないように）。"""
    return ShoppingCart()


@pytest.fixture
def filled_cart(cart):
    """fixture は別の fixture を使って組み立てられる。"""
    cart.add_item("りんご", price=100, quantity=3)
    cart.add_item("みかん", price=50, quantity=2)
    return cart
