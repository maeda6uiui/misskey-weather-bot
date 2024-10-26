resource "aws_cloudwatch_event_rule" "lambda_schedule" {
  name                = "${var.name_prefix}-lambda-schedule"
  schedule_expression = var.schedule_expression
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.lambda_schedule.name
  arn  = var.lambda_arn
}

resource "aws_lambda_permission" "allow_eventbridge_invoke_lambda" {
  function_name = var.lambda_name
  action        = "lambda:InvokeFunction"
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.lambda_schedule.arn
}
