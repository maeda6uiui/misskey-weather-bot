import argparse
import yaml
from logging import getLogger,config
from pathlib import Path

from common import get_weather_forecast,create_misskey_note

def main(args):
    #コマンドライン引数
    weather_api_key:str=args.weather_api_key
    forecast_query_param:str=args.forecast_query_param
    forecast_days:int=args.forecast_days
    forecast_language:str=args.forecast_language
    misskey_server_url:str=args.misskey_server_url
    misskey_access_token:str=args.misskey_access_token

    #ログファイルを保存するディレクトリを作成する
    logging_dir=Path("./Log")
    logging_dir.mkdir(exist_ok=True)
    
    #ロガーをセットアップする
    with open("./logging_config.yaml","r",encoding="utf-8") as r:
        logging_config=yaml.safe_load(r)
    
    config.dictConfig(logging_config)
    logger=getLogger(__name__)

    #天気予報を取得する
    dfs=get_weather_forecast(weather_api_key,forecast_query_param,forecast_days,forecast_language,logger)
    if dfs is None:
        logger.error("天気予報の取得に失敗しました")
        return

    df_location=dfs["location"]
    df_daily=dfs["daily"]
    df_hourly=dfs["hourly"]
    
    logger.debug(df_daily)
    logger.debug(df_hourly)

    #天気予報をMisskeyに投稿する
    location_name=df_location["name"].item()

    date=df_daily["date"].item()
    condition=df_daily["condition"].item()
    avgtemp_c=df_daily["avgtemp_c"].item()
    mintemp_c=df_daily["mintemp_c"].item()
    maxtemp_c=df_daily["maxtemp_c"].item()

    text=(
        f"{date}の{location_name}の天気予報\n\n"
        f"{condition}\n"
        f"{avgtemp_c}℃ (平均) / {mintemp_c}℃ (最低) / {maxtemp_c}℃ (最高)"
    )
    note_id=create_misskey_note(misskey_server_url,misskey_access_token,text,"specified",logger)
    logger.info(f"ノートのID (1日): {note_id}")

    text=f"{date}の{location_name}の天気予報(1時間ごと)\n\n"
    for _,row in df_hourly.iterrows():
        time:str=row["time"]
        time=time.split(" ")[1]

        temp_c=row["temp_c"]
        condition=row["condition"]

        text+=f"{time} / {temp_c}℃ / {condition}\n"

    note_id=create_misskey_note(misskey_server_url,misskey_access_token,text,"specified",logger)
    logger.info(f"ノートのID (1時間ごと): {note_id}")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-wk","--weather-api-key",type=str)
    parser.add_argument("-q","--forecast-query-param",type=str,default="Tokyo")
    parser.add_argument("-d","--forecast-days",type=int,default=1)
    parser.add_argument("-l","--forecast-language",type=str,default="ja")
    parser.add_argument("-u","--misskey-server-url",type=str)
    parser.add_argument("-mk","--misskey-access-token",type=str)
    args=parser.parse_args()

    main(args)
