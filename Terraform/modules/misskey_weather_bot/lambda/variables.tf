variable "name_prefix" {
  type = string
}

variable "env" {
  type = string
}

variable "lambda_config" {
  type = object({
    timeout     = number
    memory_size = number
  })
}

variable "lambda_role_arn" {
  type = string
}

variable "repository_url" {
  type = string
}
