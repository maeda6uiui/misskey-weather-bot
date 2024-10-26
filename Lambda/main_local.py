import argparse
import yaml
from logging import getLogger, config

from common import WeatherForecastPoster


def main(args):
    # コマンドライン引数
    weather_api_key: str = args.weather_api_key
    forecast_query_param: str = args.forecast_query_param
    misskey_server_url: str = args.misskey_server_url
    misskey_access_token: str = args.misskey_access_token

    # ロガーをセットアップする
    with open("./logging_config.yaml", "r", encoding="utf-8") as r:
        logging_config = yaml.safe_load(r)

    config.dictConfig(logging_config)
    logger = getLogger(__name__)

    # Misskeyに天気予報を投稿する
    wfp = WeatherForecastPoster(
        weather_api_key, misskey_server_url, misskey_access_token, logger=logger
    )
    try:
        wfp.post_weather_forecast(forecast_query_param, visibility="specified")
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-wk", "--weather-api-key", type=str)
    parser.add_argument("-q", "--forecast-query-param", type=str, default="Tokyo")
    parser.add_argument("-u", "--misskey-server-url", type=str)
    parser.add_argument("-mk", "--misskey-access-token", type=str)
    args = parser.parse_args()

    main(args)
