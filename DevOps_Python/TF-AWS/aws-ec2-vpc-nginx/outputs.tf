output "instance_public_ip" {
  description="The public ip address of the ec2 instance.."
  value = aws_instance.nginxserver.public_ip
}

output "instance_url" {
  description = "The url to access Nginx server"
  value= "https://${aws_instance.nginxserver.public_ip}"
}