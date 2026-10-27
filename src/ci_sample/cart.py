"""買い物かごのサンプル（状態を持つクラスのテストの題材）。"""

import math


class ShoppingCart:
    def __init__(self) -> None:
        # 商品名 -> (単価, 個数)
        self._items: dict[str, tuple[int, int]] = {}

    def add_item(self, name: str, price: int, quantity: int = 1) -> None:
        if price < 0:
            raise ValueError("price は 0 以上で指定してください")
        if quantity <= 0:
            raise ValueError("quantity は 1 以上で指定してください")
        _, current = self._items.get(name, (price, 0))
        self._items[name] = (price, current + quantity)

    def remove_item(self, name: str) -> None:
        if name not in self._items:
            raise KeyError(name)
        del self._items[name]

    def item_count(self) -> int:
        return sum(quantity for _, quantity in self._items.values())

    def total(self, discount_rate: float = 0.0) -> int:
        if not 0 <= discount_rate <= 1:
            raise ValueError("discount_rate は 0〜1 で指定してください")
        subtotal = sum(price * quantity for price, quantity in self._items.values())
        # 浮動小数点の誤差で 1 円ずれないよう、丸めてから切り捨てる
        return math.floor(round(subtotal * (1 - discount_rate), 6))
