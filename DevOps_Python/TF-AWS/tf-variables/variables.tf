variable "aws_instance_type" {
  description = "What type of instance you want to create?"
  type = string
  validation {
    condition = var.aws_instance_type=="t2.micro" || var.aws_instance_type=="t3.micro"
    error_message = "only t2 and  t3 micro allowed"
  }
}

# variable "root_volume_size" {
#   type = number
#   default = 20
# }

# variable "root_volume_type" {
#   type = string
#   default = "gp2"
# }

variable "ec2_config" {
  type = object({
     v_size = number
     v_type = string 
  })
    default = {
        v_size = 20
        v_type = "gp2"
    }
}

variable "additional_tags" {
  type = map(string) # Expecting key value
  default = {
    "name" = "value"
  }

}