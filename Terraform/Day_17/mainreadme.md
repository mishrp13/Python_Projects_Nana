🧱 What main.tf DOES (High-Level)

main.tf prepares AWS so that later files (blue.tf, green.tf) can safely deploy environments.

It sets up four essential pillars:

Terraform & AWS configuration

IAM permissions (who can do what)

Elastic Beanstalk application container

Secure S3 storage for application versions

1️⃣ Terraform & AWS Setup

Why: Terraform must know which tools and which AWS region to use.

What it does:

Locks Terraform to version ≥ 1.0

Locks AWS provider to version 5.x

Configures AWS region using var.aws_region

📌 Without this, Terraform cannot run.

2️⃣ IAM: Permissions (MOST IMPORTANT PART)

Elastic Beanstalk needs two different IAM roles:

🔹 A. EC2 Instance Role

Used by the EC2 servers that run your app.

This role:

Can be assumed only by EC2

Has AWS-managed policies for:

Web apps

Worker tasks

Docker/multicontainer support

Is wrapped in an instance profile (required by EC2)

📌 Without this role:

EC2 instances fail to launch

Application cannot run

🔹 B. Elastic Beanstalk Service Role

Used by Elastic Beanstalk itself.

This role allows EB to:

Create and manage EC2, ELB, ASG

Perform health checks

Run managed platform updates

📌 Without this role:

Environments fail during creation

Health reporting breaks

3️⃣ Elastic Beanstalk Application (Metadata Only)

What it is:

A logical container for environments and versions

Does NOT create servers

Does NOT deploy code

Why it exists:

Blue and Green environments must belong to an application

Application versions must be attached to an application

📌 Think of it as “registering the app name in AWS”.

4️⃣ S3 Bucket for Application Versions

Elastic Beanstalk requires S3 to store .zip files (app versions).

main.tf:

Creates a globally unique S3 bucket

Uses AWS account ID to avoid name collisions

Applies tags

🔒 Security Hardening

The bucket is fully locked down:

No public ACLs

No public bucket policies

No accidental exposure

📌 This is production-grade security.

5️⃣ AWS Account Identity (Data Source)

Terraform queries AWS to get:

Your account ID

Used only to:

Make S3 bucket names unique across all AWS accounts

📌 This does not create anything.

🚫 What main.tf DOES NOT Do

main.tf intentionally does NOT:

Create EC2 instances

Deploy application code

Create Elastic Beanstalk environments

Perform blue-green switching

Those happen in:

blue.tf

green.tf

🧠 Mental Model (Remember This)

Think of main.tf as:

“Preparing the land before building the house.”

IAM = permissions

S3 = storage

EB Application = app registration

Only after this foundation exists can you safely deploy environments.

📌 One-Line Reference (Save This)

main.tf sets up Terraform, IAM roles, secure S3 storage, and the Elastic Beanstalk application — it prepares AWS but does not deploy anything.