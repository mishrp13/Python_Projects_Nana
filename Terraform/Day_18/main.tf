
resource "random_id" "suffix" {
    byte_length = 4
}

locals {
  bucket_prefix= "${var.project_name}-${var.environment}"
  upload_bucket_name= "${local.bucket_prefix}-upload-${random_id.suffix.hex}"
  processed_bucket_name= "${local.bucket_prefix}-processed-${random_id.suffix.hex}"
  lambda_function_name="${var.project_name}-${var.environment}-processor"
}


resource "aws_s3_bucket" "upload_bucket" {
  bucket = local.upload_bucket_name
}

resource "aws_s3_bucket_versioning" "upload_bucket" {
  bucket = aws_s3_bucket.upload_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "upload_bucket" {
  bucket = aws_s3_bucket.upload_bucket.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "upload_bucket" {
  bucket = aws_s3_bucket.upload_bucket.id
  
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket" "processed_bucket" {
    bucket = local.processed_bucket_name  
}

resource "aws_s3_bucket_versioning" "processed_bucket" {
  bucket = aws_s3_bucket.processed_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "processed_bucket" {
  bucket = aws_s3_bucket.processed_bucket.id
  
  rule{
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "processed_bucket" {
  bucket= aws_s3_bucket.processed_bucket.id

  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}



resource "aws_iam_role" "lambda_role" {
  name= "${local.lambda_function_name}-role"

  assume_role_policy = jsondecode({
  
  "Version": "2012-10-17",
  "Statement": [
    {
      Action:"sts:AssumeRole"
      Effect: "Allow"
      Principal ={
        Service= "lambda.amazonaws.com"
      }
    }
  ]

  })

}

resource "aws_iam_role_policy" "lambda_policy" {
  name = "${local.lambda_function_name}-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${var.aws_region}:*:*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion"
        ]
        Resource = "${aws_s3_bucket.upload_bucket.arn}/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl"
        ]
        Resource = "${aws_s3_bucket.processed_bucket.arn}/*"
      }
    ]
  })
}

