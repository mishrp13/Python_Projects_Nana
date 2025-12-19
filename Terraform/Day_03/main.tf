terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
      # That means am locking the major version of the provider and allowed the changes with minor version
      # such as 6.1 or 6.2 but not 7.0
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}


# create s3 bucket

resource "aws_s3_bucket" "first_bucket" {
  bucket = "techtutorialswithprabal-bucket-12345"

  tags = {
    Name        = "My bucket"
    Environment = "Dev"
  }
  
}