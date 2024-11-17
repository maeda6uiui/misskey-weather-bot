data "http" "github_actions" {
  url = "https://token.actions.githubusercontent.com/.well-known/openid-configuration"
}

data "tls_certificate" "github_actions" {
  url = jsondecode(data.http.github_actions.response_body).jwks_uri
}

resource "aws_iam_openid_connect_provider" "github_actions" {
  url             = "https://token.actions.githubusercontent.com"
  client_id_list  = ["sts.amazonaws.com"]
  thumbprint_list = [data.tls_certificate.github_actions.certificates[0].sha1_fingerprint]
}

resource "aws_iam_role" "github_actions" {
  name = "${var.name_prefix}-github-actions-${var.env}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRoleWithWebIdentity"
        Principal = {
          Federated = aws_iam_openid_connect_provider.github_actions.arn
        }
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          }
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:${var.github_info.username}/${var.github_info.repo_name}:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_policy" "allow_github_actions_access_to_ecr" {
  name = "${var.name_prefix}-allow-github-actions-access-to-ecr-${var.env}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:UploadLayerPart",
          "ecr:PutImage",
          "ecr:InitiateLayerUpload",
          "ecr:CompleteLayerUpload",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
        Resource = var.misskey_weather_bot.ecr.main.arn
      },
      {
        Effect   = "Allow"
        Action   = "ecr:GetAuthorizationToken"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "allow_github_actions_access_to_lambda" {
  name = "${var.name_prefix}-allow-github-actions-access-to-lambda-${var.env}"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "lambda:UpdateFunctionCode"
        Resource = var.misskey_weather_bot.lambda.main.arn
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "allow_github_actions_access_to_ecr" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.allow_github_actions_access_to_ecr.arn
}

resource "aws_iam_role_policy_attachment" "allow_github_actions_access_to_lambda" {
  role       = aws_iam_role.github_actions.name
  policy_arn = aws_iam_policy.allow_github_actions_access_to_lambda.arn
}
