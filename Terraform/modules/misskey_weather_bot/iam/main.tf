resource "aws_iam_role" "lambda" {
  name = "${var.name_prefix}-lambda-${var.env}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "allow_lambda_access_to_cloudwatch_logs" {
  name = "${var.name_prefix}-allow-lambda-access-to-cloudwatch-logs-${var.env}"
  policy = jsonencode({
    Version="2012-10-17"
    Statement=[
      {
        Effect="Allow"
        Action="logs:CreateLogGroup"
        Resource="arn:aws:logs:${var.aws.region}:${var.aws.account_id}:*"
      },
      {
        Effect="Allow"
        Action=[
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource="${var.cloudwatch_log_group_arn}:*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "allow_lambda_access_to_cloudwatch_logs" {
  role = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.allow_lambda_access_to_cloudwatch_logs.arn
}
