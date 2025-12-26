Terraform data source (aws) — clear explanation

In Terraform, a data source is used to READ existing infrastructure — not create it.

Think of it as:

🔎 “Look up something that already exists in AWS so I can use it.”

🔹 What is a Terraform data source?
data "<PROVIDER>_<TYPE>" "<NAME>" {
  # filters / arguments
}


data → keyword meaning read-only

aws → provider

vpc / ami / subnet → resource type

<NAME> → local reference name

⚠️ Data sources do not create or modify anything.

🔹 Why data sources are needed

Terraform resources often need IDs of existing AWS objects:

Needed for	Example
EC2	AMI ID
Subnet	VPC ID
Security Group	VPC ID
Load Balancer	Subnet IDs

Instead of hardcoding IDs, data sources discover them dynamically.

🔹 Example 1: aws_ami (find latest Amazon Linux 2)
data "aws_ami" "linux2" {
  owners      = ["amazon"]
  most_recent = true

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

What Terraform does:

Calls AWS API

Finds matching AMIs

Picks the latest

Stores the AMI ID

How you use it:
ami = data.aws_ami.linux2.id

🔹 Example 2: aws_vpc (read existing VPC)
data "aws_vpc" "main" {
  default = true
}


Terraform:

Searches AWS

Returns the default VPC

Makes its attributes available

Usage:

vpc_id = data.aws_vpc.main.id

🔹 Example 3: aws_subnet (find subnet in VPC)
data "aws_subnet" "one" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}


Usage:

subnet_id = data.aws_subnet.one.id

🔹 Data source vs Resource (IMPORTANT)
Feature	data	resource
Creates infrastructure	❌	✅
Reads existing infra	✅	❌
Changes infra	❌	✅
Stored in state	✅ (read-only)	✅ (managed)
🔹 When to use data sources

✅ Use data sources when:

Infra already exists

Using default VPC/subnets

Sharing infra across teams

Reading AMIs, AZs, IAM roles

❌ Don’t use data sources when:

You want Terraform to manage lifecycle

You plan to create & destroy resources

🔹 Common AWS data sources
Data source	Purpose
aws_ami	Find AMI
aws_vpc	Get VPC
aws_subnet	Get subnet
aws_security_group	Get SG
aws_availability_zones	List AZs
aws_iam_role	Read IAM role
🔹 Common mistakes (you just hit these)

❌ Wrong tag key:

tag:name   ❌
tag:Name   ✅


❌ Referencing object instead of attribute:

subnet_id = data.aws_subnet.shared      ❌
subnet_id = data.aws_subnet.shared.id   ✅


❌ Over-filtering → “no matching found”

🔹 Mental model (remember this)

Resources build. Data sources look up.

┌──────────────────────┐
│   terraform plan     │
└─────────┬────────────┘
          │
          ▼
┌──────────────────────┐
│  Provider (AWS)      │
│  Authentication      │
└─────────┬────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│            DATA SOURCES (READ)              │
│                                            │
│  data.aws_vpc        ──► get VPC ID         │
│  data.aws_subnet     ──► get Subnet ID      │
│  data.aws_ami        ──► get AMI ID         │
│                                            │
│  ❌ No creation                              │
│  ❌ No modification                          │
│  ✅ Read-only                                │
└─────────┬──────────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│            TERRAFORM GRAPH                 │
│  (dependency resolution using references) │
└─────────┬──────────────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────┐
│            RESOURCES (CREATE)               │
│                                            │
│  aws_instance                               │
│    ├─ uses AMI ID                           │
│    ├─ uses Subnet ID                        │
│    └─ uses VPC ID                           │
│                                            │
│  ✅ Create / Update / Delete                │
└─────────┬──────────────────────────────────┘
          │
          ▼
┌──────────────────────┐
│   terraform apply    │
└──────────────────────┘
