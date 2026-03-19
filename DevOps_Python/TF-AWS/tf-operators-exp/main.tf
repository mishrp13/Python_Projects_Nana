terraform {
  
}


# Number List
variable "num_list" {
  type= list(number)
  default = [ 1,2,3,4,5 ]
}


# object List of Person

variable "person_list" {
  type = list(object({
    fname= string
    lsname= string
  }))

  default = [ {
    fname = "Raju",
    lsname = "Rastogi"
  } ,{
    fname = "sandy"
    lsname = "Singh"
  }
  
  ]
}


# Map

variable "map_list" {
  type = map(number)
  default = {
    "one" = 1
    "two" = 2
    "three"= 3
  }
}

#calculations

locals {
  mul= 2*2
  add = 2+2
  eq= 2!=3

  #double the list
  double= [for num in var.num_list: num *2]

  #odd only
  odd= [for num in var.num_list: num if num%2!=0]

  # To get only first name from person list
  fname_list= [for person in var.person_list: person.fname]

  #work with map
  map_info= [for key,value in var.map_list : key ]

  double_map= {for key , value in var.map_list: key => value *2}

}

output "output" {
  value= local.eq
}

output "out" {
  value = local.double
}

output "ot" {
  value = local.fname_list
}

output "o" {
    value = local.map_info
  
}