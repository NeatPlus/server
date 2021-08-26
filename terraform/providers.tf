# Install required providers
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.55.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.1.0"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.7.2"
    }
  }

  required_version = "~> 1.0.4"
}

# Configure AWS provider
provider "aws" {
  region = var.region
}
