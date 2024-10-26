output "role" {
  value = {
    lambda={
        arn=aws_iam_role.lambda.arn
    }
  }
}