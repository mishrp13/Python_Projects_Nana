variable "aws_region" {
  description = "Aws region for resources"
  type = string
  default = "us-east-1"
}

variable "environment" {
  description = "Environment name(dev, staging, prod)"
  type = string
  default = "dev"
}

variable "bucket_names" {
  description = "Set of S3 bucket names to create"
  type=set(string)
  default = ["demo-lifecycle-bucket-001", "demo-lifecycle-bucket-002"]
}

variable "allowed_regions" {
  description = "List of allowed aws regions"
  type= list(string)
  default = [ "us-east-1", "us-west-2", "eu-west-1", "ap-south-1" ]
}

variable "instance_type" {
  description = "EC2 instance type"
  type = string
  default = "lifecycle-demo-instance"
}

variable "instance_name" {
  description = "Name tag for EC2 instance"
  type= string
  default = "lifecycle-demo-instance"
}

variable "db_username" {
  description = "Database administrator username"
  type = string
  default = "admin"
  sensitive = true
}

variable "db_password" {
  description = "Database administrator password"
  type= string
  default = "change123!"
  sensitive = true
}

variable "db_name" {
  description = "Initial databse name"
  type = string
  default = "myappdb"
}

variable "resource_tags" {
  description = "common tags to apply to resources"
  type= map(string)
  default = {
     Environment = "dev"
     Team = "DevOps"
     CostCenter= "Engineering"
  }
}












