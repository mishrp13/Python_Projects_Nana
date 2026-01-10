variable "aws_region" {
  description = "Aws region to deploy resources"
  type = string
  default = "us-east-1"
}

variable "app_name" {

    description = "Elastic beanstalk app name"
    type = string
    default = "myapp-blue-green"
  
}

variable "instance_type" {
  
  description = "Ec2 instance type"
  type=string
  default = "t3.micro"

}

variable "solution_stack_name" {

    description = "Elastic Beanstalk solution stack"  
  
}

variable "tags" {

    description = "common tags"
    type=map(string)

     default = {
    Project     = "BlueGreenDeployment"
    Environment = "Demo"
    ManagedBy   = "Terraform"
  }
  
}
