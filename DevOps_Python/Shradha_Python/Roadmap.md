
Day 1 — Python Basics & Data Types
Theory (30 mins):
→ Variables, strings, integers, floats, booleans
→ Truthy/Falsy values — critical for DevOps scripts
→ Type conversion — int(), str(), float(), bool()
→ isinstance() — validate types from API responses

Practice:
→ Write script that reads env variables and validates types
→ Fix the "0" string truthy bug in a deployment check
→ Build a config validator using isinstance()

Day 2 — Data Structures
Theory (30 mins):
→ Lists — ordered, mutable
→ Dictionaries — key-value pairs (Boto3 responses)
→ Sets — unique values, deduplication
→ Tuples — immutable, fixed data

Practice:
→ Parse a mock Boto3 EC2 response dictionary
→ Deduplicate server list using sets
→ Filter running instances from list of dicts

Day 3 — Control Flow
Theory (30 mins):
→ if/elif/else
→ for loops, while loops
→ break, continue, pass
→ List comprehensions
→ Ternary operator

Practice:
→ Write deployment gate — deploy only if branch=main AND tests pass
→ Filter CPU usage list above 80 using list comprehension
→ Loop through EC2 instances and print status
Day 4 — Functions
Theory (30 mins):
→ def, return, arguments
→ *args, **kwargs
→ Default arguments
→ Type hints
→ Docstrings

Practice:
→ Write check_disk_usage(path, threshold=80)
→ Write validate_ip_address(ip) with type hints
→ Write send_alert(*servers, message="default alert")
Day 5 — Error Handling
Theory (30 mins):
→ try/except/finally
→ raise custom exceptions
→ Multiple except blocks
→ Exception chaining

Practice:
→ Wrap file read in proper try/except/finally
→ Create custom ConfigNotFoundError exception
→ Write retry logic with exception handling
Day 6 — File Operations
Theory (30 mins):
→ open(), read(), write(), append()
→ with statement — context manager
→ os.path operations
→ JSON and YAML file handling

Practice:
→ Read server.log and count ERROR lines
→ Parse a Kubernetes YAML manifest
→ Write JSON report to file with timestamp
Day 7 — Revision + Mini Project
Build: Log analyzer script
→ Read server.log
→ Count INFO, WARNING, ERROR lines
→ Write JSON report
→ argparse for --file and --output flags
→ Proper logging throughout

Phase 2 — Intermediate Python (Week 3-4)

Day 8 — Modules & Imports
Theory (30 mins):
→ import, from import, as
→ Standard library — os, sys, json, re, datetime
→ pip and virtual environments
→ requirements.txt

Practice:
→ Use os module for file operations
→ Use datetime for timestamp generation
→ Use re for log parsing
Day 9 — argparse & Logging
Theory (30 mins):
→ argparse — CLI tools
→ Required vs optional args
→ store_true for flags
→ Mutually exclusive groups
→ logging module — handlers, formatters, levels
→ RotatingFileHandler

Practice:
→ Build CLI tool with --env, --region, --action
→ Add logging to file + console simultaneously
→ Add --verbose flag for DEBUG level
Day 10 — OS & System Automation
Theory (30 mins):
→ os module — files, dirs, env vars
→ subprocess — run shell commands
→ psutil — system metrics
→ shutil — file operations

Practice:
→ Check CPU, memory, disk usage with psutil
→ Run shell commands from Python with subprocess
→ Archive and delete log files older than 7 days
Day 11 — Regular Expressions
Theory (30 mins):
→ re.match(), re.search(), re.findall()
→ Common patterns — IP, email, timestamp
→ Groups and named groups
→ Compile for performance

Practice:
→ Extract all IPs from nginx access log
→ Parse timestamps from log entries
→ Validate email addresses in config
Day 12 — Working with APIs
Theory (30 mins):
→ requests library
→ GET, POST, PUT, DELETE
→ Headers, authentication
→ Error handling — status codes
→ Retry logic with backoff

Practice:
→ Call GitHub API to list repos
→ POST to Slack webhook for alerts
→ Build retry decorator with exponential backoff
Day 13 — Decorators & Advanced Python
Theory (30 mins):
→ What are decorators
→ @retry decorator
→ @timer decorator
→ @logger decorator
→ functools.wraps

Practice:
→ Write @retry(times=3, delay=2) decorator
→ Write @timer decorator for performance logging
→ Write @validate_args decorator
Day 14 — Revision + Project
Build: System health checker
→ Check CPU, memory, disk on multiple servers
→ Read server list from CSV
→ Generate HTML report
→ Send Slack alert if any metric above threshold
→ argparse, logging, error handling

Phase 3 — DevOps Specific Python (Week 5-6)

Day 15 — Boto3 Basics
Theory (30 mins):
→ What is Boto3
→ boto3.client vs boto3.resource
→ Pagination
→ Waiter — wait for resource to be ready
→ Error handling — ClientError, BotoCoreError

Practice:
→ List all EC2 instances with state
→ Filter instances by tag
→ Find instances with no tags
Day 16 — Boto3 EC2 Automation
Practice:
→ Start/stop EC2 based on CLI argument
→ Get public IP of all running instances
→ List security groups attached to instance
→ Find stopped instances older than 30 days
Day 17 — Boto3 S3
Practice:
→ Check if bucket exists, create if not
→ Upload file with timestamp prefix
→ List all objects with size and last modified
→ Enable versioning on bucket
→ Set lifecycle policy — Glacier after 90 days
Day 18 — Boto3 IAM
Practice:
→ List all IAM users with last login
→ Create IAM user with ReadOnlyAccess policy
→ Find users who never logged in
→ Check MFA status for all users
Day 19 — Boto3 CloudWatch
Practice:
→ Fetch CPU metrics for EC2 last 1 hour
→ Create alarm for CPU above 80%
→ List all alarms and states
→ Fetch memory metrics — min, max, average
Day 20 — Paramiko SSH Automation
Theory (30 mins):
→ paramiko.SSHClient
→ sftp.get() and sftp.put()
→ Connection timeout and retry
→ Key-based authentication

Practice:
→ SSH into server, run df -h
→ Download log file via SFTP
→ Run command on multiple servers in parallel
Day 21 — Revision + Big Project
Build: Multi-server log collector
→ Read servers from CSV
→ SSH into each server
→ Download /var/log/app.log
→ Count ERROR, WARNING, INFO
→ CRITICAL alert if ERROR > 10
→ Generate JSON report
→ Handle unreachable servers gracefully

Phase 4 — Advanced DevOps Python (Week 7-8)

Day 22 — Multithreading
Theory (30 mins):
→ threading module
→ ThreadPoolExecutor
→ Thread safety
→ Queue for worker pattern

Practice:
→ Health check 10 URLs in parallel
→ Boto3 calls across 5 regions simultaneously
→ SSH into 10 servers at same time
Day 23 — Docker Python SDK
Practice:
→ List running containers
→ Stop/start container by name
→ Pull latest image
→ Remove exited containers
→ Build image from Dockerfile
Day 24 — Kubernetes Python Client
Practice:
→ List pods across all namespaces
→ Check if all pods are Running
→ Restart deployment by patching annotation
→ Watch for CrashLoopBackOff events
→ Scale deployment replicas
Day 25 — YAML & Kubernetes Manifests
Practice:
→ Read K8s deployment YAML
→ Update image tag programmatically
→ Update replica count
→ Apply manifest using subprocess kubectl
→ Compare two manifest files for diff
Day 26 — CI/CD Python Scripts
Practice:
→ Parse Jenkins build log for failed tests
→ Deployment script — pull image, restart, verify
→ Rollback script — stop current, start previous
→ Check if Docker tag exists before deploying
→ Read versions.json and deploy each service
Day 27 — Real World Project 1
Build: AWS Cost Report Generator
→ List all EC2, RDS, S3
→ Calculate estimated monthly cost
→ Generate JSON + HTML report
→ Send via AWS SES email
→ argparse, logging, error handling
Day 28 — Real World Project 2
Build: Kubernetes Health Dashboard
→ Connect to AKS/EKS cluster
→ Collect pod status across namespaces
→ Check node CPU and memory
→ Identify CrashLoopBackOff pods
→ Generate HTML dashboard
→ Send Slack alert for critical issues
Day 29 — Mock Interview Day
Answer without notes — 20 mins each:
→ Write boto3 script to find untagged EC2
→ Write retry decorator with exponential backoff
→ Parse K8s YAML and update image tag
→ Write multithreaded URL health checker
→ Build CLI deployment tool with argparse
Day 30 — Portfolio & GitHub
→ Review all 30 days of scripts
→ Add logging + error handling to every script
→ Push to GitHub with folder structure
→ Write README for each folder
→ Pick 5 best scripts — add detailed comments

GitHub Folder Structure:
python-devops/
├── day01-data-types/
├── day02-data-structures/
├── day03-control-flow/
├── day04-functions/
├── day05-error-handling/
├── day06-file-operations/
├── system-monitoring/
├── aws-boto3/
│   ├── ec2/
│   ├── s3/
│   ├── iam/
│   └── cloudwatch/
├── ssh-automation/
├── docker-kubernetes/
└── projects/
    ├── log-collector/
    ├── health-checker/
    ├── cost-reporter/
    └── k8s-dashboard/

Daily Routine — Non Negotiable:
TimeActivity30 minsRead theory60 minsWrite code — no copy paste20 minsReview and clean up10 minsPush to GitHub

3 Rules to follow strictly:

Never copy paste — type every line yourself
Every script must have — argparse + logging + error handling
Push to GitHub daily — becomes your portfolio


Resources in order of priority:
ResourceUse forAutomate the Boring Stuff (free)Days 1-7 fundamentalsReal Python (realpython.com)Days 8-14 intermediateBoto3 official docsDays 15-21 AWS automationKodeKloud Python for DevOpsStructured labsAbhishek Veeramalla YouTubeReal world projects

Interview readiness by phase:
After PhaseYou can handlePhase 1 (Week 2)Junior DevOps Python questionsPhase 2 (Week 4)Mid-level scripting questionsPhase 3 (Week 6)Senior AWS automation questionsPhase 4 (Week 8)Any Python DevOps interview question
By Day 30 you'll have a strong GitHub portfolio, real project experience, and full confidence to handle any Python question in a DevOps interview. 🚀