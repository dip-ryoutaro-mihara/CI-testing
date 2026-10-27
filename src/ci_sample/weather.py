"""外部 API と現在時刻に依存する処理のサンプル（モックの題材）。"""

from datetime import datetime
from typing import Protocol


class WeatherAPIError(Exception):
    """天気 API の呼び出しに失敗したことを表す。"""


class WeatherClient(Protocol):
    def get_temperature(self, city: str) -> float: ...


def weather_advice(city: str, client: WeatherClient) -> str:
    try:
        temp = client.get_temperature(city)
    except ConnectionError as e:
        raise WeatherAPIError(f"{city} の気温を取得できませんでした") from e

    if temp >= 30:
        return "暑いので水分補給を"
    if temp >= 10:
        return "過ごしやすい天気です"
    return "寒いので上着を"


def greeting(now: datetime | None = None) -> str:
    now = now or datetime.now()
    if 5 <= now.hour < 12:
        return "おはようございます"
    if 12 <= now.hour < 18:
        return "こんにちは"
    return "こんばんは"
