terraform {
  required_providers {
    aws={
        source = "hashicorp/aws"
        version ="~> 5.0"
    }
  }

  required_version = ">=1.0"
}

provider "aws" {

    region = var.aws_region
  
}

# IAM ROLE FOR EC2 (Elastic Beanstalk Instances)
# ONLY EC2 instances can use this role

#❗ If this was wrong → EB environment would fail to launch

resource "aws_iam_role" "eb_ec2_role" {
    name= "${var.app_name}-eb-ec2-role"
    assume_role_policy = jsonencode({
        version= "2012-10-17"

        Statement = [
            {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Principal ={
                Service = "ec2.amazonaws.com"
            }

            }
        
        ]
    })

    tags= var.tags

}


# Attach AWS Managed Policies to EC2 Role

#These give permissions to the EC2 instances.

resource "aws_iam_role_policy_attachment" "eb_web_tier" {
  
  role = aws_iam_role.eb_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier"
  # Permission to: write logs, talk to ELB, basic web app needs

}

resource "aws_iam_role_policy_attachment" "eb_service_managed_updates" {
    role = aws_iam_role.eb_service_role.name
    policy_arn = "arn:aws:iam::aws:policy/AWSElasticBeanstalkManagedUpdatesCustomerRolePolicy"
  
}


resource "aws_elastic_beanstalk_application" "app" {

    name=var.app_name
    description = "Blue-green Deployment Demo Application"
    tags=var.tags

}

resource "aws_s3_bucket_public_access_block" "app_versions" {

  bucket = aws_s3_bucket.app_versions.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

data "aws_caller_identity" "current" {}







