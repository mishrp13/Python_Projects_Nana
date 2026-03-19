terraform {
  required_providers {
    aws={
        source = "hashicorp/aws"
        version = "5.55.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}


data "aws_ami" "name" {
  most_recent = true
  owners = ["amazon"]
}

output "aws_ami" {
  value = data.aws_ami.name.id
}

output "security_group" {
  value = data.aws_security_group.name.id
}

data "aws_security_group" "name" {
  tags={
    name= "MySG"
    ENV= "PROD"
  }
}

data "aws_vpc" "name" {
  tags={
    ENV= "PROD"
    Name="my-vpc"
  }
}

output "vpc_id" {
  value = data.aws_vpc.name.id
}

data "aws_availability_zones" "names" {
  state= "available"
}

output "aws_zones" {
  value = data.aws_availability_zones.names
}

data "aws_caller_identity" "name" {
  
}

output "caller_info" {
  value = data.aws_caller_identity.name
}

output "region_name" {
  value = data.aws_region.name
}

data "aws_subnet" "name" {
  filter{
      name="vpc-id"
      values= [data.data.aws_vpc.name.id]
      }

      tags={
        Name= "private-subnet"
      }

}
resource "aws_instance" "myserver" {
  ami= data.aws_ami.name.id
  instance_type = "t2.micro"
  subnet_id = data.aws_subnet.name.id
  security_groups = [data.aws_security_group_name.id]

  tags={
    Name="SampleServer"
  }
}