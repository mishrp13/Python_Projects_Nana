# Variables, local variables, output variables, Variable precedence

# 1. we use variable or define variable to use it again and again. In locals we can define variables that we defined and make use of it and it makes code more reusable and structured. Variable precedence we have to take care and that is (terraform plan -var=environment=prod (this is something we use while running terraform plan command)> terraform.tfvars (for this we have to create separate terraform.tfvars file and it makes code more managable because then we have to only make changes in that specific file only) > Export (Env Variable ...this is something we have to use in command line) > default(its returen in our main file)) . 

