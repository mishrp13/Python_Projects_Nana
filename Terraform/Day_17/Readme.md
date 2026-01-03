What is Blue–Green Deployment?

Blue–Green deployment is a release strategy where you run two identical environments:

Blue → current production version

Green → new version you want to release

Only one environment receives live traffic at any time.

Deployment flow

Blue is live and serving users

Green is deployed with the new version

Tests run against Green

Traffic is switched from Blue → Green

Blue is kept for rollback (or destroyed later)

Benefits

✅ Zero downtime

✅ Instant rollback

✅ Safe production releases

How Blue–Green Works in AWS

Common AWS services used:

Application Load Balancer (ALB) – routes traffic

Target Groups – one for Blue, one for Green

EC2 / ECS / EKS / Lambda – application compute

Terraform – controls infrastructure and traffic switching

High-Level Architecture
Users
  |
ALB Listener (port 80)
  |
  |----> Target Group BLUE  (v1)
  |
  |----> Target Group GREEN (v2)


Terraform changes which target group the ALB forwards traffic to.

Blue–Green Deployment with Terraform (EC2 Example)
1️⃣ Define Target Groups
resource "aws_lb_target_group" "blue" {
  name     = "blue-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

resource "aws_lb_target_group" "green" {
  name     = "green-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id
}

2️⃣ Launch Two Auto Scaling Groups (Blue & Green)
resource "aws_autoscaling_group" "blue" {
  name                 = "blue-asg"
  launch_template {
    id      = aws_launch_template.blue.id
    version = "$Latest"
  }
  target_group_arns = [aws_lb_target_group.blue.arn]
  desired_capacity  = 2
}

resource "aws_autoscaling_group" "green" {
  name                 = "green-asg"
  launch_template {
    id      = aws_launch_template.green.id
    version = "$Latest"
  }
  target_group_arns = [aws_lb_target_group.green.arn]
  desired_capacity  = 2
}


👉 Blue runs current app version
👉 Green runs new app version

3️⃣ ALB Listener with Switchable Target Group

This is the key part.

variable "active_color" {
  description = "Which environment is live: blue or green"
  type        = string
  default     = "blue"
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = var.active_color == "blue"
      ? aws_lb_target_group.blue.arn
      : aws_lb_target_group.green.arn
  }
}

4️⃣ Deploy New Version (Green)
terraform apply


Green ASG launches

Green app is live but receives no traffic

You test Green directly (via ALB test rule or instance IP)

5️⃣ Switch Traffic (Blue → Green)
terraform apply -var="active_color=green"


✅ ALB instantly routes all traffic to Green
✅ Blue remains intact for rollback

6️⃣ Rollback (If Needed)
terraform apply -var="active_color=blue"


⚡ Rollback takes seconds

Blue–Green with ECS (Quick Note)

In real-world AWS setups, ECS + ALB + Terraform is more common.

ECS services: blue and green

ALB listener switches target group

Same Terraform concept applies

AWS CodeDeploy can also automate this, but Terraform gives full control.

When to Use Blue–Green vs Rolling
Strategy	Best When
Blue–Green	Zero downtime, fast rollback
Rolling	Cost sensitive, simpler apps
Canary	Gradual traffic testing
Key Terraform Best Practices

Use variables for active environment

Keep both environments identical

Use health checks aggressively

Never destroy the old environment immediately

Summary

Blue–Green = two production-ready environments

ALB controls traffic

Terraform switches traffic using variables

Rollbacks are instant and 




Main.tf:

