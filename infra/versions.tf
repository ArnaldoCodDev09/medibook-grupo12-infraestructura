terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.0, < 7.0"
    }
  }

  backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "MediBook"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Course      = "Infraestructura como Codigo"
    }
  }
}

