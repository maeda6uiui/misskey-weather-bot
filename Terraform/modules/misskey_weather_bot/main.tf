module "ecr" {
  source = "./ecr"
  
  aws = var.aws
}

module "iam" {
  source = "./iam"

  name_prefix = var.name_prefix
  env = var.env
}

module "lambda" {
  source = "./lambda"

  name_prefix = var.name_prefix
  env = var.env

  lambda_config = var.lambda_config

  repository_url = module.ecr.main.repository_url
  lambda_role_arn = module.iam.role.lambda.arn
}