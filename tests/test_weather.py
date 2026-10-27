"""モックの例: 外部 API や現在時刻のように、テストのたびに結果が変わるものを差し替える。

CI では外部ネットワークに頼るテストは不安定（フレーキー）になりやすい。
依存を引数で受け取る形にしておくと、テストで偽物を渡せる。
"""

from datetime import datetime
from unittest.mock import Mock

import pytest

from ci_sample.weather import WeatherAPIError, greeting, weather_advice


def test_weather_advice_hot():
    client = Mock()
    client.get_temperature.return_value = 32.0

    assert weather_advice("東京", client) == "暑いので水分補給を"
    # 正しい引数で呼ばれたかも確かめられる
    client.get_temperature.assert_called_once_with("東京")


@pytest.mark.parametrize(
    ("temp", "expected"),
    [
        (30.0, "暑いので水分補給を"),
        (29.9, "過ごしやすい天気です"),
        (10.0, "過ごしやすい天気です"),
        (9.9, "寒いので上着を"),
    ],
)
def test_weather_advice_boundaries(temp, expected):
    client = Mock()
    client.get_temperature.return_value = temp
    assert weather_advice("大阪", client) == expected


def test_weather_advice_when_api_fails():
    client = Mock()
    # side_effect で「呼ぶと例外を出す」偽物にできる
    client.get_temperature.side_effect = ConnectionError("timeout")

    with pytest.raises(WeatherAPIError):
        weather_advice("札幌", client)


@pytest.mark.parametrize(
    ("hour", "expected"),
    [
        (5, "おはようございます"),
        (11, "おはようございます"),
        (12, "こんにちは"),
        (17, "こんにちは"),
        (18, "こんばんは"),
        (4, "こんばんは"),
    ],
)
def test_greeting_depends_on_time(hour, expected):
    # 現在時刻を引数で渡せるので、何時に CI が動いても結果が同じになる
    assert greeting(datetime(2026, 1, 1, hour, 0)) == expected
