variable "env" {
    description = "Environment to deploy to: dev, stage or prod."
    type = string

    validation {
        condition     = var.env == "dev" || var.env == "stage" || var.env == "prod"
        error_message = "The env value must be a valid string: dev, stage or prod."
    }
}

variable "username" {
    description = "The username for the postgre DB master user"
    type = string
    sensitive = true
}

variable "password" {
    description = "The password for the postgre DB master user"
    type = string
    sensitive = true
}
