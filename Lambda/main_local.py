import argparse
import yaml
from logging import getLogger,config

from common import get_weather_forecast

def main(args):
    #コマンドライン引数
    weather_api_key:str=args.weather_api_key
    forecast_query_param:str=args.forecast_query_param
    forecast_days:int=args.forecast_days
    
    #ロガーをセットアップする
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)

    logger=getLogger(__name__)
    logger.debug(args)

    #天気予報を取得する
    dfs=get_weather_forecast(weather_api_key,forecast_query_param,forecast_days,logger)
    
    logger.info(dfs["daily"])
    logger.info(dfs["hourly"])

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-k","--weather-api-key",type=str)
    parser.add_argument("-q","--forecast-query-param",type=str,default="Tokyo")
    parser.add_argument("-d","--forecast-days",type=int,default=1)
    args=parser.parse_args()

    main(args)
