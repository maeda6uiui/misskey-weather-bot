resource "aws_cloudwatch_log_group" "main" {
  name = "/aws/lambda/${var.name_prefix}-lambda-${var.env}"
}
