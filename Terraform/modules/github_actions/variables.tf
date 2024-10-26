variable "name_prefix" {
  type = string
}

variable "env" {
  type = string
}

variable "github_info" {
  type = object({
    username  = string
    repo_name = string
  })
}

variable "misskey_weather_bot" {
  type = object({
    ecr = object({
      main = object({
        arn = string
      })
    })
    lambda = object({
      main = object({
        arn = string
      })
    })
  })
}
