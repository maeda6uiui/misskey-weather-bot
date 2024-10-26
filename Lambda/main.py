import logging
import os
from logging import getLogger

from common import WeatherForecastPoster

WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
FORECAST_QUERY_PARAM = os.environ["FORECAST_QUERY_PARAM"]
MISSKEY_SERVER_URL = os.environ["MISSKEY_SERVER_URL"]
MISSKEY_ACCESS_TOKEN = os.environ["MISSKEY_ACCESS_TOKEN"]

logger = getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    # Misskeyに天気予報を投稿する
    wfp = WeatherForecastPoster(
        WEATHER_API_KEY, MISSKEY_SERVER_URL, MISSKEY_ACCESS_TOKEN, logger=logger
    )
    try:
        wfp.post_weather_forecast(FORECAST_QUERY_PARAM)
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {e}")
