# misskey-weather-bot

## 概要

Misskeyに天気予報を投稿するbotを作成するコードです。

AWS Lambdaを定期実行し、[Weather API](https://www.weatherapi.com/)から取得した天気予報データをMisskeyに投稿します。
Lambdaやその他のAWSリソースはTerraformを用いて作成します。
LambdaのコードはPythonで作成し、DockerイメージをLambdaにデプロイします。
