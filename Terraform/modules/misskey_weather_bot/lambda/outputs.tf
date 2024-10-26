output "main" {
  value = {
    arn = aws_lambda_function.main.arn
    function_name=aws_lambda_function.main.function_name
  }
}
