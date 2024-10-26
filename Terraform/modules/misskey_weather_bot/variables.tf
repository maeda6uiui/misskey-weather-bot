variable "name_prefix" {
  type = string
}

variable "env" {
  type = string
}

variable "lambda_config" {
  type = object({
    timeout = number
    memory_size=number
  })
}
