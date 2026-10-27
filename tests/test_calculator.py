"""正常系・異常系・パラメータ化の例。"""

import pytest

from ci_sample.calculator import add, divide


# 正常系: 期待どおりの入力で、期待どおりの結果が返る
def test_add_returns_sum():
    assert add(2, 3) == 5


# パラメータ化: 同じテストを入力を変えて何度も回す
@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (1, 2, 3),
        (-1, -2, -3),  # 負の数
        (0, 0, 0),  # ゼロ
        (1.5, 2.5, 4.0),  # 小数
    ],
)
def test_add_various_inputs(a, b, expected):
    assert add(a, b) == expected


def test_divide_returns_quotient():
    assert divide(10, 4) == 2.5


# 浮動小数点は誤差が出るので、== ではなく pytest.approx で比べる
def test_divide_float_uses_approx():
    assert divide(1, 3) == pytest.approx(0.3333, rel=1e-3)


# 異常系: 不正な入力で、決めたとおりの例外が出る
def test_divide_by_zero_raises_value_error():
    with pytest.raises(ValueError, match="0 で割ることはできません"):
        divide(1, 0)
