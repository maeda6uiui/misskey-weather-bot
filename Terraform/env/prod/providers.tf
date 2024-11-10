terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~>4.0"
    }
  }

  backend "s3" {
    bucket = "misskey-weather-bot-tfstate"
    region = "ap-northeast-1"
    key    = "prod.tfstate"
  }

  required_version = "~>1.9"
}

provider "aws" {
  region = "ap-northeast-1"

  default_tags {
    tags = {
      Service   = local.service
      Env       = local.env
      ManagedBy = local.managed_by
    }
  }
}
