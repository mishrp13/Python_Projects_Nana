Day 1 — File Operations

Write a script to read a file called server.log and count the total number of lines
Write a script that creates a new file and writes current timestamp + a custom message to it every time it runs
Write a script that reads a log file and appends only lines containing "ERROR" to a new file called errors.log
Write a script that reads two files and merges their content into a third file
Write a script that checks if a file exists before reading it, and prints a proper message if it doesn't


Day 2 — Data Structures

Given a list of server names with duplicates, write a script to remove duplicates and sort alphabetically
Given a list of numbers representing CPU usage, write a script using list comprehension to filter only values above 80
Write a script that takes a dictionary of server:status pairs and prints only servers where status is "stopped"
Given a list of dictionaries containing EC2 instance data, write a script to find the instance with highest CPU using max()
Write a script that merges two dictionaries of server configs, with second dict values overriding first on conflict


Day 3 — Functions & Error Handling

Write a function check_disk_usage(path, threshold=80) that returns True if usage is above threshold
Write a function that reads a config file and raises a custom exception ConfigNotFoundError if file doesn't exist
Write a function with try/except/finally that opens a file, reads it, and always closes it in finally block
Write a function that validates an IP address format and raises ValueError if invalid
Write a function that takes *args of server names and prints each with its index number


Day 4 — OS & System

Write a script that takes a directory path as argument and lists all files with their sizes in KB
Write a script that finds all .log files in a directory older than 7 days and deletes them
Write a script that creates a directory structure like logs/2024/march/ if it doesn't already exist
Write a script that renames all .txt files in a directory by adding today's date as prefix
Write a script that walks through a directory recursively and prints total size of all files combined


Day 5 — String & Regex

Write a script that reads a log file and extracts all unique IP addresses using regex
Write a script that reads an Nginx access log and counts how many times each IP appears
Write a script that finds all lines in a log file matching pattern ERROR: [timestamp] and prints them
Write a script that reads a config file and replaces all occurrences of localhost with a given hostname
Write a script that validates if a list of email addresses are in correct format using regex


Day 6 — JSON & YAML

Write a script that reads a JSON config file and prints each key-value pair in readable format
Write a script that takes a Python dictionary of server configs and writes it to a JSON file with indentation
Write a script that reads a Kubernetes deployment YAML and prints the container image name
Write a script that reads a Kubernetes deployment YAML and updates the image tag from v1.0 to v2.0 and saves it
Write a script that merges two JSON config files into one, with second file values taking priority


Day 7 — Revision Day

Redo Day 1 Question 3 but add proper logging using the logging module instead of print
Redo Day 4 Question 2 but add a --dry-run flag that prints files that would be deleted without actually deleting
Redo Day 5 Question 2 but write results to a JSON file with IP as key and count as value
Combine Day 2 and Day 6 — read a JSON file containing list of EC2 instances, filter only running ones, write filtered list back to a new JSON file
Take any script from Days 1-6 and add proper try/except, logging to file, and argparse for input arguments


Day 8 — Logging & CLI

Rewrite a previous script replacing all print() with proper logging.info(), logging.warning(), logging.error()
Write a script that logs to both console and a file simultaneously using two handlers
Write a script that implements log rotation — max 5 files, 1MB each using RotatingFileHandler
Write a script that logs different levels (DEBUG, INFO, WARNING, ERROR) and filters to show only WARNING and above
Write a logging config using a dictionary config (logging.config.dictConfig) instead of basic config


Day 9 — argparse

Write a script with --host, --port, --protocol arguments that prints a connection string
Write a script with --env (required), --region (default: us-east-1), --action (choices: start/stop/list) arguments
Write a script with a --verbose flag that when passed shows DEBUG logs, otherwise shows only INFO
Write a script with --input-file and --output-file arguments that reads from one and writes to other
Write a script with subcommands — deploy, rollback, status — each with their own arguments


Day 10 — Process & System Monitoring

Write a script using psutil that prints CPU and memory usage every 5 seconds
Write a script that checks disk usage on all mount points and prints WARNING if any is above 80%
Write a script that lists all running processes with their PID, name, and CPU usage
Write a script that finds and kills all processes matching a given name passed as argument
Write a script that monitors system stats every 10 seconds and logs to file, stops after 1 minute


Day 11 — Networking

Write a script that checks if a given host and port is reachable using sockets
Write a script that reads a CSV of hostname,port pairs and checks connectivity for each
Write a script that performs DNS lookup for a list of hostnames and prints their IPs
Write a script that checks HTTP status code of a list of URLs and prints which ones are down
Write a script that measures response time of an HTTP endpoint and alerts if above 2 seconds


Day 12 — SSH Automation (Paramiko)

Write a script using Paramiko to SSH into a server and run df -h command and print output
Write a script that SSHs into multiple servers from a list and runs uptime on each
Write a script that uses Paramiko SFTP to upload a local file to a remote server
Write a script that SSHs into a server, checks if a service is running, and starts it if not
Write a script that collects /var/log/syslog from multiple servers and saves locally with hostname as filename


Day 13 — REST APIs

Write a script that calls the GitHub API to list all public repos of a given username
Write a script that calls a REST API with retry logic — retries 3 times with 5 second wait on failure
Write a script that calls an API, handles 404, 500, and timeout errors separately
Write a script that sends a POST request with JSON payload and prints the response status and body
Write a script that polls an API endpoint every 30 seconds until it returns status "completed"


Day 14 — Revision Day

Build a CLI system monitor tool — --check cpu/memory/disk flags, logs to file, alerts if threshold crossed
Add retry logic to a Paramiko SSH script — retries 3 times if connection fails
Combine Day 11 and Day 13 — check URL health via requests, log results, send alert via API if any URL is down
Rewrite any Day 8-13 script with full argparse + logging + error handling
Write a script that reads server list from JSON, SSHs into each, collects uptime, saves results to JSON


Day 15 — EC2 Basics

Write a boto3 script to list all EC2 instances showing InstanceId, State, and InstanceType
Write a script that filters and prints only running EC2 instances
Write a script that lists all EC2 instances that have no tags attached
Write a script that finds all EC2 instances with a specific tag key-value pair
Write a script that prints all EC2 instances grouped by their state (running, stopped, terminated)


Day 16 — EC2 Advanced

Write a script with argparse that starts or stops an EC2 instance based on --action and --instance-id flags
Write a script that gets the public IP of all running instances and saves to a text file
Write a script that describes all security groups attached to a given instance
Write a script that lists all EC2 instances and checks if detailed monitoring is enabled
Write a script that finds all stopped EC2 instances older than 30 days and prints a cost-saving recommendation


Day 17 — S3

Write a script that checks if an S3 bucket exists and creates it if not
Write a script that uploads a local file to S3 with a timestamp prefix in the key name
Write a script that lists all objects in a bucket with their sizes and last modified date
Write a script that enables versioning on a given S3 bucket
Write a script that sets a lifecycle policy on a bucket to delete objects older than 90 days


Day 18 — IAM

Write a script that lists all IAM users with their creation date and last login time
Write a script that creates a new IAM user and attaches ReadOnlyAccess policy
Write a script that lists all IAM roles and their attached policies
Write a script that finds all IAM users who have never logged in
Write a script that checks if MFA is enabled for all IAM users and prints those without MFA


Day 19 — CloudWatch

Write a script that fetches CPU utilization metrics for a given EC2 instance for the last 1 hour
Write a script that lists all existing CloudWatch alarms and their current states
Write a script that creates a CloudWatch alarm for CPU above 80% on a given instance
Write a script that fetches memory metrics from CloudWatch and prints min, max, average
Write a script that lists all log groups in CloudWatch with their retention periods


Day 20 — Lambda & SNS

Write a script that lists all Lambda functions with their runtime and last modified date
Write a script that invokes a Lambda function and prints the response payload
Write a script that lists all SNS topics in your account
Write a script that publishes a message to an SNS topic given topic ARN and message as arguments
Write a script that creates a new SNS topic and subscribes an email address to it


Day 21 — Revision Day (Big Project)
Build one complete boto3 monitoring script with all of these requirements:

Accept --region and --threshold as CLI arguments
List all running EC2 instances
Fetch CloudWatch CPU metrics for each instance for last 1 hour
If any instance CPU average is above threshold, send SNS alert
Log all actions to a rotating log file with proper log levels
Handle all boto3 exceptions properly with meaningful error messages
Output a summary JSON report at the end


Day 22 — Decorators & Advanced Python

Write a @retry(times=3, delay=2) decorator that retries a function on exception
Write a @timer decorator that prints how long a function took to execute
Write a @logger decorator that logs function name, arguments, and return value
Write a retry decorator with exponential backoff — 1s, 2s, 4s, 8s delays
Write a @validate_args decorator that checks if arguments to a function are not None


Day 23 — Multithreading

Write a script that checks HTTP health of 10 URLs in parallel using ThreadPoolExecutor
Write a script that runs boto3 describe_instances across 5 regions in parallel using threads
Write a script that SSHs into 10 servers simultaneously and collects uptime from each
Write a script that uses threading with a Queue to process a list of S3 uploads concurrently
Write a script that runs parallel tasks but limits to max 3 concurrent threads at a time


Day 24 — Docker Automation

Write a script using Docker Python SDK to list all running containers with their names and status
Write a script that stops and removes all containers with status "exited"
Write a script that pulls the latest version of a given image
Write a script that restarts a container by name and verifies it is running after restart
Write a script that reads a list of images from a file and pulls all of them in sequence


Day 25 — Kubernetes Automation

Write a script using the kubernetes Python client to list all pods across all namespaces
Write a script that checks if all pods in a given namespace are in Running state
Write a script that lists all deployments and their desired vs available replicas
Write a script that restarts a deployment by patching its annotation
Write a script that watches pod events in real time and logs any pod that goes into CrashLoopBackOff


Day 26 — CI/CD Scripting

Write a script that parses a Jenkins build log file and extracts all failed test names
Write a deployment script that pulls latest Docker image, stops old container, starts new one, verifies health
Write a rollback script that stops current container and starts previous image version
Write a script that checks if a Docker image tag exists in DockerHub before deploying
Write a script that reads a versions.json file and deploys each service at its specified version


Day 27 — Real World Project 1
Build a complete server health report generator:

Read a CSV file containing hostname, username, key_path
SSH into each server using Paramiko
Collect CPU usage, memory usage, disk usage, uptime
Handle connection failures gracefully — mark as unreachable
Generate an HTML report with a table showing all server stats
Color code rows — green if healthy, red if any metric above 80%
Save report as health_report_YYYY-MM-DD.html


Day 28 — Real World Project 2
Build a complete AWS cost and usage report:

Accept --region and --output flags via argparse
List all running EC2 instances with instance type and uptime hours
List all S3 buckets with total size
List all RDS instances with their class and status
Calculate estimated monthly cost for EC2 based on instance type
Generate a JSON report with all findings
Send the report as email attachment using AWS SES


Day 29 — Mock Interview Day
Answer these 10 questions without referring to previous code. Time yourself — max 20 mins each:

Write a script to find all EC2 instances with no tags and stop them after sending SNS alert
Write a retry decorator with exponential backoff and max retries as parameter
Write a multithreaded URL health checker that logs results to file
Parse a Kubernetes YAML, update the replica count, and apply it using subprocess
Write a CLI tool to start/stop/list EC2 instances with proper logging and error handling
Read a log file, extract all ERROR lines with timestamps, write to JSON grouped by date
SSH into a server, check if disk above 90%, if yes archive and delete old logs automatically
Write a script that lists all S3 buckets, checks if versioning is enabled, enables it if not
Write a script that monitors a directory and triggers a function whenever a new file appears
Build a health check script that hits 5 microservice endpoints and sends Slack alert if any is down


Day 30 — Final Revision & Portfolio Cleanup

Review all 30 days of scripts — add missing logging, error handling, docstrings
Make sure every script has argparse — no hardcoded values
Organize all scripts in GitHub with folder structure:

python-devops/
├── file-operations/
├── system-monitoring/
├── aws-boto3/
├── networking/
├── docker-k8s/
└── projects/

Write a proper README for each folder explaining what each script does
Pick your 5 best scripts and add detailed inline comments explaining every section — these are your interview talking points


Golden Rules for all 30 days:

Every script must have proper logging
Every script must have error handling
Every script must use argparse — no hardcoded values
Push to GitHub every single day
Never copy paste — type everything yourself 🚀