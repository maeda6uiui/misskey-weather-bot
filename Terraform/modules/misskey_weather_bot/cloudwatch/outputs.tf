output "log_group" {
  value={
    main={
        arn=aws_cloudwatch_log_group.main.arn
    }
  }
}
