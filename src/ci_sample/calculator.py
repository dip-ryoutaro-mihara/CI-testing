"""四則演算のサンプル。"""


def add(a: float, b: float) -> float:
    return a + b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("0 で割ることはできません")
    return a / b
