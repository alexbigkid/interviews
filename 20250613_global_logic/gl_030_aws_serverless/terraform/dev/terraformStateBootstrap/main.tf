locals {
  env     = "dev"
  region  = "us-west-2"
  profile = "dev"
}

provider "aws" {
  region  = local.region
  profile = local.profile
}

module "terraformStateBootstrap" {
  source = "../../templates/terraformStateBootstrap"
  env    = local.env
}
