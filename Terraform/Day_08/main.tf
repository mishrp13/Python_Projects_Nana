resource "aws_s3_bucket" "bucket1" {
   count=2
   #count=length(var.bucket_names)
    bucket= var.bucket_names[count.index]
  
   tags=var.tags
}

resource "aws_s3_bucket" "bucket_2" {
  for_each = var.bucket_name_set
  #bucket=each.value
  bucket=each.key # both each.key and each.value are same in set but the difference will come when we will
  # use map because there we use key value pair
  tags = var.tags
  depends_on = [ aws_s3_bucket.bucket1 ]
}