1. Core Data Types
python# ── String
hostname = "web-01"
region   = "us-east-1"
branch   = "feature/login"

# ── Integer
port         = 8080
min_replicas = 1
max_replicas = 10

# ── Float
cpu_threshold    = 80.5
memory_threshold = 75.0

# ── Boolean
is_production = True
tests_passed  = False
multi_az      = True

# ── None (absence of value)
instance_id = None
error       = None

# ── List (ordered, mutable)
availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
security_groups    = ["sg-001", "sg-002"]

# ── Tuple (ordered, immutable)
allowed_regions  = ("us-east-1", "us-west-2")
valid_envs       = ("dev", "staging", "prod")

# ── Dictionary (key-value pairs)
instance = {
    "id":           "i-1234567890",
    "type":         "t3.micro",
    "state":        "running",
    "region":       "us-east-1",
    "tags":         {"env": "prod", "team": "devops"}
}

# ── Set (unique values, unordered)
unique_regions = {"us-east-1", "us-west-2", "us-east-1"}
# → {"us-east-1", "us-west-2"}  duplicates removed

2. Type Checking — Critical for Boto3
python# ── Check type
print(type("web-01"))       # <class 'str'>
print(type(8080))           # <class 'int'>
print(type(True))           # <class 'bool'>
print(type(None))           # <class 'NoneType'>
print(type([]))             # <class 'list'>
print(type({}))             # <class 'dict'>

# ── isinstance() — preferred way to check type
value = "80"

if isinstance(value, str):
    print("It's a string")
elif isinstance(value, int):
    print("It's an integer")

# ── Check multiple types at once
def validate_port(port):
    if not isinstance(port, (int, float)):
        raise TypeError(f"Port must be int or float, got: {type(port).__name__}")
    return port

3. The Silent Bug — String vs Integer in Boto3
pythonimport boto3

# ── Boto3 sometimes returns numbers as strings
# This is the DANGEROUS pattern

# ❌ WRONG — silent bug
response = {
    "InstanceCount": "0",   # Boto3 returned string "0" not int 0
    "RunningInstances": "3"
}

instance_count = response["InstanceCount"]

# "0" is a non-empty string → Python treats it as TRUTHY
if instance_count:
    print("Instances are running")   # ← THIS RUNS EVEN THOUGH COUNT IS 0!
    # BUG: deploys when it shouldn't

# ✅ CORRECT — always convert and validate type
instance_count = int(response["InstanceCount"])

if instance_count > 0:
    print("Instances are running")   # ← Only runs when actually > 0
else:
    print("No instances running — skipping deployment")

4. Truthy and Falsy Values — Know These Cold
python# ── FALSY values in Python (evaluate to False)
bool(0)          # False  ← integer zero
bool(0.0)        # False  ← float zero
bool("")         # False  ← empty string
bool([])         # False  ← empty list
bool({})         # False  ← empty dict
bool(set())      # False  ← empty set
bool(None)       # False  ← None

# ── TRUTHY values (evaluate to True)
bool(1)          # True
bool(-1)         # True  ← any non-zero number
bool("0")        # True  ← non-empty STRING including "0"!
bool("False")    # True  ← non-empty string!
bool([0])        # True  ← list with one item
bool({"a": 1})   # True  ← non-empty dict

# ── THE DANGEROUS ONES in DevOps scripts
status = "0"        # returned from API as string
if status:
    print("Truthy!")    # ← RUNS! "0" is truthy as string

count = 0           # integer zero
if count:
    print("Truthy!")    # ← Does NOT run. 0 is falsy

# ── CORRECT pattern for API responses
def is_healthy(instance_count):
    """Always convert before comparing"""
    count = int(instance_count)   # convert string to int first
    return count > 0

5. Type Conversion
python# ── str to int
port = int("8080")          # 8080
count = int("0")            # 0  ← now correctly falsy

# ── str to float
threshold = float("80.5")   # 80.5

# ── int to str
instance_num = str(42)      # "42"

# ── str to bool — NEVER do this directly
bool("False")   # True  ← WRONG! non-empty string is truthy

# ── CORRECT way to parse bool from string
def parse_bool(value: str) -> bool:
    """
    Safely parse boolean from string.
    Handles: "true", "True", "TRUE", "1", "yes"
    """
    return str(value).lower() in ("true", "1", "yes")

parse_bool("true")    # True  ✅
parse_bool("True")    # True  ✅
parse_bool("false")   # False ✅
parse_bool("0")       # False ✅
parse_bool("False")   # False ✅

# ── list to set (remove duplicates)
regions = ["us-east-1", "us-west-2", "us-east-1"]
unique  = list(set(regions))   # ["us-east-1", "us-west-2"]

# ── dict keys/values to list
instance = {"id": "i-123", "type": "t3.micro", "state": "running"}
keys   = list(instance.keys())    # ["id", "type", "state"]
values = list(instance.values())  # ["i-123", "t3.micro", "running"]

6. String Operations — Critical for DevOps
pythonbranch  = "feature/login-page"
region  = "us-east-1"
env     = "  production  "

# ── Check prefix/suffix
branch.startswith("feature/")   # True
branch.startswith("main")       # False
branch.endswith(".yaml")        # False

# ── Contains
"feature" in branch             # True
"main" in branch                # False

# ── Split
parts = branch.split("/")       # ["feature", "login-page"]
region_parts = region.split("-")# ["us", "east", "1"]

# ── Strip whitespace (common in config file parsing)
clean_env = env.strip()         # "production"

# ── Upper/Lower
branch.upper()    # "FEATURE/LOGIN-PAGE"
branch.lower()    # "feature/login-page"

# ── Replace
new_branch = branch.replace("feature/", "")  # "login-page"

# ── f-strings (always use these)
instance_type = "t3.micro"
environment   = "prod"
name = f"{environment}-{instance_type}-server"
# → "prod-t3.micro-server"

# ── Format with padding (useful for log formatting)
status = f"{'RUNNING':<10} {'i-1234567890':>15}"
# → "RUNNING     i-1234567890"

7. Conditional Operators
python# ── Basic comparison
x = 5
x == 5      # True   equal
x != 5      # False  not equal
x > 3       # True   greater than
x < 3       # False  less than
x >= 5      # True   greater than or equal
x <= 5      # True   less than or equal

# ── Logical operators
True and True    # True
True and False   # False
True or False    # True
not True         # False

# ── Identity operators
x = None
x is None        # True   ← use this for None checks
x is not None    # False

# ── Membership operators
"us-east-1" in ["us-east-1", "us-west-2"]    # True
"eu-west-1" not in ["us-east-1", "us-west-2"] # True

# ── Ternary (inline if/else)
env = "prod" if branch == "main" else "staging"
instance_type = "t3.large" if env == "prod" else "t3.micro"

8. Real DevOps Use Case — Deployment Branch Logic
pythonimport logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def determine_deployment_target(
    branch: str,
    tests_passed: bool,
    instance_count: str   # comes as string from API
) -> str:
    """
    Determines deployment target based on branch,
    test results and current instance count.

    Args:
        branch: git branch name
        tests_passed: whether all tests passed
        instance_count: current running instances (string from API)
    Returns:
        str: deployment target — staging, production, or skip
    Raises:
        ValueError: if branch is empty
        TypeError: if instance_count cannot be converted to int
    """
    # ── Validate inputs
    if not isinstance(branch, str) or not branch.strip():
        raise ValueError(f"Invalid branch: '{branch}'")

    if not isinstance(tests_passed, bool):
        raise TypeError(
            f"tests_passed must be bool, got: {type(tests_passed).__name__}"
        )

    # ── Convert instance_count from string to int safely
    try:
        count = int(instance_count)
    except (ValueError, TypeError) as e:
        raise TypeError(
            f"instance_count must be numeric string, got: '{instance_count}'"
        ) from e

    logger.info(f"Branch: {branch}")
    logger.info(f"Tests passed: {tests_passed}")
    logger.info(f"Running instances: {count}")

    # ── Deployment logic

    # Production — only from main + all tests pass
    if branch == "main" and tests_passed and count > 0:
        logger.info("All conditions met → deploying to PRODUCTION")
        return "production"

    # Main branch but tests failed
    if branch == "main" and not tests_passed:
        logger.warning("Main branch but tests FAILED → skipping deployment")
        return "skip"

    # Feature branch → staging
    if branch.startswith("feature/"):
        logger.info("Feature branch → deploying to STAGING")
        return "staging"

    # Hotfix branch → staging first
    if branch.startswith("hotfix/"):
        logger.info("Hotfix branch → deploying to STAGING for review")
        return "staging"

    # Release branch → staging
    if branch.startswith("release/"):
        logger.info("Release branch → deploying to STAGING")
        return "staging"

    # Any other branch → skip
    logger.info(f"Branch '{branch}' not configured for deployment → skip")
    return "skip"


def deploy(target: str, branch: str) -> None:
    """
    Executes deployment to target environment.

    Args:
        target: deployment target (staging/production/skip)
        branch: git branch name
    """
    if target == "skip":
        logger.info("Deployment skipped")
        return

    logger.info(f"Starting deployment to {target.upper()}...")
    logger.info(f"Branch: {branch}")
    logger.info(f"Target: {target}")

    # ── Add real deployment logic here
    # e.g. boto3 calls, kubectl commands, etc.

    logger.info(f"Deployment to {target.upper()} completed")


def main():
    # ── Simulate values coming from CI/CD environment
    # These would come from env vars or API calls in real usage

    test_cases = [
        # (branch,            tests_passed, instance_count)
        ("main",              True,         "3"),   # → production
        ("main",              False,        "3"),   # → skip
        ("feature/login",     True,         "0"),   # → staging
        ("feature/payments",  False,        "2"),   # → staging
        ("hotfix/critical",   True,         "5"),   # → staging
        ("release/v2.0",      True,         "3"),   # → staging
        ("dependabot/update", True,         "2"),   # → skip
    ]

    print("\n" + "=" * 60)
    print(" DEPLOYMENT DECISION ENGINE")
    print("=" * 60)

    for branch, tests_passed, instance_count in test_cases:
        try:
            target = determine_deployment_target(
                branch,
                tests_passed,
                instance_count
            )
            deploy(target, branch)
            print(
                f" {branch:<30} → "
                f"{'✅' if target != 'skip' else '⏭️ '} "
                f"{target.upper()}"
            )

        except (ValueError, TypeError) as e:
            logger.error(f"Validation error: {e}")
            sys.exit(1)

    print("=" * 60)


if __name__ == "__main__":
    main()
```

---

**Sample output:**
```
============================================================
 DEPLOYMENT DECISION ENGINE
============================================================
 main                           → ✅ PRODUCTION
 main                           → ⏭️  SKIP
 feature/login                  → ✅ STAGING
 feature/payments               → ✅ STAGING
 hotfix/critical                → ✅ STAGING
 release/v2.0                   → ✅ STAGING
 dependabot/update              → ⏭️  SKIP
============================================================

Key concepts summary — remember for interview:
ConceptDevOps relevanceisinstance()Validate Boto3 response types before usingint("0") == 0Convert string numbers from APIs before comparingbool("0") == TrueNon-empty string is always truthy — dangerous in conditionalsstr.startswith()Branch name matching in CI/CD logicx is NoneAlways use is for None checks, never ==parse_bool()Never directly cast string to boolin operatorCheck membership in allowed regions, envs, branchesTernary operatorClean one-line conditionals for env selection