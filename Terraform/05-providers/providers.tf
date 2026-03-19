terraform {
  required_version = "~>1.7"
  required_providers {
    aws={
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-1"
}

provider "aws" {
  region = "us-east-1"
  alias = "us-east"
}

resource "aws_s3_bucket" "eu_west_1" {
  bucket= "some-random-bucket-name-aoshjja"
}

resource "aws_s3_bucket" "us_east_1" {
 bucket="some-randome-bucket-2231343"
 provider=aws.us-east  
}

# if we are not providing alias then that alias will be considered as default one