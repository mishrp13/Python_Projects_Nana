Here are three simple ways to create 3 S3 buckets using:

✅ Bash (AWS CLI)
✅ Python (boto3)
✅ Terraform

I’ll keep each one copy-paste ready.

✅ 1️⃣ Create 3 S3 Buckets Using Bash (AWS CLI)
Requirements

AWS CLI installed

Configured with aws configure

Bucket names must be globally unique

Bash Script
#!/bin/bash

REGION="us-east-1"

BUCKETS=(
my-demo-bucket-001
my-demo-bucket-002
my-demo-bucket-003
)

for bucket in "${BUCKETS[@]}"
do
  aws s3api create-bucket \
    --bucket $bucket \
    --region $REGION \
    --create-bucket-configuration LocationConstraint=$REGION

  echo "Created bucket: $bucket"
done


Run:

chmod +x create_buckets.sh
./create_buckets.sh

✅ 2️⃣ Create 3 S3 Buckets Using Python (boto3)
Install boto3
pip install boto3

Python Script
import boto3

region = "us-east-1"

buckets = [
    "my-demo-bucket-101",
    "my-demo-bucket-102",
    "my-demo-bucket-103"
]

s3 = boto3.client("s3", region_name=region)

for bucket in buckets:
    s3.create_bucket(
        Bucket=bucket,
        CreateBucketConfiguration={
            'LocationConstraint': region
        }
    )
    print(f"Created bucket: {bucket}")


Run:

python create_buckets.py

✅ 3️⃣ Create 3 S3 Buckets Using Terraform
Terraform File: main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "bucket1" {
  bucket = "my-demo-bucket-201"
}

resource "aws_s3_bucket" "bucket2" {
  bucket = "my-demo-bucket-202"
}

resource "aws_s3_bucket" "bucket3" {
  bucket = "my-demo-bucket-203"
}

Run Terraform
terraform init
terraform plan
terraform apply

✅ Better Terraform Method — Using Loop (Cleaner)
provider "aws" {
  region = "us-east-1"
}

variable "bucket_names" {
  default = [
    "my-demo-bucket-301",
    "my-demo-bucket-302",
    "my-demo-bucket-303"
  ]
}

resource "aws_s3_bucket" "buckets" {
  for_each = toset(var.bucket_names)
  bucket   = each.value
}

⚠️ Important Notes

Bucket names must be globally unique

Avoid uppercase letters

Use hyphens instead of underscores

Make sure AWS credentials are configured


🐍 ✅ 50 Python DevOps / Cloud Coding Practice Questions
🔹 Python Basics + Automation

Write Python script to create 3 files

Read file line by line

Count word frequency in file

Parse JSON file

Convert JSON → CSV

Read environment variables

Validate input arguments

Add logging to script

Handle exceptions properly

Retry function on failure

🔹 File + OS Automation

List files older than X days

Delete temp files

Zip a directory

Extract archive

Monitor directory for new files

Rename files in bulk

Check disk usage

Execute shell command from Python

Capture command output

Monitor process status

🔹 AWS boto3 Practice

Create S3 bucket

Enable versioning

Upload file to S3

Download file

List all buckets

Create EC2 instance

Stop instances with tag

List AMIs

Create IAM user

Attach IAM policy

🔹 Cloud Automation Tasks

Delete snapshots older than X days

Tag all resources

Audit unused volumes

List idle load balancers

Check security groups with open ports

🔹 API + DevOps Tasks

Call REST API

Parse API response

Handle pagination

Authenticate with token

Build simple webhook listener

🔹 DevOps Utilities

Parse log files

Extract errors from logs

Monitor CPU usage

Send alert email

Create health check script

🔹 Advanced Practice

Multithreaded downloader

Async API calls

Config-driven automation

Build CLI tool with argparse

Write reusable automation module

🐚 ✅ 50 Bash DevOps Coding Practice Questions
🔹 Bash Fundamentals

Write hello world script

Use positional parameters

Read user input

If/else condition

Case statement

For loop

While loop

Functions in bash

Exit codes

Trap signals

🔹 File Operations

Find files older than X days

Delete files by pattern

Count lines in files

Replace string in files

Rename files in loop

Check if file exists

Compare two files

Monitor file changes

Tail logs live

Merge files

🔹 Text Processing

Use grep with regex

awk column extract

sed replace text

Sort + unique lines

Parse CSV

Extract JSON using jq

Extract IPs from logs

Count errors in logs

Filter by date

Parse command output

🔹 System Automation

Check service status

Restart if down

Monitor disk usage

Monitor memory

Kill process by name

List top processes

Cron job script

Backup script

Rotate logs

Health check script

🔹 AWS CLI Bash Tasks

Create S3 buckets loop

Upload files to S3

List EC2 instances

Stop tagged instances

Create security group

🔹 Advanced Bash Tasks

Retry on failure

Parallel execution

Menu-driven script

Script with logging

Error handling framework

🌍 ✅ 50 Terraform Practice Questions
🔹 Terraform Basics

Create S3 bucket

Create EC2 instance

Create security group

Create VPC

Create subnet

Create IAM role

Create EBS volume

Create load balancer

Create RDS

Create autoscaling group

🔹 Variables + Inputs

Use variables

Default values

Variable validation

Sensitive variables

tfvars file

🔹 Loops + Meta Arguments

Use count

Use for_each

Dynamic blocks

Conditional resources

Loop resources from list

🔹 Modules

Create module

Use module

Pass variables to module

Output from module

Version modules

🔹 State Management

Remote backend S3

DynamoDB locking

State import

State rm

State mv

🔹 Terraform Structure

Multi-env setup

Dev/prod workspaces

Folder structure

Reusable code

DRY principles

🔹 Advanced Terraform

Data sources

Depends_on

Lifecycle rules

Ignore changes

Prevent destroy

🔹 Real Interview Tasks

Create 3 S3 buckets with loop

Tag all resources

Enable versioning on buckets

Create VPC module

Create EC2 with user_data

🔹 Production Scenarios

Blue/green infra

Multi-region setup

Conditional env deploy

Partial apply strategy

Destroy selective resources



1. How do you connect two VPCs (same region & different region)?
1. VPC Peering

Works for: Same region and different regions

How it works:

Creates a direct, private network connection between two VPCs

Traffic stays on the AWS backbone (no internet)

You must update route tables and security groups

Limitations:

No transitive routing (VPC-A → VPC-B → VPC-C not allowed)

One-to-one connections only

Best used when:

Few VPCs

Simple architecture

Low latency is required

2. AWS Transit Gateway

Works for: Same region (can connect cross-region using TGW peering)

How it works:

Acts as a central hub for multiple VPCs

Supports transitive routing

Simplifies large network architectures

Advantages:

Scales easily

Centralized routing and security

Cleaner than multiple peering connections

Best used when:

Many VPCs

Enterprise-scale environments

Hub-and-spoke architecture

3. Site-to-Site VPN

Works for: Same region & different region

How it works:

Encrypted IPSec tunnel over the internet

Can connect VPC-to-VPC or VPC-to-on-prem

Limitations:

Lower performance than peering

Depends on internet

Best used when:

Temporary connection

Encryption is required

On-prem integration

4. VPC Endpoint / AWS PrivateLink

Works for: Same region & cross-region (service-based)

How it works:

Exposes specific services, not full VPC access

Uses private IPs

No route table changes needed

Best used when:

You want to access only one service

Microservice architecture

High security requirement

Interview Summary Answer (Strong & Short)

“For simple connectivity between two VPCs in the same or different region, I use VPC Peering. For large-scale architectures requiring transitive routing, I use Transit Gateway. VPN is used for encrypted or temporary connections.”

Comparison Table (Quick Memory Aid)
Method	Same Region	Different Region	Transitive	Use Case
VPC Peering	✅	✅	❌	Simple VPC-to-VPC
Transit Gateway	✅	✅ (peering)	✅	Enterprise scale
Site-to-Site VPN	✅	✅	❌	Secure / temporary
PrivateLink	✅	✅	N/A	Service access

2. S3 bucket policy – how do you give access to a specific folder?

--“To give access to a specific folder in S3, I use bucket policies with object prefixes and explicitly allow ListBucket with conditions. Since S3 doesn’t support real folders, access is always prefix-based.”

You control access using bucket policy or IAM policy with a prefix.

Example:

{
  "Effect": "Allow",
  "Action": ["s3:GetObject"],
  "Resource": "arn:aws:s3:::my-bucket/reports/*"
}


Key points:

S3 has no real folders, only object prefixes

Access can be read / write / list

Can also use IAM roles or ACLs (not recommended)

3. What is a private subnet? How does it access the internet?

Private Subnet:

No direct route to Internet Gateway

Used for DBs, backend services

Internet Access:

Via NAT Gateway (recommended)

Route table → 0.0.0.0/0 → NAT Gateway

NAT Gateway sits in public subnet

4. Load Balancers – types, layers, how they work?

Types:

ALB (Application Load Balancer) – Layer 7

HTTP / HTTPS

Path-based & host-based routing

NLB (Network Load Balancer) – Layer 4

TCP / UDP

High performance, static IP

CLB (Classic) – Legacy

Gateway Load Balancer – Layer 3

Used for firewalls

5. What is CloudWatch? How did you use it?

CloudWatch:

Monitoring & observability service

Used for:

Metrics (CPU, memory, latency)

Logs (application, Lambda, EC2)

Alarms (CPU > 80%, pod crash)

Dashboards

Example:

“I used CloudWatch alarms integrated with SNS for alerts.”

6. What is AWS Lambda?

Serverless compute

Runs code without managing servers

Event-driven (S3, API Gateway, CloudWatch)

Pay only for execution time

Used for:

Automation

API backend

Data processing

7. What is Kinesis? How do you troubleshoot?

Kinesis:

Real-time streaming service

Handles large data streams

Components:

Streams

Shards

Producers

Consumers

Troubleshooting:

Check shard limits

Consumer lag

CloudWatch metrics (IteratorAge)

IAM permissions

Throughput errors

8. Have you worked on Kafka?

Sample answer:

“Yes, I have worked on Kafka for real-time data streaming. I handled topics, partitions, consumer groups, and monitored lag using metrics.”

If no experience:

“I understand Kafka concepts but haven’t worked extensively in production.”

9. Issues you faced recently?

Good examples:

Pod crash due to memory limit

Terraform state lock issue

High latency due to misconfigured ALB

Disk full on EC2

Always include:

Root cause

Fix

Prevention

10. Terraform state file & locking

State file:

Keeps track of real infrastructure

Best practice:

Store in S3

Enable DynamoDB locking

Locking:

Prevents multiple users from modifying infra at same time

11. How do you delete resources in IaC?

terraform destroy

Remove resource from code → terraform apply

Use lifecycle rules (prevent_destroy)

Tag-based cleanup

12. Kubernetes troubleshooting – step by step

kubectl get pods

kubectl describe pod

kubectl logs

Check node status

Check resource limits

Check services & ingress

Validate configmaps & secrets

13. How do you handle production issues?

Structured answer:

Acknowledge alert

Check monitoring/logs

Identify impact

Rollback or quick fix

Communicate status

Permanent fix

Post-mortem



1. Production issues you have handled recently

I handled issues such as memory leaks causing pod OOMKills, increased latency due to uneven traffic distribution at ALB, and failed deployments caused by misconfigured environment variables. I used CloudWatch and Kubernetes metrics to identify the root cause, applied temporary mitigation to restore service, and followed up with permanent fixes and post-incident documentation.

2. How do you use CloudWatch and what options are available?

CloudWatch is used for end-to-end observability. I use metrics for infrastructure health, logs for application debugging, alarms for proactive alerting, dashboards for visualization, and EventBridge for automated responses to system events.

3. What is CloudTrail?

CloudTrail captures all control-plane API activity across AWS services. It is critical for security investigations, compliance audits, and identifying unauthorized or accidental changes in the environment.

--“CloudTrail provides complete visibility into AWS API activity and is mainly used for security auditing, compliance, and incident investigation.”

4. What is .gitignore?

.gitignore defines files that should not be tracked in Git, such as secrets, state files, and build artifacts. It helps maintain repository hygiene and prevents accidental exposure of sensitive data.

5. Difference between Security Group and NACL?

Security Groups are stateful, instance-level firewalls that allow traffic by default once permitted. NACLs are stateless, subnet-level filters that provide an additional layer of network security.

6. S3 lifecycle

S3 lifecycle policies automate data tiering and retention management. They are used to transition infrequently accessed data to cheaper storage classes and enforce data retention policies for compliance.

--S3 Lifecycle is a feature that lets you automatically manage objects in an S3 bucket by transitioning or expiring data based on rules.
It is mainly used for cost optimization and data retention management.

What Lifecycle Rules Can Do
1. Transition Actions

Move objects between storage classes:

Standard → Standard-IA

Standard → One Zone-IA

Standard → Glacier Instant Retrieval

Glacier → Glacier Deep Archive

Example:

Move logs to Standard-IA after 30 days and to Glacier after 90 days.

2. Expiration Actions

Permanently delete objects after a defined period

Delete incomplete multipart uploads

Example:

Delete backup files after 365 days.

Lifecycle Rule Scope

Lifecycle rules can be applied to:

Entire bucket

Specific prefix (folder)

Objects with specific tags

Real-World Use Cases

Log retention management

Archiving old application data

Compliance-based data deletion

Reducing storage cost for infrequently accessed data

Versioned Buckets & Lifecycle

For versioning-enabled buckets:

Can expire noncurrent versions

Can clean up old object versions automatically

Best Practices (Mention in Interview)

Use lifecycle rules with prefix + tags

Combine with S3 Intelligent-Tiering

Enable bucket versioning

Test lifecycle policies carefully (deletion is permanent)

7. Python basics – mutable & immutable, string reverse

Mutable objects like lists can be changed in memory, while immutable objects like strings cannot. String reversal can be efficiently done using slicing, which creates a new string.

8. Steps before deploying code

Before deployment, I ensure code quality through reviews, automated tests, security scans, configuration validation, and infrastructure checks. Deployment is done via CI/CD with rollback strategies enabled.

9. Security measures used in AWS environment

Security is enforced using IAM roles with least privilege, network segmentation, encryption, monitoring with CloudTrail and GuardDuty, and continuous vulnerability scanning.

10. Types of load balancers in AWS and ALB layer

AWS provides ALB, NLB, CLB, and Gateway Load Balancer. ALB works at Layer 7 and supports advanced routing, SSL termination, and WebSocket traffic.

11. Terraform destroy, state storage, and locking

Terraform resources are destroyed using terraform destroy or code changes. State is stored remotely in S3 with DynamoDB locking to ensure safe collaboration and prevent race conditions.

12. CI/CD best practices to prevent inappropriate changes

I enforce strict CI/CD controls such as branch protection, approval workflows, automated testing, artifact versioning, and role-based deployment access to protect production environments.

13. Full overview of monitoring and alerting system

Monitoring combines metrics, logs, and traces to provide visibility into system health. Alerts are configured with thresholds and anomaly detection and integrated with on-call tools for rapid incident response.

14. AWS services used in your project

I have worked extensively with EC2, EKS, ALB, IAM, S3, RDS, Lambda, CloudWatch, CloudTrail, Terraform, and CI/CD services like CodePipeline and GitHub Actions.

15. What is Kinesis?

Kinesis is a scalable streaming platform for real-time data ingestion and processing. It enables handling high-throughput data streams with low latency and fault tolerance.