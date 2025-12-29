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