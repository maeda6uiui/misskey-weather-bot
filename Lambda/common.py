import pandas as pd
import requests
from logging import Logger

def get_weather_forecast(api_key:str,q:str,days:int,logger:Logger)->dict[str,pd.DataFrame]:
    """
    天気予報のデータを取得する

    Parameters
    ----------
    api_key: str
        Weather APIのAPIキー
    q: str
        クエリパラメータ
    days: int
        天気予報を取得する日数
    logger: Logger
        ロガー

    Returns
    ----------
    dict[str,DataFrame]
        daily: 1日ごとのデータ
        hourly: 1時間ごとのデータ
    """
    response=requests.get(
        "https://api.weatherapi.com/v1/forecast.json",
        headers={
            "key": api_key
        },
        params={
            "q": q,
            "days": days
        }
    )
    if response.status_code!=200:
        logger.error(f"Weather APIの実行に失敗しました: {response.status_code}")
        return None
    
    data=response.json()

    data_daily={
        "date": [],
        "maxtemp_c": [],
        "mintemp_c": [],
        "avgtemp_c": [],
        "condition": [],
        "sunrise": [],
        "sunset": []
    }
    data_hourly={
        "time": [],
        "temp_c": [],
        "condition": []
    }

    for forecastday in data["forecast"]["forecastday"]:
        #1日ごとのデータ
        date=forecastday["date"]
        maxtemp_c=forecastday["day"]["maxtemp_c"]
        mintemp_c=forecastday["day"]["mintemp_c"]
        avgtemp_c=forecastday["day"]["avgtemp_c"]
        condition=forecastday["day"]["condition"]["text"]
        sunrise=forecastday["astro"]["sunrise"]
        sunset=forecastday["astro"]["sunset"]

        data_daily["date"].append(date)
        data_daily["maxtemp_c"].append(maxtemp_c)
        data_daily["mintemp_c"].append(mintemp_c)
        data_daily["avgtemp_c"].append(avgtemp_c)
        data_daily["condition"].append(condition)
        data_daily["sunrise"].append(sunrise)
        data_daily["sunset"].append(sunset)

        #1時間ごとのデータ
        for hour in forecastday["hour"]:
            time=hour["time"]
            temp_c=hour["temp_c"]
            condition=hour["condition"]["text"]

            data_hourly["time"].append(time)
            data_hourly["temp_c"].append(temp_c)
            data_hourly["condition"].append(condition)

    df_daily=pd.DataFrame(data_daily)
    df_hourly=pd.DataFrame(data_hourly)

    return {
        "daily": df_daily,
        "hourly": df_hourly
    }
