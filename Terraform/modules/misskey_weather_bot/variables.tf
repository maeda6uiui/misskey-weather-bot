variable "name_prefix" {
  type = string
}

variable "env" {
  type = string
}

variable "aws" {
  type = object({
    region = string
    account_id=string
  })
}

variable "lambda_config" {
  type = object({
    timeout = number
    memory_size=number
  })
}
