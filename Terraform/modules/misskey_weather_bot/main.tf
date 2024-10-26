module "ecr" {
  source = "./ecr"

  aws = var.aws
}

module "cloudwatch" {
  source = "./cloudwatch"

  name_prefix = var.name_prefix
  env = var.env
}

module "iam" {
  source = "./iam"

  name_prefix = var.name_prefix
  env         = var.env
  aws = var.aws

  cloudwatch_log_group_arn = module.cloudwatch.log_group.main.arn
}

module "lambda" {
  source = "./lambda"

  name_prefix = var.name_prefix
  env         = var.env

  lambda_config = var.lambda_config

  repository_url  = module.ecr.main.repository_url
  lambda_role_arn = module.iam.role.lambda.arn
}