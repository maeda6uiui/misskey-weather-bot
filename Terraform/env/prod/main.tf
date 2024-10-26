module "account_info" {
  source = "../../modules/account_info"
}

module "misskey_weather_bot" {
  source = "../../modules/misskey_weather_bot"

  name_prefix = local.service
  env         = local.env
  aws         = module.account_info.aws

  lambda_config = {
    timeout     = 15
    memory_size = 128
  }
}

module "github_actions" {
  source = "../../modules/github_actions"

  name_prefix = local.service
  env         = local.env

  misskey_weather_bot = module.misskey_weather_bot

  github_info = {
    username  = "maeda6uiui"
    repo_name = "misskey-weather-bot"
  }
}
