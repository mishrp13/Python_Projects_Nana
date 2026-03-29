"""
Script 4: Infrastructure Health Monitor
Monitors EC2 instances health using Python data
types — dicts, lists, sets, conditionals, and
string operations to build health summary.
"""

import argparse
import json
import logging
import sys
from collections import defaultdict
from datetime import datetime
from typing import Optional

import boto3
from botocore.exceptions import ClientError

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("health_monitor.log")
    ]
)
logger = logging.getLogger(__name__)

# ── Health thresholds
THRESHOLDS = {
    "cpu_warning":    70.0,
    "cpu_critical":   90.0,
    "status_healthy": "ok",
}

# ── Health status levels
HEALTH_LEVELS = {
    "HEALTHY":  0,
    "WARNING":  1,
    "CRITICAL": 2,
    "UNKNOWN":  3
}


# ──────────────────────────────────────────────
# HEALTH CHECKERS
# ──────────────────────────────────────────────

def check_instance_status(
    instance_id: str,
    region: str
) -> dict:
    """
    Checks EC2 instance status checks from AWS.

    Args:
        instance_id: EC2 instance ID
        region: AWS region
    Returns:
        dict: status check results
    """
    ec2 = boto3.client("ec2", region_name=region)

    try:
        response = ec2.describe_instance_status(
            InstanceIds=[instance_id],
            IncludeAllInstances=True
        )

        statuses = response.get("InstanceStatuses", [])

        if not statuses:
            return {
                "instance_status": "unknown",
                "system_status":   "unknown",
                "health_level":    "UNKNOWN"
            }

        status = statuses[0]

        # ── Safely extract status strings
        instance_status = (
            status
            .get("InstanceStatus", {})
            .get("Status", "unknown")
            .lower()
        )
        system_status = (
            status
            .get("SystemStatus", {})
            .get("Status", "unknown")
            .lower()
        )

        # ── Determine health level using conditionals
        if instance_status == "ok" and system_status == "ok":
            health_level = "HEALTHY"
        elif "impaired" in instance_status or "impaired" in system_status:
            health_level = "CRITICAL"
        elif instance_status == "initializing" or system_status == "initializing":
            health_level = "WARNING"
        else:
            health_level = "UNKNOWN"

        return {
            "instance_status": instance_status,
            "system_status":   system_status,
            "health_level":    health_level
        }

    except ClientError as e:
        logger.error(f"Failed to get status for {instance_id}: {e}")
        return {
            "instance_status": "error",
            "system_status":   "error",
            "health_level":    "UNKNOWN"
        }


def check_cloudwatch_cpu(
    instance_id: str,
    region: str,
    period_minutes: int = 5
) -> dict:
    """
    Fetches CPU utilization from CloudWatch.

    Args:
        instance_id: EC2 instance ID
        region: AWS region
        period_minutes: lookback period in minutes
    Returns:
        dict: CPU metrics and health assessment
    """
    from datetime import timedelta

    cw = boto3.client("cloudwatch", region_name=region)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=period_minutes)

    try:
        response = cw.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{
                "Name": "InstanceId",
                "Value": instance_id
            }],
            StartTime=start_time,
            EndTime=end_time,
            Period=period_minutes * 60,
            Statistics=["Average", "Maximum"]
        )

        datapoints = response.get("Datapoints", [])

        if not datapoints:
            return {
                "cpu_average": None,
                "cpu_maximum": None,
                "cpu_health":  "UNKNOWN"
            }

        # ── Get latest datapoint
        latest = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]
        cpu_avg = round(float(latest.get("Average", 0)), 2)
        cpu_max = round(float(latest.get("Maximum", 0)), 2)

        # ── Determine CPU health using conditionals + thresholds
        if cpu_avg >= THRESHOLDS["cpu_critical"]:
            cpu_health = "CRITICAL"
        elif cpu_avg >= THRESHOLDS["cpu_warning"]:
            cpu_health = "WARNING"
        else:
            cpu_health = "HEALTHY"

        return {
            "cpu_average": cpu_avg,
            "cpu_maximum": cpu_max,
            "cpu_health":  cpu_health
        }

    except ClientError as e:
        logger.error(f"Failed to get CPU for {instance_id}: {e}")
        return {
            "cpu_average": None,
            "cpu_maximum": None,
            "cpu_health":  "UNKNOWN"
        }


def assess_overall_health(
    status_check: dict,
    cpu_metrics: dict
) -> str:
    """
    Determines overall health from multiple checks.
    Uses HEALTH_LEVELS dict to find worst status.

    Args:
        status_check: result from check_instance_status
        cpu_metrics: result from check_cloudwatch_cpu
    Returns:
        str: overall health level
    """
    levels = [
        HEALTH_LEVELS.get(status_check["health_level"], 3),
        HEALTH_LEVELS.get(cpu_metrics["cpu_health"], 3)
    ]

    # ── Return worst health level
    worst_level = max(levels)
    return {v: k for k, v in HEALTH_LEVELS.items()}[worst_level]


def monitor_instances(region: str, instance_ids: list) -> list:
    """
    Monitors health of all specified EC2 instances.

    Args:
        region: AWS region
        instance_ids: list of EC2 instance IDs
    Returns:
        list: health results for all instances
    """
    results = []

    for i, instance_id in enumerate(instance_ids, 1):
        logger.info(
            f"Checking {i}/{len(instance_ids)}: {instance_id}"
        )

        status_check = check_instance_status(instance_id, region)
        cpu_metrics = check_cloudwatch_cpu(instance_id, region)
        overall = assess_overall_health(status_check, cpu_metrics)

        result = {
            "instance_id":      instance_id,
            "overall_health":   overall,
            "status_check":     status_check,
            "cpu_metrics":      cpu_metrics,
            "checked_at":       datetime.utcnow().strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        }

        results.append(result)

        icon = {
            "HEALTHY": "✅",
            "WARNING": "⚠️",
            "CRITICAL": "🔴",
            "UNKNOWN": "❓"
        }.get(overall, "❓")

        logger.info(f"{icon} {instance_id}: {overall}")

    return results


def print_health_report(results: list) -> None:
    """Prints formatted health report."""
    by_health = defaultdict(list)
    for r in results:
        by_health[r["overall_health"]].append(r)

    print("\n" + "=" * 65)
    print(" INFRASTRUCTURE HEALTH REPORT")
    print("=" * 65)
    print(f" Total Instances : {len(results)}")
    print(f" Healthy         : {len(by_health['HEALTHY'])}")
    print(f" Warning         : {len(by_health['WARNING'])}")
    print(f" Critical        : {len(by_health['CRITICAL'])}")
    print(f" Unknown         : {len(by_health['UNKNOWN'])}")
    print("=" * 65)

    for result in results:
        health = result["overall_health"]
        cpu = result["cpu_metrics"].get("cpu_average")
        cpu_str = f"{cpu:.1f}%" if cpu is not None else "N/A"

        icon = {
            "HEALTHY":  "✅",
            "WARNING":  "⚠️ ",
            "CRITICAL": "🔴",
            "UNKNOWN":  "❓"
        }.get(health, "❓")

        print(
            f" {icon} {result['instance_id']:<25} "
            f"{health:<10} CPU: {cpu_str}"
        )

    print("=" * 65 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Monitor EC2 instance health"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (default: us-east-1)"
    )
    parser.add_argument(
        "--instances",
        nargs="+",
        required=True,
        help="EC2 instance IDs to monitor"
    )
    parser.add_argument(
        "--output",
        help="Save JSON report to file"
    )
    parser.add_argument(
        "--fail-on-critical",
        action="store_true",
        help="Exit with code 1 if any CRITICAL instances"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # ── Deduplicate instance IDs using set
        unique_instances = list(set(args.instances))
        logger.info(f"Monitoring {len(unique_instances)} instances")

        results = monitor_instances(args.region, unique_instances)

        print_health_report(results)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Report saved: {args.output}")

        critical = [r for r in results if r["overall_health"] == "CRITICAL"]
        if args.fail_on_critical and critical:
            logger.error(f"{len(critical)} CRITICAL instances found")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()