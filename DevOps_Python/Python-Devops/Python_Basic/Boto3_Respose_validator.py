"""
Script 1: Boto3 Response Type Validator
Safely extracts and validates EC2 instance data
from Boto3 API responses — prevents silent type bugs
"""

import argparse
import logging
import sys
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("boto3_validator.log")
    ]
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# TYPE VALIDATORS
# ──────────────────────────────────────────────

def safe_int(value: Any, field_name: str) -> int:
    """
    Safely converts a value to integer.
    Prevents silent bugs where '0' is treated as truthy.

    Args:
        value: value to convert
        field_name: name of field for error message
    Returns:
        int: converted integer value
    Raises:
        TypeError: if value cannot be converted to int
    """
    if value is None:
        raise TypeError(f"Field '{field_name}' is None — cannot convert to int")

    try:
        return int(value)
    except (ValueError, TypeError) as e:
        raise TypeError(
            f"Field '{field_name}' expected int-compatible value, "
            f"got: '{value}' (type: {type(value).__name__})"
        ) from e


def safe_str(value: Any, field_name: str) -> str:
    """
    Safely converts a value to string and validates
    it is not empty.

    Args:
        value: value to convert
        field_name: name of field for error message
    Returns:
        str: cleaned string value
    Raises:
        ValueError: if value is empty or None
    """
    if value is None:
        raise ValueError(f"Field '{field_name}' is None")

    result = str(value).strip()

    if not result:
        raise ValueError(f"Field '{field_name}' is empty string")

    return result


def safe_bool(value: Any, field_name: str) -> bool:
    """
    Safely parses boolean from various formats.
    Handles: True, False, 'true', 'false', '1', '0', 'yes', 'no'

    Args:
        value: value to parse as bool
        field_name: name of field for error message
    Returns:
        bool: parsed boolean value
    Raises:
        ValueError: if value cannot be interpreted as bool
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return value != 0

    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ("true", "1", "yes", "enabled"):
            return True
        if normalized in ("false", "0", "no", "disabled"):
            return False

    raise ValueError(
        f"Field '{field_name}' cannot be parsed as bool: "
        f"'{value}' (type: {type(value).__name__})"
    )


# ──────────────────────────────────────────────
# EC2 RESPONSE PARSER
# ──────────────────────────────────────────────

def parse_ec2_instance(raw: dict) -> dict:
    """
    Safely parses and type-validates an EC2 instance
    from Boto3 describe_instances response.

    Args:
        raw: raw EC2 instance dict from Boto3
    Returns:
        dict: validated and typed instance data
    Raises:
        TypeError: if required fields have wrong types
        KeyError: if required fields are missing
    """
    required_fields = [
        "InstanceId",
        "InstanceType",
        "State",
    ]

    # ── Check required fields exist
    for field in required_fields:
        if field not in raw:
            raise KeyError(f"Required field missing: '{field}'")

    # ── Parse state safely
    state_name = raw.get("State", {}).get("Name", "unknown")

    # ── Parse tags safely
    tags = {}
    for tag in raw.get("Tags", []):
        key = safe_str(tag.get("Key", ""), "tag_key")
        val = str(tag.get("Value", ""))
        tags[key] = val

    # ── Parse CPU options safely
    cpu_options = raw.get("CpuOptions", {})
    core_count = safe_int(
        cpu_options.get("CoreCount", 0),
        "CoreCount"
    )
    threads_per_core = safe_int(
        cpu_options.get("ThreadsPerCore", 1),
        "ThreadsPerCore"
    )

    # ── Build validated instance dict
    instance = {
        "instance_id":        safe_str(raw["InstanceId"], "InstanceId"),
        "instance_type":      safe_str(raw["InstanceType"], "InstanceType"),
        "state":              safe_str(state_name, "State.Name"),
        "is_running":         state_name == "running",
        "public_ip":          raw.get("PublicIpAddress", None),
        "private_ip":         raw.get("PrivateIpAddress", None),
        "az":                 raw.get("Placement", {}).get("AvailabilityZone", "unknown"),
        "core_count":         core_count,
        "threads_per_core":   threads_per_core,
        "tags":               tags,
        "environment":        tags.get("Environment", "unknown"),
        "name":               tags.get("Name", "unnamed"),
    }

    logger.debug(f"Parsed instance: {instance['instance_id']} — {instance['state']}")
    return instance


def fetch_ec2_instances(region: str, filters: list = None) -> list:
    """
    Fetches EC2 instances from AWS using Boto3.

    Args:
        region: AWS region
        filters: optional list of Boto3 filters
    Returns:
        list: validated list of parsed EC2 instances
    Raises:
        ClientError: if AWS API call fails
    """
    logger.info(f"Fetching EC2 instances in region: {region}")

    ec2 = boto3.client("ec2", region_name=region)

    kwargs = {}
    if filters:
        kwargs["Filters"] = filters

    try:
        response = ec2.describe_instances(**kwargs)
    except ClientError as e:
        raise ClientError(
            e.response,
            f"Failed to describe instances: {e}"
        )

    instances = []
    for reservation in response.get("Reservations", []):
        for raw_instance in reservation.get("Instances", []):
            try:
                parsed = parse_ec2_instance(raw_instance)
                instances.append(parsed)
            except (TypeError, ValueError, KeyError) as e:
                logger.warning(
                    f"Skipping malformed instance: {e}"
                )

    logger.info(f"Successfully parsed {len(instances)} instances")
    return instances


def print_instance_report(instances: list) -> None:
    """
    Prints a formatted report of EC2 instances.

    Args:
        instances: list of parsed instance dicts
    """
    running = [i for i in instances if i["is_running"]]
    stopped = [i for i in instances if not i["is_running"]]

    print("\n" + "=" * 70)
    print(" EC2 INSTANCE REPORT")
    print("=" * 70)
    print(f" Total    : {len(instances)}")
    print(f" Running  : {len(running)}")
    print(f" Stopped  : {len(stopped)}")
    print("=" * 70)

    for instance in instances:
        status = "✅ RUNNING" if instance["is_running"] else "🔴 STOPPED"
        print(
            f" {status:<15} "
            f"{instance['instance_id']:<22} "
            f"{instance['instance_type']:<12} "
            f"{instance['name']:<20} "
            f"{instance['environment']}"
        )

    print("=" * 70 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch and validate EC2 instances from Boto3"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--state",
        choices=["running", "stopped", "all"],
        default="all",
        help="Filter by instance state"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    filters = []
    if args.state != "all":
        filters.append({
            "Name": "instance-state-name",
            "Values": [args.state]
        })

    try:
        instances = fetch_ec2_instances(args.region, filters or None)
        print_instance_report(instances)

    except ClientError as e:
        logger.error(f"AWS error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()