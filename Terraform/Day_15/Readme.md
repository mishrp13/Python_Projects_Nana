💡Successfully Completed Cross-Region VPC Peering Project using Terraform (AWS)

I’m excited to share that I’ve successfully completed a hands-on AWS VPC Peering project using Terraform, guided by Piyush sachdeva. This project gave me strong practical exposure to AWS networking concepts and Infrastructure as Code (IaC).

🔹 Project Overview:


The goal of this project was to design and implement a cross-region VPC peering architecture that enables secure communication between AWS resources deployed in different regions.
    

🔹 Architecture & Implementation Details:
      
Created a Primary VPC in us-east-1

Created a Secondary VPC in us-east-2

Provisioned subnets in each VPC with appropriate CIDR blocks

Configured custom route tables for both VPCs

Established and accepted a cross-region VPC peering connection

Updated route tables to enable traffic flow between the VPCs

Launched EC2 instances in both regions using Terraform

Configured security groups to allow ICMP traffic for connectivity testing



🔹 Validation & Results:

After completing the setup, I successfully pinged EC2 instances across different AWS regions, which confirmed:

✔ Correct VPC peering configuration

✔ Proper route table entries

✔ Security groups allowing cross-VPC communication

🔹 Key Learnings & Takeaways:

In-depth understanding of AWS VPC architecture

Hands-on experience with cross-region VPC peering

 Working with Terraform multi-provider configurations

Importance of routing and security groups in AWS networking

Validating and troubleshooting network connectivity


This project has significantly boosted my confidence in designing and implementing AWS networking solutions using Terraform. Looking forward to building more real-world cloud and DevOps projects 🚀

#AWS #Terraform #VPCPeering #CloudNetworking #DevOps #InfrastructureAsCode #AWSProjects 