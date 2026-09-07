variable "name_prefix" {
  description = "Prefix for resource names"
  type = string
}

variable "vpc_cidr" {
  description = "CIDR block for vpc"
  type = string
}

variable "azs" {
  description = "List of availability Zones"
  type = list(string)
}

variable "private_subnets" {
  description = "List of Private subnet CIDR blocks"
  type = list(string)
}

variable "public_subnets" {
  description = "List of Public subnet CIDR blocks"
  type=list(string)
}

variable "enable_nat_gateway" {
  description = "Use a single NAT gateway for all private subnets"
  type = bool
  default = true
}

variable "single_nat_gateway" {
  description = "Use a single nat gateway for all private subnets"
  type = bool
  default = true
}


