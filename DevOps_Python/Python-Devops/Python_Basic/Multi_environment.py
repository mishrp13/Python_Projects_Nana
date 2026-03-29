"""
Script 5: Multi-Environment Config Manager
Manages configuration across dev/staging/prod
environments using Python dicts, type validation,
string operations, and conditional logic.
Simulates reading config, validating types,
and applying environment-specific overrides.
"""

import argparse
import json
import logging
import os
import sys
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("config_manager.log")
    ]
)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# CONFIG SCHEMA
# ──────────────────────────────────────────────

@dataclass
class DatabaseConfig:
    host:             str
    port:             int
    name:             str
    max_connections:  int
    ssl_enabled:      bool


@dataclass
class AppConfig:
    instance_type:    str
    min_replicas:     int
    max_replicas:     int
    cpu_threshold:    float
    debug_mode:       bool
    allowed_regions:  list
    feature_flags:    dict


@dataclass
class EnvironmentConfig:
    environment:  str
    aws_region:   str
    database:     DatabaseConfig
    app:          AppConfig
    tags:         dict = field(default_factory=dict)


# ──────────────────────────────────────────────
# BASE CONFIG TEMPLATES
# ──────────────────────────────────────────────

BASE_CONFIG = {
    "aws_region": "us-east-1",
    "database": {
        "host":            "localhost",
        "port":            5432,
        "name":            "appdb",
        "max_connections": 10,
        "ssl_enabled":     True
    },
    "app": {
        "instance_type":   "t3.micro",
        "min_replicas":    1,
        "max_replicas":    3,
        "cpu_threshold":   80.0,
        "debug_mode":      False,
        "allowed_regions": ["us-east-1"],
        "feature_flags": {
            "new_dashboard":    False,
            "dark_mode":        False,
            "beta_api":         False
        }
    }
}

# ── Environment specific overrides
ENV_OVERRIDES = {
    "dev": {
        "database": {
            "host":            "dev-db.internal",
            "max_connections": 5,
            "ssl_enabled":     False
        },
        "app": {
            "instance_type":   "t3.micro",
            "min_replicas":    1,
            "max_replicas":    2,
            "debug_mode":      True,
            "feature_flags": {
                "new_dashboard": True,
                "dark_mode":     True,
                "beta_api":      True
            }
        }
    },
    "staging": {
        "database": {
            "host":            "staging-db.internal",
            "max_connections": 20,
            "ssl_enabled":     True
        },
        "app": {
            "instance_type":   "t3.small",
            "min_replicas":    1,
            "max_replicas":    5,
            "debug_mode":      False,
            "feature_flags": {
                "new_dashboard": True,
                "dark_mode":     False,
                "beta_api":      False
            }
        }
    },
    "prod": {
        "database": {
            "host":            "prod-db.internal",
            "max_connections": 100,
            "ssl_enabled":     True
        },
        "app": {
            "instance_type":   "t3.large",
            "min_replicas":    3,
            "max_replicas":    20,
            "cpu_threshold":   70.0,
            "debug_mode":      False,
            "allowed_regions": [
                "us-east-1",
                "us-west-2",
                "eu-west-1"
            ],
            "feature_flags": {
                "new_dashboard": False,
                "dark_mode":     False,
                "beta_api":      False
            }
        }
    }
}


# ──────────────────────────────────────────────
# CONFIG MERGER AND VALIDATOR
# ──────────────────────────────────────────────

def deep_merge(base: dict, override: dict) -> dict:
    """
    Deep merges override dict into base dict.
    Override values take precedence.

    Args:
        base: base configuration dict
        override: override values dict
    Returns:
        dict: merged configuration
    """
    result = deepcopy(base)

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)

    return result


def validate_config_types(config: dict, env: str) -> list:
    """
    Validates all config values have correct types.
    Catches type mismatches before they cause runtime bugs.

    Args:
        config: merged config dict
        env: environment name
    Returns:
        list: list of validation errors
    """
    errors = []

    # ── Database validations
    db = config.get("database", {})

    if not isinstance(db.get("port"), int):
        errors.append(
            f"database.port must be int, "
            f"got: {type(db.get('port')).__name__}"
        )

    if not isinstance(db.get("max_connections"), int):
        errors.append(
            f"database.max_connections must be int, "
            f"got: {type(db.get('max_connections')).__name__}"
        )

    if not isinstance(db.get("ssl_enabled"), bool):
        errors.append(
            f"database.ssl_enabled must be bool, "
            f"got: {type(db.get('ssl_enabled')).__name__}"
        )

    # ── CRITICAL: check for string "False" instead of bool False
    ssl_raw = db.get("ssl_enabled")
    if isinstance(ssl_raw, str):
        errors.append(
            f"database.ssl_enabled is string '{ssl_raw}' "
            f"not bool — 'False' string is TRUTHY in Python!"
        )

    # ── App validations
    app = config.get("app", {})

    if not isinstance(app.get("min_replicas"), int):
        errors.append(
            f"app.min_replicas must be int, "
            f"got: {type(app.get('min_replicas')).__name__}"
        )

    if not isinstance(app.get("max_replicas"), int):
        errors.append(
            f"app.max_replicas must be int, "
            f"got: {type(app.get('max_replicas')).__name__}"
        )

    if not isinstance(app.get("cpu_threshold"), (int, float)):
        errors.append(
            f"app.cpu_threshold must be numeric, "
            f"got: {type(app.get('cpu_threshold')).__name__}"
        )

    if not isinstance(app.get("debug_mode"), bool):
        errors.append(
            f"app.debug_mode must be bool, "
            f"got: {type(app.get('debug_mode')).__name__}"
        )

    # ── Production-specific validations
    if env == "prod":
        if app.get("debug_mode") is True:
            errors.append(
                "SECURITY: debug_mode must be False in production"
            )

        if not db.get("ssl_enabled"):
            errors.append(
                "SECURITY: ssl_enabled must be True in production"
            )

        min_r = app.get("min_replicas", 0)
        if isinstance(min_r, int) and min_r < 2:
            errors.append(
                f"Production min_replicas must be >= 2, got: {min_r}"
            )

    return errors


def build_environment_config(env: str) -> dict:
    """
    Builds complete config for given environment
    by merging base config with env overrides.

    Args:
        env: environment name (dev/staging/prod)
    Returns:
        dict: complete merged and validated config
    Raises:
        ValueError: if environment is unknown
        TypeError: if config validation fails
    """
    valid_envs = {"dev", "staging", "prod"}

    if env not in valid_envs:
        raise ValueError(
            f"Unknown environment: '{env}'. "
            f"Must be one of: {sorted(valid_envs)}"
        )

    logger.info(f"Building config for environment: {env}")

    # ── Merge base with environment overrides
    overrides = ENV_OVERRIDES.get(env, {})
    merged = deep_merge(BASE_CONFIG, overrides)

    # ── Validate types
    errors = validate_config_types(merged, env)

    if errors:
        for error in errors:
            logger.error(f"Config validation error: {error}")
        raise TypeError(
            f"Config validation failed for '{env}' "
            f"with {len(errors)} error(s)"
        )

    # ── Add metadata
    merged["environment"] = env
    merged["tags"] = {
        "Environment": env,
        "ManagedBy":   "ConfigManager",
        "Project":     "banking"
    }

    logger.info(f"Config built successfully for: {env}")
    return merged


def print_config_diff(dev: dict, prod: dict) -> None:
    """
    Prints key differences between dev and prod configs.

    Args:
        dev: dev environment config
        prod: prod environment config
    """
    print("\n" + "=" * 60)
    print(" CONFIG DIFF: dev vs prod")
    print("=" * 60)

    comparisons = [
        ("instance_type",   dev["app"]["instance_type"],
                            prod["app"]["instance_type"]),
        ("min_replicas",    dev["app"]["min_replicas"],
                            prod["app"]["min_replicas"]),
        ("max_replicas",    dev["app"]["max_replicas"],
                            prod["app"]["max_replicas"]),
        ("cpu_threshold",   dev["app"]["cpu_threshold"],
                            prod["app"]["cpu_threshold"]),
        ("debug_mode",      dev["app"]["debug_mode"],
                            prod["app"]["debug_mode"]),
        ("ssl_enabled",     dev["database"]["ssl_enabled"],
                            prod["database"]["ssl_enabled"]),
        ("max_connections", dev["database"]["max_connections"],
                            prod["database"]["max_connections"]),
    ]

    print(f" {'Setting':<20} {'DEV':<15} {'PROD':<15}")
    print("-" * 60)
    for setting, dev_val, prod_val in comparisons:
        diff_marker = "⚠️ " if dev_val != prod_val else "  "
        print(
            f" {diff_marker}{setting:<18} "
            f"{str(dev_val):<15} "
            f"{str(prod_val):<15}"
        )

    print("=" * 60 + "\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-environment config manager"
    )
    parser.add_argument(
        "--env",
        required=True,
        choices=["dev", "staging", "prod", "all"],
        help="Target environment"
    )
    parser.add_argument(
        "--output",
        help="Save config to JSON file"
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Show diff between dev and prod"
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate config, don't print"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        envs_to_build = (
            ["dev", "staging", "prod"]
            if args.env == "all"
            else [args.env]
        )

        configs = {}
        for env in envs_to_build:
            config = build_environment_config(env)
            configs[env] = config
            logger.info(f"✅ Config valid for: {env}")

        if args.validate_only:
            print(f"\n All configs valid: {', '.join(envs_to_build)}\n")
            sys.exit(0)

        # ── Print configs
        for env, config in configs.items():
            print(f"\n{'=' * 60}")
            print(f" CONFIG: {env.upper()}")
            print(f"{'=' * 60}")
            print(json.dumps(config, indent=2))

        # ── Show diff if requested
        if args.show_diff and "dev" in configs and "prod" in configs:
            print_config_diff(configs["dev"], configs["prod"])

        # ── Save to file
        if args.output:
            output_data = (
                configs if args.env == "all"
                else configs[args.env]
            )
            with open(args.output, "w") as f:
                json.dump(output_data, f, indent=2)
            logger.info(f"Config saved to: {args.output}")

    except (ValueError, TypeError) as e:
        logger.error(f"Config error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()