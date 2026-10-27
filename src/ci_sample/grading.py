"""点数から評価を決めるサンプル（境界値テストの題材）。"""


def grade(score: int) -> str:
    # bool は int のサブクラスなので、明示的に弾く
    if not isinstance(score, int) or isinstance(score, bool):
        raise TypeError("score は整数で指定してください")
    if not 0 <= score <= 100:
        raise ValueError("score は 0〜100 で指定してください")

    if score > 80:
        return "A"
    if score >= 60:
        return "B"
    if score >= 40:
        return "C"
    return "D"
