resource "aws_instance" "web_server" {
  ami = ""
  instance_type = var.instance_type

  tags = merge(
    var.resource_tags,
    {
        Name = var.instance_type
        Demo = "create_before_destroy"
    }
  )

  lifecycle {
    create_before_destroy = true
  }

}

resource "aws_s3_bucket_versioning" "critical_data" {
  bucket = aws_s3_bucket.critical_data.id
    versioning_configuration {
        status = "Enabled"
    }
}

resource "aws_launch_template" "app_server" {
  name_prefix = "app-server-"
    image_id = ""   
    instance_type = var.instance_type

    tag_specifications {
        resource_type = "instance"
        tags = merge(
            var.resource_tags,
            {
                Name = "App Server from ASG"
                Demo = "ignore_changes"
            }
        )
    }
}

resource "aws_autoscaling_group" "app_asg" {
  name_prefix = "app-asg-"
    max_size = 2
    min_size = 1
    desired_capacity = 1
    launch_template {
        id = aws_launch_template.app_server.id
        version = "$Latest"
    }
}


