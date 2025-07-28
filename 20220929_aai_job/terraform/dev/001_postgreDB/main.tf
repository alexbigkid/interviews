locals {
  env    = "dev"
  region = "us-west-1"
}

variable "user" {
    type = string
    sensitive = true
}

variable "pswd" {
    type = string
    sensitive = true
}

terraform {
  backend "s3" {
    bucket = "aai-terraform-state-do-not-delete"
    key    = "dev/001_postgreDB/terraform.tfstate"
    region = "us-west-1"

    dynamodb_table = "aai-terraform-lock"
    encrypt        = true
  }
}

provider "aws" {
  region = local.region
}

module "postgreDB" {
  source   = "../../templates/postgreDB"
  env      = local.env
  username = var.user
  password = var.pswd
}
