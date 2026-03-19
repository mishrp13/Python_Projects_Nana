ec2_config = [ {
  ami= "ubuntu" # use correct ami
  instance_type = "t3.micro"
},{
    ami="amazon" # use correct ami 
    instance_type = "t3.micro"
} ]



ec2_map = {
  "ubuntu" = {
  ami= "ubuntu" # use correct ami
  instance_type = "t3.micro"
  },

  "amazon_linux"={
  ami="amazon" # use correct ami 
  instance_type = "t3.micro"
  }
}