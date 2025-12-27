
variable "environment" {

    default = "dev"
    type = string
  
}


variable "region" {
    type = string
    default = "us-east-1"
  
}

variable "instance_count" {

    description = "Number of EC2 instances"
    type=number
    
  
}

variable "monitoring_enables" {

    description = "Enable detailed monitoring for Ec2 instances"
    type = bool
    default = true
  
}

variable "associate_public_ip" {
    description = "Associate public ip address with EC2 instance"
    type = bool
    default = true
  
}

variable "cidr_block" {

    description = "CIDR block for the vpc"
    type= list(string)
    default = ["10.0.0.0/8","192.168.0.0/16","172.16.0.0/12"]
  
}

variable "allowed_vm_types" {

    description = "List of allowed vm types"
    type=list(string)
    default = [ "t2.micro", "t2.small", "t3.micro", "t3.small" ]
  
}

variable "allowed_region" {

    description = "List of allowed aws regions"
    type = set(string)
    default = [ "us-east-1", "us-west-2", "eu-west-1", "eu-west-1" ]
  
}

variable "tags" {

    type = map(string)
    default = {
        Environment = "dev"
        Name = "dev-Instance"
        created_by = "terraform"
        compliance= "yes"
    
    }   
  
}

variable "ingress_value" {

    type= tuple([ number, string, number ])
    default = [ 443, "tcp", 443 ]
  
}

variable "config" {

    type = object({
      region = string,
      monitoring = bool,
      instance_count=number
    })

    default = {
      region = "us-east-1",
      monitoring = true
      instance_count = 1
    }
  
}

variable "bucket_names" {

   description = "List of s3 bucket names to create"
   type= list(string)
   default = [ "my-unique-bucket-dayx08-1234561", "my-unique-bucket-dayx08-1234562" ]
  
}


variable "bucket_name_set" {

   description = "List of s3 bucket names to create"
   type= set(string)
   default = [ "my-unique-bucket-dayx08-1234560", "my-unique-bucket-dayx08-1234569" ]
  
}


variable "ingress_rules" {
  description = "List of ingress rules for security group"
  type = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
    description = string
  }))
  default = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP"
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS"
    }
  ]
}


variable "bucket_name" {

  default = "techtutorialwithprabal-101"
  
}