variable "ec2_config" {
  type= list(object({
    ami = string
    instance_type= string
  }))
}

# For each we generally use with map and set

variable "ec2_map" {
  #key,value (object{ami,inst})
  type= map(object({
    ami = string
    instance_type= string
  }))
}