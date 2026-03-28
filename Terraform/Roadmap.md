Week 1 — Terraform Core Fundamentals (Days 1-7)
Day 1 — Terraform Basics

What is IaC and why Terraform
Install Terraform + AWS CLI setup
Understand HCL syntax — blocks, arguments, expressions
Practice:

hcl# Write your first provider block
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}
provider "aws" {
  region = "us-east-1"
}
Day 2 — Resources & Data Sources

resource block deep dive
data block — read existing AWS resources
Resource dependencies — implicit vs explicit
Practice:

hcl# Create EC2 using data source for AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-*-22.04-amd64-server-*"]
  }
}
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro"
}
Day 3 — Variables & Outputs

variable block — types, defaults, validation
output block — exposing values
locals block — computed values
terraform.tfvars and *.auto.tfvars
Practice:

hclvariable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "EC2 instance type"
  validation {
    condition     = contains(["t2.micro", "t2.small"], var.instance_type)
    error_message = "Must be t2.micro or t2.small"
  }
}
Day 4 — State Management

What is terraform.tfstate
Why state is critical — never edit manually
terraform state list
terraform state show
terraform state mv
terraform state rm
Remote state — S3 backend with DynamoDB locking
Practice:

hclterraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
Day 5 — Terraform CLI Commands

terraform init
terraform plan
terraform apply
terraform destroy
terraform fmt
terraform validate
terraform output
terraform refresh
terraform import
Practice all commands on real AWS resources

Day 6 — Modules

What are modules and why use them
Creating reusable modules
Module inputs and outputs
Calling modules
Practice:

hcl# Create a reusable EC2 module
module "web_server" {
  source        = "./modules/ec2"
  instance_type = "t2.micro"
  environment   = "prod"
  name          = "web-server"
}
Day 7 — Revision + Mini Project

Create complete VPC with:

VPC, Subnets (public + private)
Internet Gateway
Route Tables
Security Groups
EC2 instance in public subnet


Everything using variables and outputs


Week 2 — AWS Resources with Terraform (Days 8-14)
Day 8 — VPC Deep Dive

VPC, Subnets, CIDR blocks
Internet Gateway, NAT Gateway
Route Tables, Route Table Associations
Practice: Build 3-tier network (public, private, database subnets)

Day 9 — EC2 & Auto Scaling

EC2 with user_data scripts
Key pairs, security groups
Launch Templates
Auto Scaling Groups
Practice: EC2 with nginx installed via user_data

Day 10 — Load Balancers

Application Load Balancer (ALB)
Target Groups
Listeners and Rules
Health checks
Practice: ALB + EC2 Auto Scaling Group

Day 11 — S3 & IAM

S3 bucket with versioning, encryption, lifecycle
IAM users, roles, policies
Instance profiles
Practice: S3 bucket + IAM role for EC2 to access S3

Day 12 — RDS

RDS instance in private subnet
Subnet groups, parameter groups
Security groups for RDS
Practice: RDS MySQL in private subnet with EC2 in public subnet

Day 13 — EKS

EKS cluster with Terraform
Node groups
IAM roles for EKS
Practice: Full EKS cluster setup (directly relevant to your profile)

Day 14 — Revision + Project

Build complete 3-tier architecture:

VPC + subnets
ALB → EC2 Auto Scaling
RDS in private subnet
S3 for storage
IAM roles
All in one Terraform project




Week 3 — Advanced Terraform (Days 15-21)
Day 15 — Workspaces

What are workspaces
terraform workspace new/select/list
Using workspaces for dev/staging/prod
Practice:

bashterraform workspace new dev
terraform workspace new prod
terraform workspace select dev
terraform apply -var-file=dev.tfvars
Day 16 — Loops & Conditionals

count — create multiple resources
for_each — create resources from maps/sets
for expressions
Conditional expressions
Practice:

hcl# Create multiple S3 buckets
variable "buckets" {
  default = ["dev", "staging", "prod"]
}
resource "aws_s3_bucket" "env_buckets" {
  for_each = toset(var.buckets)
  bucket   = "myapp-${each.key}-bucket"
}
Day 17 — Dynamic Blocks

dynamic block for repeated nested blocks
Practice:

hcl# Dynamic security group rules
dynamic "ingress" {
  for_each = var.ingress_rules
  content {
    from_port   = ingress.value.port
    to_port     = ingress.value.port
    protocol    = "tcp"
    cidr_blocks = ingress.value.cidr_blocks
  }
}
Day 18 — Functions

String functions — format, join, split, replace
Collection functions — length, flatten, merge, lookup
Numeric functions
Type conversion functions
Practice: Use 10 different functions in real resources

Day 19 — Terraform with CI/CD

Run Terraform in Jenkins pipeline
Run Terraform in GitHub Actions
Practice:

yaml# GitHub Actions Terraform pipeline
- name: Terraform Plan
  run: terraform plan -out=tfplan
- name: Terraform Apply
  run: terraform apply tfplan
```

**Day 20 — Terraform Cloud & Sentinel**
- Terraform Cloud basics
- Remote runs
- Sentinel policies for compliance
- Practice: Connect local Terraform to Terraform Cloud

**Day 21 — Revision + Advanced Project**
- Build multi-environment infrastructure:
  - Dev, Staging, Prod workspaces
  - Reusable modules for VPC, EC2, RDS
  - Remote state in S3
  - CI/CD pipeline applying Terraform on merge

---

**Week 4 — Interview Prep (Days 22-30)**

**Day 22 — Common Interview Questions Set 1**

Practice answering these:
1. What is Terraform state and why is it important?
2. What happens if two people run terraform apply simultaneously?
3. What is the difference between `count` and `for_each`?
4. How do you handle secrets in Terraform?
5. What is a Terraform module?

**Day 23 — Common Interview Questions Set 2**

1. How do you import existing AWS resources into Terraform?
2. What is the difference between `terraform taint` and `terraform import`?
3. How do you prevent accidental deletion of resources?
4. What is `depends_on` and when do you use it?
5. What is the difference between local and remote state?

**Day 24 — Common Interview Questions Set 3**

1. How do you manage multiple environments in Terraform?
2. What is a data source and how is it different from a resource?
3. How do you structure a large Terraform project?
4. What is `terraform plan -out` and why use it?
5. How do you handle Terraform state drift?

**Day 25 — Scenario Based Questions**

Practice these real-world scenarios:

1. Your `terraform apply` fails halfway — what do you do?
2. A colleague manually changed an AWS resource — how do you handle it?
3. You need to rename a resource without destroying it — how?
4. You need to move a resource to a different module — how?
5. Your state file got corrupted — what do you do?

**Day 26 — Debugging & Troubleshooting**

- `TF_LOG=DEBUG terraform apply`
- Reading plan output carefully
- Understanding resource diffs
- Fixing state issues
- Practice: Intentionally break configs and fix them

**Day 27 — Terraform Security Best Practices**

- Never store secrets in `.tf` files
- Use AWS Secrets Manager + SSM Parameter Store
- Encrypt state file in S3
- Use least privilege IAM for Terraform
- Enable state locking with DynamoDB
- Practice: Implement all security best practices

**Day 28 — Mock Interview Day 1**

Answer these without notes, time yourself 5 mins each:
1. Explain Terraform lifecycle — init, plan, apply, destroy
2. How does remote state work with S3 and DynamoDB?
3. Write a module for reusable VPC
4. How do you handle sensitive variables?
5. Explain `terraform import` with example

**Day 29 — Mock Interview Day 2**

1. Build a complete VPC + EC2 + RDS from scratch live
2. Fix these bugs in Terraform code (use the buggy code from your earlier practice)
3. Explain your real Terraform experience at TCS/Citibank
4. How do you structure Terraform for enterprise multi-account AWS?
5. What is Terragrunt and when would you use it?

**Day 30 — Final Revision & Portfolio**

- Push all Terraform projects to GitHub
- Structure your repo:
```
terraform-aws/
├── modules/
│   ├── vpc/
│   ├── ec2/
│   ├── rds/
│   └── eks/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── README.md

Write README for each module
These become your portfolio and interview talking points


Daily Routine
TimeActivity30 minsRead theory / docs60 minsHands on practice in AWS20 minsPush to GitHub10 minsReview what you built

Best Resources
ResourceUse forKodeKloud TerraformStructured learning + labsTerraform official docsReference while codingSpacelift blogAdvanced conceptsAnton Babenko YouTubeReal world Terraform patternsTutorials DojoTerraform Associate exam prep

Certification to aim for
After 30 days go for HashiCorp Terraform Associate (003) — adds strong credibility to your resume alongside your AWS experience. Study takes 1 extra week after this roadmap.

Top interview topics by frequency:
TopicHow often askedState management⭐⭐⭐⭐⭐ Every interviewModules⭐⭐⭐⭐⭐ Every interviewcount vs for_each⭐⭐⭐⭐⭐ Every interviewRemote backend⭐⭐⭐⭐ Very frequentWorkspaces⭐⭐⭐⭐ Very frequentImport⭐⭐⭐⭐ Very frequentDynamic blocks⭐⭐⭐ FrequentSentinel⭐⭐ Occasional
By Day 30 you'll have real projects on GitHub, strong fundamentals, and confident answers for every interview question. Your existing TCS experience with Terraform gives you real examples to quote — that's your biggest advantage over freshers. 🚀