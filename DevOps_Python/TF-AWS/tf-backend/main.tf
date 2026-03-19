terraform {
  required_providers {
    aws ={
        source = "hashicorp/aws"
        version = "5.54.1"
    }
  }

  backend "s3" {
    bucket="demo-bucket"
    key="backend.tfstate"
    region="eu-east-1"
  }
}



provider "aws" {
  region = "eu-east-1"
}


resource "aws_instance" "myserver" {
  ami = ""
  instance_type = "t2.micro"

  tags={
    Name= "SampleServer"
  }
}


