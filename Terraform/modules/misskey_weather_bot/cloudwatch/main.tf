resource "aws_cloudwatch_log_group" "main" {
  name = "${var.name_prefix}-lambda-${var.env}"
}
