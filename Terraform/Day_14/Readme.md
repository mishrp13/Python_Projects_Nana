📘 Day 14 — AWS Static Website Hosting with Terraform


🧠 Core Topic

How to deploy a static website on AWS using Infrastructure-as-Code (Terraform), with S3 + CloudFront + Terraform resources, keeping security and performance best practices. 
GitHub

📌 What You’ll Learn (Key Concepts)
📍 1) Infrastructure As Code with Terraform

Terraform lets you write declarative config files to define cloud resources. This means you write “what you want” and Terraform figures out how to get there. 
terraform.video

📍 2) AWS Static Website Architecture
Users (internet)
     ↓ HTTPS
CloudFront CDN
     ↓
Origin: S3 Bucket (private)


✔ S3 bucket stores website files (HTML/CSS/JS)
✔ CloudFront caches and delivers content worldwide
✔ OAC (Origin Access Control) ensures security — only CloudFront can read from the bucket 
LinkedIn

📌 Terraform Resources Usually Used
Terraform Resource	Purpose
aws_s3_bucket	Stores static assets
aws_s3_bucket_policy	Controls access permissions
aws_cloudfront_distribution	CDN layer for caching & delivery
aws_s3_bucket_object	Uploads individual files
for_each	Automates uploading multiple files
outputs	Exposes outputs like website URL
🧾 Configuration Notes
🛠 1. S3 Bucket

You create an S3 bucket.

Do not make it public.

Use CloudFront as a secured origin.

📄 2. CloudFront CDN

Points to the S3 bucket.

Serves content over HTTPS.

Ensures fast global delivery.

🔐 3. Origin Access Control (OAC)

Instead of public bucket access:

CloudFront is given a policy to read only.

That means users never talk directly to S3.

Keeps the bucket secure. 
LinkedIn

📊 Diagram You Can Draw
           Internet Users
                 ↓ HTTPS
          ╔══════════════════╗
          ║ CloudFront CDN   ║
          ╚══════════════════╝
                  |
           OAC secure access
                  |
          ╔══════════════════╗
          ║ S3 Bucket (origin)║  ← Website assets (HTML/CSS/JS)
          ╚══════════════════╝

📜 Useful Terraform Code Snippets
📌 1. S3 Bucket
resource "aws_s3_bucket" "website" {
  bucket = "my-static-site"
  acl    = "private"
}

📌 2. CloudFront Distribution
resource "aws_cloudfront_distribution" "cdn" {
  origin {
    domain_name = aws_s3_bucket.website.bucket_regional_domain_name
    origin_id   = "s3-origin"
  }
  enabled = true
  default_cache_behavior {
    allowed_methods  = ["GET","HEAD"]
    cached_methods   = ["GET","HEAD"]
    target_origin_id = "s3-origin"
    viewer_protocol_policy = "redirect-to-https"
  }
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

📌 3. Uploading Files
resource "aws_s3_bucket_object" "files" {
  for_each = fileset("www", "*")

  bucket = aws_s3_bucket.website.id
  key    = each.value
  source = "www/${each.value}"
}

📝 Takeaways (Bullet Points)

Infrastructure as Code (IaC) makes deployments reproducible. 
terraform.video

Static websites are cost-effective because S3 + CloudFront has no server cost. 
LinkedIn

Security through OAC keeps the bucket private while still serving content fast. 
LinkedIn

Terraform loops (for_each) help automate uploading many files. 
terraform.video

📌 Best Practices Covered

✅ Keep S3 private → only CloudFront access
✅ Use HTTPS via CloudFront
✅ Automate file uploads with Terraform
✅ Output distribution domain for use

🧠 Quick Revision Notes

Why use CloudFront?

Caches content globally for speed

Hides S3 bucket from public internet

Terraform Benefits

Version control your infra

Reproducible deployments

No manual console clicks


---------------------------------------------------------

🧠 Core Difference (one-liner)
for loop → used inside expressions to transform data
for_each → used to create multiple resources dynamically
🔁 1. for loop (Expression)

Used to manipulate or generate values (lists/maps).

✅ Example:
variable "names" {
  default = ["app", "db", "cache"]
}

output "upper_names" {
  value = [for name in var.names : upper(name)]
}

👉 Output:

["APP", "DB", "CACHE"]
💡 Key points:
Works inside [] (list) or {} (map)
Does not create resources
Used for:
Transforming data
Filtering
Formatting
⚙️ 2. for_each (Meta-argument)

Used to create multiple instances of a resource/module

✅ Example:
variable "instances" {
  default = {
    app = "t2.micro"
    db  = "t2.small"
  }
}

resource "aws_instance" "example" {
  for_each = var.instances

  instance_type = each.value
  tags = {
    Name = each.key
  }
}

👉 This creates:

1 EC2 for app
1 EC2 for db
💡 Key points:
Used in resource, module, or data blocks
Creates multiple real infrastructure resources
Uses:
each.key
each.value
🔥 Interview Comparison Table
Feature	for loop 🧮	for_each ⚙️
Purpose	Data transformation	Resource creation
Used in	Expressions	Resource/Module blocks
Output	List / Map	Multiple resources
Keywords	for, in	for_each, each.key, each.value
Creates infra?	❌ No	✅ Yes
🎯 Interview Tip (Say this confidently)

“In Terraform, a for loop is used to transform data structures like lists or maps, whereas for_each is used to create multiple instances of resources based on a map or set. So one is for data processing, the other is for infrastructure provisioning.”

⚠️ Common Mistake (Good to mention)
Beginners confuse for_each with loops
👉 But Terraform is declarative, not procedural
👉 So for_each is not a loop—it’s a resource iterator