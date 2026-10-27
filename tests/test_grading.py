"""境界値テストの例。

境界値分析: 条件が切り替わる値（79 と 80 など）の両側を必ずテストする。
バグは「以上」と「より大きい」の取り違えのように、境目で起きやすい。
"""

import pytest

from ci_sample.grading import grade


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (100, "A"),  # 上限
        (80, "A"),  # A の下限
        (79, "B"),  # A の下限 - 1
        (60, "B"),
        (59, "C"),
        (40, "C"),
        (39, "D"),
        (0, "D"),  # 下限
    ],
)
def test_grade_boundaries(score, expected):
    assert grade(score) == expected


# 範囲外は境界のすぐ外側（-1 と 101）を確かめる
@pytest.mark.parametrize("score", [-1, 101])
def test_grade_out_of_range_raises(score):
    with pytest.raises(ValueError):
        grade(score)


# 型が違う入力も異常系として確かめる
@pytest.mark.parametrize("score", ["80", None, 80.5, True])
def test_grade_rejects_non_int(score):
    with pytest.raises(TypeError):
        grade(score)
