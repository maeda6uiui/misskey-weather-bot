resource "aws_ecr_repository" "main" {
  name                 = "lambda/misskey-weather-bot"
  image_tag_mutability = "IMMUTABLE"
}

resource "terraform_data" "main" {
  triggers_replace = [
    aws_ecr_repository.main.arn
  ]

  provisioner "local-exec" {
    command = "bash ${path.module}/push_temp_image.sh"
    environment = {
      AWS_REGION     = var.aws.region
      AWS_ACCOUNT_ID = var.aws.account_id
      REPOSITORY_URL = aws_ecr_repository.main.repository_url
    }
  }
}
