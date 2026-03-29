"""
Script 2: CI/CD Deployment Decision Engine
Determines deployment target based on branch name,
test results, and environment conditions.
Uses Python data types and conditional operators.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("deployment.log")
    ]
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# DATA CLASSES
# ──────────────────────────────────────────────

@dataclass
class DeploymentContext:
    """
    Holds all context needed for deployment decision.
    Uses Python dataclass for clean typed structure.
    """
    branch:           str
    tests_passed:     bool
    instance_count:   int
    cpu_usage:        float
    commit_sha:       str
    build_number:     int
    environment:      Optional[str] = None
    deploy_target:    Optional[str] = None
    skip_reason:      Optional[str] = None


@dataclass
class DeploymentResult:
    """
    Holds the result of a deployment decision.
    """
    target:         str
    approved:       bool
    reason:         str
    timestamp:      str
    branch:         str
    commit_sha:     str
    build_number:   int


# ──────────────────────────────────────────────
# VALIDATORS
# ──────────────────────────────────────────────

def validate_branch(branch: str) -> str:
    """
    Validates branch name format.

    Args:
        branch: git branch name
    Returns:
        str: cleaned branch name
    Raises:
        ValueError: if branch is empty or invalid
    """
    if not isinstance(branch, str):
        raise TypeError(
            f"Branch must be string, got: {type(branch).__name__}"
        )

    cleaned = branch.strip()

    if not cleaned:
        raise ValueError("Branch name cannot be empty")

    # ── Valid branch prefixes
    valid_prefixes = (
        "main",
        "master",
        "feature/",
        "hotfix/",
        "release/",
        "fix/",
        "chore/",
        "dependabot/"
    )

    is_valid = any(
        cleaned == prefix or cleaned.startswith(prefix)
        for prefix in valid_prefixes
    )

    if not is_valid:
        logger.warning(f"Non-standard branch name: '{cleaned}'")

    return cleaned


def validate_cpu_usage(cpu: float) -> float:
    """
    Validates CPU usage is within valid range.

    Args:
        cpu: CPU usage percentage
    Returns:
        float: validated CPU usage
    Raises:
        ValueError: if CPU usage is out of range
    """
    try:
        cpu_float = float(cpu)
    except (ValueError, TypeError) as e:
        raise TypeError(f"CPU usage must be numeric, got: '{cpu}'") from e

    if not 0.0 <= cpu_float <= 100.0:
        raise ValueError(
            f"CPU usage must be between 0 and 100, got: {cpu_float}"
        )

    return cpu_float


# ──────────────────────────────────────────────
# DEPLOYMENT DECISION LOGIC
# ──────────────────────────────────────────────

def determine_environment(branch: str) -> str:
    """
    Maps branch name to target environment.

    Args:
        branch: validated git branch name
    Returns:
        str: target environment name
    """
    if branch in ("main", "master"):
        return "production"

    if branch.startswith("release/"):
        return "staging"

    if branch.startswith(("feature/", "fix/", "hotfix/")):
        return "staging"

    if branch.startswith(("chore/", "dependabot/")):
        return "development"

    return "development"


def check_deployment_gates(ctx: DeploymentContext) -> tuple:
    """
    Checks all deployment gates and returns
    approval status with reason.

    Args:
        ctx: DeploymentContext with all deployment info
    Returns:
        tuple: (approved: bool, reason: str)
    """
    environment = ctx.environment

    # ── Production gates — strictest
    if environment == "production":

        if not ctx.tests_passed:
            return False, "Production deploy blocked — tests FAILED"

        if ctx.instance_count <= 0:
            return False, "Production deploy blocked — no healthy instances"

        if ctx.cpu_usage > 80.0:
            return False, (
                f"Production deploy blocked — "
                f"CPU too high: {ctx.cpu_usage}%"
            )

        return True, "All production gates passed"

    # ── Staging gates — moderate
    if environment == "staging":

        if not ctx.tests_passed:
            return False, "Staging deploy blocked — tests FAILED"

        return True, "Staging gates passed"

    # ── Development gates — minimal
    if environment == "development":
        return True, "Development deploy — no gates required"

    return False, f"Unknown environment: {environment}"


def make_deployment_decision(ctx: DeploymentContext) -> DeploymentResult:
    """
    Makes final deployment decision based on all context.

    Args:
        ctx: DeploymentContext
    Returns:
        DeploymentResult: final deployment decision
    """
    logger.info(f"Evaluating deployment for branch: {ctx.branch}")
    logger.info(f"Build: #{ctx.build_number} | Commit: {ctx.commit_sha[:8]}")

    # ── Determine environment
    ctx.environment = determine_environment(ctx.branch)
    logger.info(f"Target environment: {ctx.environment}")

    # ── Check all gates
    approved, reason = check_deployment_gates(ctx)

    result = DeploymentResult(
        target=ctx.environment,
        approved=approved,
        reason=reason,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        branch=ctx.branch,
        commit_sha=ctx.commit_sha,
        build_number=ctx.build_number
    )

    if approved:
        logger.info(f"✅ APPROVED → {ctx.environment.upper()}: {reason}")
    else:
        logger.warning(f"❌ BLOCKED → {ctx.environment.upper()}: {reason}")

    return result


def save_decision(result: DeploymentResult, output_file: str) -> None:
    """
    Saves deployment decision to JSON file for audit trail.

    Args:
        result: DeploymentResult to save
        output_file: path to output JSON file
    """
    data = {
        "timestamp":    result.timestamp,
        "branch":       result.branch,
        "commit_sha":   result.commit_sha,
        "build_number": result.build_number,
        "target":       result.target,
        "approved":     result.approved,
        "reason":       result.reason
    }

    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Decision saved to: {output_file}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="CI/CD Deployment Decision Engine"
    )
    parser.add_argument(
        "--branch",
        required=True,
        help="Git branch name"
    )
    parser.add_argument(
        "--tests-passed",
        required=True,
        help="Whether tests passed: true/false"
    )
    parser.add_argument(
        "--instance-count",
        type=int,
        default=1,
        help="Number of healthy instances (default: 1)"
    )
    parser.add_argument(
        "--cpu-usage",
        type=float,
        default=0.0,
        help="Current CPU usage percentage (default: 0.0)"
    )
    parser.add_argument(
        "--commit-sha",
        default="unknown",
        help="Git commit SHA"
    )
    parser.add_argument(
        "--build-number",
        type=int,
        default=0,
        help="CI build number"
    )
    parser.add_argument(
        "--output",
        default="deployment_decision.json",
        help="Output JSON file for decision audit trail"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # ── Validate and parse inputs
        branch = validate_branch(args.branch)

        # ── Safe bool parsing — "true"/"false" string
        tests_passed_map = {
            "true": True,
            "false": False,
            "1": True,
            "0": False
        }
        tests_passed_str = args.tests_passed.strip().lower()
        if tests_passed_str not in tests_passed_map:
            raise ValueError(
                f"--tests-passed must be true/false, "
                f"got: '{args.tests_passed}'"
            )
        tests_passed = tests_passed_map[tests_passed_str]

        cpu_usage = validate_cpu_usage(args.cpu_usage)

        # ── Build context
        ctx = DeploymentContext(
            branch=branch,
            tests_passed=tests_passed,
            instance_count=int(args.instance_count),
            cpu_usage=cpu_usage,
            commit_sha=args.commit_sha,
            build_number=int(args.build_number)
        )

        # ── Make decision
        result = make_deployment_decision(ctx)

        # ── Save audit trail
        save_decision(result, args.output)

        # ── Print result
        status = "✅ APPROVED" if result.approved else "❌ BLOCKED"
        print(f"\n {status} → {result.target.upper()}")
        print(f" Reason: {result.reason}")
        print(f" Branch: {result.branch}")
        print(f" Build:  #{result.build_number}\n")

        # ── Exit code — 0 approved, 1 blocked
        sys.exit(0 if result.approved else 1)

    except (ValueError, TypeError) as e:
        logger.error(f"Validation error: {e}")
        sys.exit(2)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()