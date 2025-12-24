Terraform Functions in AWS (Complete Guide)
1️⃣ What Are Terraform Functions?

Terraform functions are built-in helper methods that allow you to:

Manipulate strings, numbers, lists, maps

Perform conditions and validations

Format data dynamically

Control logic inside Terraform configuration

👉 Functions are not AWS-specific, but they are heavily used when provisioning AWS resources with Terraform.

2️⃣ Syntax of Terraform Functions
function_name(argument1, argument2, ...)


Example:

upper("devops")

3️⃣ Categories of Terraform Functions (Most Important)

Terraform functions are grouped into the following categories:

🧮 1. Numeric Functions

Used for calculations.

Function	Description
abs()	Absolute value
ceil()	Rounds up
floor()	Rounds down
max()	Maximum value
min()	Minimum value
Example (AWS EC2 instance count)
instance_count = max(2, var.instance_count)


Ensures minimum 2 EC2 instances.

🔤 2. String Functions

Used to manipulate text.

Function	Description
upper()	Convert to uppercase
lower()	Convert to lowercase
trim()	Remove whitespace
replace()	Replace string
format()	Format string
Example (AWS resource naming)
name = format("%s-%s", var.env, "vpc")


Output:

dev-vpc

📚 3. Collection Functions (List & Map)

Very common in AWS infra.

Function	Description
length()	Size of list/map
element()	Get element by index
lookup()	Get value from map
merge()	Merge maps
flatten()	Flatten nested lists
zipmap()	Create map from lists
Example (Subnet CIDR selection)
cidr_block = element(var.subnet_cidrs, count.index)

Example (Tags in AWS)
tags = merge(
  var.common_tags,
  {
    Name = "ec2-${var.env}"
  }
)

🔀 4. Conditional Functions

Used to apply logic.

Function	Description
condition ? true : false	Ternary operator
coalesce()	First non-null value
try()	Catch errors safely
Example (Environment-based instance type)
instance_type = var.env == "prod" ? "t3.large" : "t3.micro"

Example (Fallback values)
ami = try(var.custom_ami, data.aws_ami.amazon_linux.id)

📐 5. Type Conversion Functions

Convert data types.

Function	Description
tolist()	Convert to list
tomap()	Convert to map
tostring()	Convert to string
tonumber()	Convert to number
Example
allowed_ports = tolist(["22", "80", "443"])

🧱 6. Encoding & Decoding Functions

Used for AWS policies & user data.

Function	Description
jsonencode()	Convert HCL → JSON
jsondecode()	Convert JSON → HCL
base64encode()	Encode base64
base64decode()	Decode base64
Example (IAM Policy)
policy = jsonencode({
  Version = "2012-10-17"
  Statement = [{
    Effect = "Allow"
    Action = "s3:*"
    Resource = "*"
  }]
})

📦 7. File & Template Functions

Used for scripts and configs.

Function	Description
file()	Read file content
templatefile()	Dynamic templates
fileset()	List matching files
Example (EC2 User Data)
user_data = file("userdata.sh")

Example (Dynamic User Data)
user_data = templatefile("userdata.sh.tpl", {
  env = var.env
})

🌐 8. Networking & CIDR Functions (Very Important for AWS)
Function	Description
cidrsubnet()	Create subnets
cidrhost()	Get specific IP
cidrnetmask()	Subnet mask
Example (Subnet creation)
cidr_block = cidrsubnet(var.vpc_cidr, 8, count.index)

🕒 9. Date & Time Functions

Used for automation.

Function	Description
timestamp()	Current time
formatdate()	Format date
timeadd()	Add time
Example (Tag with creation date)
CreatedOn = formatdate("YYYY-MM-DD", timestamp())

🧪 10. Validation & Error Handling Functions
Function	Description
can()	Check expression validity
try()	Error fallback
Example (Input validation)
condition = can(regex("^ami-", var.ami_id))

4️⃣ Real-World AWS Example (All Combined)
resource "aws_instance" "app" {
  count         = length(var.subnet_ids)
  ami           = var.ami
  instance_type = var.env == "prod" ? "t3.large" : "t3.micro"
  subnet_id     = element(var.subnet_ids, count.index)

  user_data = templatefile("userdata.sh.tpl", {
    env = upper(var.env)
  })

  tags = merge(var.common_tags, {
    Name = format("app-%s-%d", var.env, count.index)
  })
}

5️⃣ Terraform Functions vs AWS Functions
Terraform	AWS
Evaluated locally	Evaluated by AWS
Used in .tf files	Used in AWS services
No API calls	Uses AWS APIs
6️⃣ Interview One-Line Answer

Terraform functions are built-in expressions used to transform, validate, and manipulate data dynamically while provisioning AWS infrastructure using Terraform.

7️⃣ Most Asked Terraform Functions in Interviews

✅ lookup()
✅ merge()
✅ element()
✅ jsonencode()
✅ cidrsubnet()
✅ templatefile()
✅ try()
✅ coalesce()