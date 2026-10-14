provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "BookEase"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Capstone    = "Session21"
    }
  }
}
