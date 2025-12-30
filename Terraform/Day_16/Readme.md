AWS IAM User Management Using Terraform – Notes
Objective

To automate IAM user creation and management in AWS using Terraform, by:

Reading users from a user.csv file

Creating IAM users dynamically

Creating login profiles (console access)

Assigning users to specific IAM groups (Engineer, Manager, Education, etc.)

Tagging users for better management and cost tracking

1. Input File: user.csv

The CSV file acts as the single source of truth for IAM users.

Contains fields like:

first_name

last_name

department

job_title

Why CSV?

Easy to maintain

Scalable (add/remove users without changing Terraform code)

Clean separation of data and infrastructure logic

2. Reading CSV File in Terraform

Terraform uses the csvdecode() function to read and parse the CSV file.

Key Concept

file() → reads the CSV file

csvdecode() → converts it into a list of maps

Each row becomes a user object

This allows Terraform to loop over users dynamically.

3. IAM User Creation
Resource Used

aws_iam_user

Implementation Highlights

Users are created dynamically using for_each

Username is usually constructed using:

first_name.last_name

Each user is uniquely identified using a key (e.g., email or name)

Benefits

No hardcoded users

Fully automated

Idempotent (safe re-runs)

4. Creating IAM Login Profiles (Console Access)
Resource Used

aws_iam_user_login_profile

Purpose

Enables AWS Management Console login for IAM users

Automatically generates a password

Key Features

Password reset required on first login

Secure handling of credentials

Passwords can be output securely if needed

5. IAM Groups Creation
Example Groups

engineer

manager

education

sales

hr

Resource Used

aws_iam_group

Why Groups?

Best practice in AWS IAM

Permissions are assigned to groups, not users

Easier access management

6. Assigning Users to Groups
Resource Used

aws_iam_user_group_membership

Logic Used

Group assignment is based on the department field from the CSV

Conditional or mapping logic determines which group a user belongs to

Example Mapping Logic

If department = Sales → Sales group

If department = Education → Education group

If department = Corporate → Manager group

Benefits

Automatic role-based access control (RBAC)

No manual user-to-group assignment

Easy to scale

7. Tagging IAM Users
Tags Applied

Department

JobTitle

ManagedBy = Terraform

Environment

Purpose of Tagging

Cost allocation

Better organization

Auditing and compliance

Easy filtering in AWS Console

8. Terraform Best Practices Followed

Used for_each instead of count

Data-driven infrastructure (CSV-based)

Reusable and modular design

No hardcoded IAM users or groups

Clear separation of:

Data (CSV)

Logic (Terraform)

Permissions (IAM groups & policies)

9. Advantages of This Approach

✅ Fully automated IAM onboarding

✅ Easy to add/remove users

✅ Scalable for large organizations

✅ Consistent access control

✅ Infrastructure as Code (IaC) compliance

✅ Reduced human error

10. Real-World Use Case

This approach is commonly used in:

Enterprises onboarding employees

Training environments

AWS accounts with frequent user changes

Compliance-driven organizations

