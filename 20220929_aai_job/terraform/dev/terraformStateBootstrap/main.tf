locals {
  env     = "dev"
  region  = "us-west-1"
  profile = "gh_pipeline"
}

provider "aws" {
  region  = local.region
  profile = local.profile
}

module "terraformStateBootstrap" {
  source = "../../templates/terraformStateBootstrap"
  env    = local.env
}
