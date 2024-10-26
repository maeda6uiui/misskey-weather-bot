resource "aws_ecr_repository" "main" {
  name = "lambda/misskey-weather-bot"
  image_tag_mutability = "IMMUTABLE"
}
