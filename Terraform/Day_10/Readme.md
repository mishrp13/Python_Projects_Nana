Conditional Expression in Terraform
What it is

A conditional expression lets you choose a value based on a condition (similar to if-else).
It is often used in AWS to control resource configuration, enable/disable features, or switch between environments.

Syntax
condition ? true_value : false_value

AWS Example 1: Enable public IP only in dev
variable "environment" {
  default = "dev"
}

resource "aws_instance" "example" {
  ami           = "ami-0abcdef123"
  instance_type = "t2.micro"

  associate_public_ip_address = var.environment == "dev" ? true : false
}


🔹 Explanation

In dev, EC2 gets a public IP

In prod, it does not

AWS Example 2: Choose instance type by environment
instance_type = var.environment == "prod" ? "t3.large" : "t3.micro"

Common AWS Use Cases

✔ Environment-based configuration
✔ Optional features (monitoring, encryption, public access)
✔ Cost optimization

2. Splat Expression in Terraform
What it is

A splat expression is used to extract attributes from multiple resources or lists.

Think of it as:
👉 “Give me this attribute from all resources”

Syntax
resource_type.resource_name[*].attribute

AWS Example 1: Multiple EC2 instances → get all IDs
resource "aws_instance" "web" {
  count         = 3
  ami           = "ami-0abcdef123"
  instance_type = "t2.micro"
}

output "instance_ids" {
  value = aws_instance.web[*].id
}


🔹 Output:

["i-123", "i-456", "i-789"]

AWS Example 2: Get private IPs for an ALB target group
output "private_ips" {
  value = aws_instance.web[*].private_ip
}

AWS Example 3: Splat with modules
module "vpc" {
  source = "./vpc"
  count  = 2
}

output "vpc_ids" {
  value = module.vpc[*].vpc_id
}

When to use splat expressions

✔ count or for_each resources
✔ Outputs
✔ Passing lists to AWS resources (ALB, ASG, Security Groups)

3. Dynamic Block in Terraform
What it is

A dynamic block allows you to generate repeated nested blocks dynamically.

In AWS, many resources have repeatable nested blocks, such as:

ingress / egress in security groups

listener rules

tags

ebs_block_device

Syntax
dynamic "block_name" {
  for_each = collection
  content {
    # block content
  }
}

AWS Example 1: Dynamic security group rules
variable "ingress_rules" {
  default = [
    { port = 80, cidr = "0.0.0.0/0" },
    { port = 443, cidr = "0.0.0.0/0" }
  ]
}

resource "aws_security_group" "web_sg" {
  name = "web-sg"

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = [ingress.value.cidr]
    }
  }
}


🔹 Terraform creates two ingress rules automatically.

AWS Example 2: Dynamic EBS volumes for EC2
variable "volumes" {
  default = [
    { device = "/dev/sdb", size = 50 },
    { device = "/dev/sdc", size = 100 }
  ]
}

resource "aws_instance" "example" {
  ami           = "ami-0abcdef123"
  instance_type = "t2.micro"

  dynamic "ebs_block_device" {
    for_each = var.volumes
    content {
      device_name = ebs_block_device.value.device
      volume_size = ebs_block_device.value.size
    }
  }
}

When to use dynamic blocks

✔ When AWS resource has repeated nested blocks
✔ When rules/blocks depend on variables
✔ To avoid copy-paste code

| Feature                | Purpose                                | Common AWS Usage                   |
| ---------------------- | -------------------------------------- | ---------------------------------- |
| Conditional Expression | Choose values dynamically              | Env-based instance type, public IP |
| Splat Expression       | Extract attributes from many resources | EC2 IDs, IPs, subnet IDs           |
| Dynamic Block          | Generate nested blocks dynamically     | SG rules, EBS volumes, listeners   |
