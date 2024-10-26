output "role" {
  value = {
    github_actions={
        name=aws_iam_role.github_actions.name
        arn=aws_iam_role.github_actions.arn
    }
  }
}
