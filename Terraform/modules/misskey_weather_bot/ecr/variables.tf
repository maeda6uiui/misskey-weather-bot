variable "aws" {
  type = object({
    region = string
    account_id=string
  })
}
