import os
import yaml
from logging import getLogger,config
from pathlib import Path

from common import WeatherForecastPoster

WEATHER_API_KEY=os.environ["WEATHER_API_KEY"]
FORECAST_QUERY_PARAM=os.environ["FORECAST_QUERY_PARAM"]
MISSKEY_SERVER_URL=os.environ["MISSKEY_SERVER_URL"]
MISSKEY_ACCESS_TOKEN=os.environ["MISSKEY_ACCESS_TOKEN"]

def lambda_handler():
    #ログファイルを保存するディレクトリを作成する
    logging_dir=Path("./Log")
    logging_dir.mkdir(exist_ok=True)
    
    #ロガーをセットアップする
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)
    logger=getLogger(__name__)

    #Misskeyに天気予報を投稿する
    wfp=WeatherForecastPoster(WEATHER_API_KEY,MISSKEY_SERVER_URL,MISSKEY_ACCESS_TOKEN,logger=logger)
    try:
        wfp.post_weather_forecast(FORECAST_QUERY_PARAM,visibility="specified")
    except Exception as e:
        logger.error(f"処理中にエラーが発生しました: {e}")
