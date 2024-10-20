import pandas as pd
import requests
from logging import getLogger,Logger
from misskey import Misskey

class WeatherForecastPoster(object):
    """
    天気予報をMisskeyに投稿するクラス
    """
    def __init__(
        self,
        weather_api_key:str,
        misskey_server_url:str,
        misskey_access_token:str,
        logger:Logger=None):
        """
        Parameters
        ----------
        weather_api_key: str
            Weather APIのAPIキー
        misskey_server_url: str
            MisskeyサーバーのURL
        misskey_access_token: str
            Misskeyのアクセストークン
        logger (optional): Logger
            ロガー
        """
        self._weather_api_key=weather_api_key
        self._mk=Misskey(address=misskey_server_url,i=misskey_access_token)

        if logger is not None:
            self._logger=logger
        else:
            self._logger=getLogger(__name__)

    def _get_weather_forecast(self,q:str,days:int)->dict[str,pd.DataFrame]:
        """
        天気予報のデータを取得する

        Parameters
        ----------
        q: str
            クエリパラメータ
        days: int
            天気予報を取得する日数

        Returns
        ----------
        dict[str,DataFrame]
            location: 位置データ
            daily: 1日ごとの天気予報データ
            hourly: 1時間ごとの天気予報データ
        """
        response=requests.get(
            "https://api.weatherapi.com/v1/forecast.json",
            headers={
                "key": self._weather_api_key
            },
            params={
                "q": q,
                "days": days,
                "lang": "ja"
            }
        )
        if response.status_code!=200:
            raise RuntimeError(f"Weather APIの実行に失敗しました: {response.status_code}")
        
        data=response.json()

        location=data["location"]
        data_location={
            "name": [location["name"]],
            "region": [location["region"]],
            "country": [location["country"]]
        }
        df_location=pd.DataFrame(data_location)

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
            "location": df_location,
            "daily": df_daily,
            "hourly": df_hourly
        }
    
    def _create_misskey_note(self,text:str,visibility:str)->str:
        """
        Misskeyにノートを作成する

        Parameters
        ----------
        text: str
            ノートの内容
        visibility: str
            ノートの公開範囲

        Returns
        ----------
        str
            ノートのID
        """
        note=self._mk.notes_create(text=text,visibility=visibility)
        note_id=note["createdNote"]["id"]

        return note_id
    
    def _get_condition_emoji(self,condition:str)->str:
        """
        天気を表す絵文字を返す

        Parameters
        ----------
        condition: str
            天気を表す文字列

        Returns
        ----------
        str
            天気を表す絵文字
        """
        if "晴" in condition:
           return "☀"
        elif "曇" in condition:
            return "☁"
        elif "雨" in condition:
            return "☂"
        elif "雪" in condition:
            return "❄"
        
        return ""
    
    def post_weather_forecast(self,q:str,visibility:str="public"):
        """
        天気予報をMisskeyに投稿する

        Parameters
        ----------
        q: str
            Weather APIを実行するときのクエリパラメータ
        visibility: str
            ノートの公開範囲
        """
        dfs=self._get_weather_forecast(q,1)

        df_location=dfs["location"]
        df_daily=dfs["daily"]
        df_hourly=dfs["hourly"]

        self._logger.debug(df_location)
        self._logger.debug(df_daily)
        self._logger.debug(df_hourly)

        location_name=df_location["name"].item()

        date=df_daily["date"].item()
        condition=df_daily["condition"].item()
        avgtemp_c=df_daily["avgtemp_c"].item()
        mintemp_c=df_daily["mintemp_c"].item()
        maxtemp_c=df_daily["maxtemp_c"].item()

        text=(
            f"{date}の{location_name}の天気予報\n\n"
            f"{self._get_condition_emoji(condition)+condition}\n"
            f"{avgtemp_c}℃ (平均) / {mintemp_c}℃ (最低) / {maxtemp_c}℃ (最高)"
        )
        note_id=self._create_misskey_note(text,visibility)
        self._logger.info(f"ノートID (1日ごとの天気予報): {note_id}")

        text=f"{date}の{location_name}の天気予報(1時間ごと)\n\n"
        for _,row in df_hourly.iterrows():
            time:str=row["time"]
            time=time.split(" ")[1]

            temp_c=row["temp_c"]
            condition=row["condition"]

            text+=f"{time} / {temp_c}℃ / {self._get_condition_emoji(condition)+condition}\n"

        note_id=self._create_misskey_note(text,visibility)
        self._logger.info(f"ノートID (1時間ごとの天気予報): {note_id}")
