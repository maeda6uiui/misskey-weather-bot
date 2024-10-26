resource "aws_iam_role" "lambda" {
  name = "${var.name_prefix}-lambda-${var.env}"
  assume_role_policy = jsonencode({
    Version="2012-10-17"
    Statement=[
        {
            Effect="Allow"
            Action="sts:AssumeRole"
            Principal={
                Service="lambda.amazonaws.com"
            }
        }
    ]
  })
}
