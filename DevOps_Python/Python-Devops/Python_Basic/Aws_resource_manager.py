"""
Script 3: AWS Resource Tag Validator
Validates all AWS resources have required tags.
Uses Python data types — dicts, sets, lists,
string operations, and conditional logic.
"""

import argparse
import json
import logging
import sys
from collections import defaultdict
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("tag_validator.log")
    ]
)
logger = logging.getLogger(__name__)

# ── Required tags for all resources
REQUIRED_TAGS = {
    "Environment",
    "Project",
    "Team",
    "ManagedBy"
}

# ── Valid values for specific tags
VALID_TAG_VALUES = {
    "Environment": {"dev", "staging", "prod"},
    "ManagedBy":   {"Terraform", "Manual", "CloudFormation"}
}


# ──────────────────────────────────────────────
# TAG VALIDATORS
# ──────────────────────────────────────────────

def parse_tags(raw_tags: list) -> dict:
    """
    Converts Boto3 tags list to clean dict.
    Handles None and empty tags safely.

    Args:
        raw_tags: list of {"Key": k, "Value": v} dicts
    Returns:
        dict: clean {key: value} tag dict
    """
    if not raw_tags:
        return {}

    tags = {}
    for tag in raw_tags:
        key = str(tag.get("Key", "")).strip()
        value = str(tag.get("Value", "")).strip()
        if key:
            tags[key] = value

    return tags


def validate_tags(
    resource_id: str,
    resource_type: str,
    tags: dict
) -> dict:
    """
    Validates resource tags against required tag policy.

    Args:
        resource_id: AWS resource ID
        resource_type: type of resource (EC2, S3, etc.)
        tags: dict of resource tags
    Returns:
        dict: validation result with issues found
    """
    issues = []

    # ── Check required tags exist
    existing_keys = set(tags.keys())
    missing_tags = REQUIRED_TAGS - existing_keys

    if missing_tags:
        issues.append({
            "type": "MISSING_TAGS",
            "detail": f"Missing required tags: {sorted(missing_tags)}"
        })

    # ── Check tag values are valid
    for tag_key, valid_values in VALID_TAG_VALUES.items():
        if tag_key in tags:
            tag_value = tags[tag_key]
            if tag_value not in valid_values:
                issues.append({
                    "type": "INVALID_TAG_VALUE",
                    "detail": (
                        f"Tag '{tag_key}' has invalid value: "
                        f"'{tag_value}'. "
                        f"Allowed: {sorted(valid_values)}"
                    )
                })

    # ── Check for empty tag values
    for key, value in tags.items():
        if not value:
            issues.append({
                "type": "EMPTY_TAG_VALUE",
                "detail": f"Tag '{key}' has empty value"
            })

    return {
        "resource_id":   resource_id,
        "resource_type": resource_type,
        "tags":          tags,
        "is_compliant":  len(issues) == 0,
        "issues":        issues
    }


# ──────────────────────────────────────────────
# AWS RESOURCE FETCHERS
# ──────────────────────────────────────────────

def fetch_ec2_tags(region: str) -> list:
    """
    Fetches all EC2 instances and their tags.

    Args:
        region: AWS region
    Returns:
        list: list of validation results
    """
    logger.info(f"Fetching EC2 instances in {region}...")
    ec2 = boto3.client("ec2", region_name=region)

    results = []
    try:
        response = ec2.describe_instances()
        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance.get("InstanceId", "unknown")
                raw_tags = instance.get("Tags", [])
                tags = parse_tags(raw_tags)
                result = validate_tags(
                    instance_id,
                    "EC2",
                    tags
                )
                results.append(result)

    except ClientError as e:
        logger.error(f"Failed to fetch EC2 instances: {e}")

    logger.info(f"Fetched {len(results)} EC2 instances")
    return results


def fetch_s3_tags(region: str) -> list:
    """
    Fetches all S3 buckets and their tags.

    Args:
        region: AWS region
    Returns:
        list: list of validation results
    """
    logger.info("Fetching S3 buckets...")
    s3 = boto3.client("s3", region_name=region)

    results = []
    try:
        buckets = s3.list_buckets().get("Buckets", [])
        for bucket in buckets:
            bucket_name = bucket.get("Name", "unknown")
            try:
                tag_response = s3.get_bucket_tagging(Bucket=bucket_name)
                raw_tags = tag_response.get("TagSet", [])
            except ClientError as e:
                if e.response["Error"]["Code"] == "NoSuchTagSet":
                    raw_tags = []
                else:
                    logger.warning(
                        f"Failed to get tags for bucket "
                        f"{bucket_name}: {e}"
                    )
                    continue

            tags = parse_tags(raw_tags)
            result = validate_tags(bucket_name, "S3", tags)
            results.append(result)

    except ClientError as e:
        logger.error(f"Failed to fetch S3 buckets: {e}")

    logger.info(f"Fetched {len(results)} S3 buckets")
    return results


# ──────────────────────────────────────────────
# REPORT GENERATOR
# ──────────────────────────────────────────────

def generate_compliance_report(
    all_results: list,
    output_file: Optional[str] = None
) -> dict:
    """
    Generates compliance report from all validation results.

    Args:
        all_results: list of all validation results
        output_file: optional path to save JSON report
    Returns:
        dict: summary report
    """
    total = len(all_results)
    compliant = [r for r in all_results if r["is_compliant"]]
    non_compliant = [r for r in all_results if not r["is_compliant"]]

    # ── Group by resource type
    by_type = defaultdict(lambda: {"total": 0, "compliant": 0})
    for result in all_results:
        rtype = result["resource_type"]
        by_type[rtype]["total"] += 1
        if result["is_compliant"]:
            by_type[rtype]["compliant"] += 1

    # ── Group issues by type
    issue_counts = defaultdict(int)
    for result in non_compliant:
        for issue in result["issues"]:
            issue_counts[issue["type"]] += 1

    report = {
        "summary": {
            "total_resources":     total,
            "compliant":           len(compliant),
            "non_compliant":       len(non_compliant),
            "compliance_rate":     f"{(len(compliant)/total*100):.1f}%" if total > 0 else "0%"
        },
        "by_resource_type": dict(by_type),
        "issue_breakdown":  dict(issue_counts),
        "non_compliant_resources": non_compliant
    }

    if output_file:
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)
        logger.info(f"Report saved to: {output_file}")

    return report


def print_report(report: dict) -> None:
    """Prints formatted compliance report to console."""
    summary = report["summary"]

    print("\n" + "=" * 60)
    print(" AWS TAG COMPLIANCE REPORT")
    print("=" * 60)
    print(f" Total Resources  : {summary['total_resources']}")
    print(f" Compliant        : {summary['compliant']}")
    print(f" Non-Compliant    : {summary['non_compliant']}")
    print(f" Compliance Rate  : {summary['compliance_rate']}")
    print("=" * 60)

    if report["issue_breakdown"]:
        print("\n Issue Breakdown:")
        for issue_type, count in report["issue_breakdown"].items():
            print(f"   {issue_type:<25} : {count}")

    if report["non_compliant_resources"]:
        print("\n Non-Compliant Resources:")
        for r in report["non_compliant_resources"]:
            print(f"\n   {r['resource_type']}: {r['resource_id']}")
            for issue in r["issues"]:
                print(f"     ⚠️  {issue['detail']}")

    print("\n" + "=" * 60 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate AWS resource tags for compliance"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--resources",
        nargs="+",
        choices=["ec2", "s3", "all"],
        default=["all"],
        help="Resource types to check (default: all)"
    )
    parser.add_argument(
        "--output",
        help="Save JSON report to file"
    )
    parser.add_argument(
        "--fail-on-non-compliant",
        action="store_true",
        help="Exit with code 1 if any non-compliant resources found"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    all_results = []

    try:
        check_all = "all" in args.resources

        if check_all or "ec2" in args.resources:
            all_results.extend(fetch_ec2_tags(args.region))

        if check_all or "s3" in args.resources:
            all_results.extend(fetch_s3_tags(args.region))

        if not all_results:
            logger.warning("No resources found to validate")
            sys.exit(0)

        report = generate_compliance_report(
            all_results,
            args.output
        )
        print_report(report)

        non_compliant_count = report["summary"]["non_compliant"]
        if args.fail_on_non_compliant and non_compliant_count > 0:
            logger.error(
                f"{non_compliant_count} non-compliant resources found"
            )
            sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()