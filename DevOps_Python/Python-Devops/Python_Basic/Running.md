# Script 1 — Boto3 Type Validator
pip install boto3
python script1.py --region us-east-1 --state running

# Script 2 — Deployment Decision Engine
python script2.py \
  --branch main \
  --tests-passed true \
  --instance-count 3 \
  --cpu-usage 45.5 \
  --commit-sha abc123def \
  --build-number 42

# Script 3 — Tag Validator
python script3.py \
  --region us-east-1 \
  --resources ec2 s3 \
  --output report.json \
  --fail-on-non-compliant

# Script 4 — Health Monitor
python script4.py \
  --region us-east-1 \
  --instances i-1234567890 i-0987654321 \
  --output health.json \
  --fail-on-critical

# Script 5 — Config Manager
python script5.py --env all --show-diff
python script5.py --env prod --validate-only
python script5.py --env staging --output staging_config.json