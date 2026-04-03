resource "aws_s3_bucket" "bucket1" {
   count=2
   # here we can use length becuase it is list
   #count=length(var.bucket_names)
    bucket= var.bucket_names[count.index]
  
   tags=var.tags
}

resource "aws_s3_bucket" "bucket_2" {
  # Here we cannot use length because it is set and set does not maintain the order of the elements and also does not allow duplicate values
  for_each = var.bucket_name_set
  #bucket=each.value
  bucket=each.key # both each.key and each.value are same in set but the difference will come when we will
  # use map because there we use key value pair
  tags = var.tags
  depends_on = [ aws_s3_bucket.bucket1 ]
}