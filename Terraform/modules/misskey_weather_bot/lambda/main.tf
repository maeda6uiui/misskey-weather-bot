resource "aws_lambda_function" "main" {
  function_name = "${var.name_prefix}-lambda-${var.env}"

  role = var.lambda_role_arn

  #実際のイメージはGitHub Actionsでデプロイする
  package_type = "Image"
  image_uri    = "${var.repository_url}:temp"

  timeout     = var.lambda_config.timeout
  memory_size = var.lambda_config.memory_size
}
