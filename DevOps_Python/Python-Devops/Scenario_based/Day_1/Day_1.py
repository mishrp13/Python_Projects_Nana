# You are a DevOps engineer at a fintech company.
# Every night a batch job runs and generates a log file
# called app.log on 10 different servers.

# Your task is to write a Python script that:

# 1. Reads a CSV file called servers.csv which contains:
#    hostname, username, key_path

# 2. SSHs into each server using Paramiko

# 3. Downloads /var/log/app.log from each server

# 4. Parses the downloaded log and counts:
#    - Total lines
#    - ERROR count
#    - WARNING count
#    - INFO count

# 5. If ERROR count is above 10 on any server
#    print a CRITICAL alert for that server

# 6. Generate a summary report as a JSON file called
#    report_YYYY-MM-DD.json with results from all servers

# 7. Handle servers that are unreachable gracefully
#    — mark them as UNREACHABLE in the report
#    — continue processing remaining servers

# 8. All actions must be logged to audit.log


import argparse
import csv
import json
import logging
import os
import sys
from collections import defaultdict
from datetime import datetime
from logging.handlers import RotatingFileHandler

import paramiko

# ── Logging Setup
def setup_logging(log_file: str = "audit.log") -> logging.Logger:
    """
    Sets up logging to both console and rotating audit log file.

    Args:
        log_file: path to audit log file
    Returns:
        logging.Logger: configured logger
    """
    logger = logging.getLogger("devops_log_collector")
    logger.setLevel(logging.DEBUG)

    # ── Format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # ── Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ── Rotating file handler — 5 files, 5MB each
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logging()


# ──────────────────────────────────────────────
# STEP 1 — Read servers from CSV
# ──────────────────────────────────────────────

def read_servers(csv_file: str) -> list:
    """
    Reads server details from a CSV file.

    Args:
        csv_file: path to CSV file with hostname, username, key_path
    Returns:
        list: list of dicts with server details
    Raises:
        FileNotFoundError: if CSV file doesn't exist
        ValueError: if CSV is missing required columns
    """
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: '{csv_file}'")

    required_columns = {"hostname", "username", "key_path"}

    servers = []
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)

        # ── Validate columns
        if not required_columns.issubset(set(reader.fieldnames)):
            missing = required_columns - set(reader.fieldnames)
            raise ValueError(f"CSV missing required columns: {missing}")

        for row in reader:
            servers.append({
                "hostname": row["hostname"].strip(),
                "username": row["username"].strip(),
                "key_path": row["key_path"].strip()
            })

    logger.info(f"Loaded {len(servers)} servers from '{csv_file}'")
    return servers


# ──────────────────────────────────────────────
# STEP 2 — SSH and download log file
# ──────────────────────────────────────────────

def download_log(
    hostname: str,
    username: str,
    key_path: str,
    remote_path: str,
    local_path: str,
    timeout: int = 10
) -> bool:
    """
    SSHs into a server and downloads a log file via SFTP.

    Args:
        hostname: server hostname or IP
        username: SSH username
        key_path: path to private key file
        remote_path: path to log file on remote server
        local_path: local path to save downloaded file
        timeout: SSH connection timeout in seconds
    Returns:
        bool: True if download succeeded, False if server unreachable
    """
    logger.info(f"Connecting to {hostname}...")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # ── Connect via SSH
        ssh.connect(
            hostname=hostname,
            username=username,
            key_filename=key_path,
            timeout=timeout
        )
        logger.info(f"Connected to {hostname}")

        # ── Download file via SFTP
        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()

        logger.info(
            f"Downloaded '{remote_path}' from "
            f"{hostname} → '{local_path}'"
        )
        return True

    except paramiko.AuthenticationException:
        logger.error(f"Authentication failed for {hostname}")
        return False

    except paramiko.SSHException as e:
        logger.error(f"SSH error on {hostname}: {e}")
        return False

    except FileNotFoundError:
        logger.error(f"Remote file not found on {hostname}: {remote_path}")
        return False

    except Exception as e:
        logger.error(f"Failed to connect to {hostname}: {e}")
        return False

    finally:
        ssh.close()
        logger.debug(f"SSH connection closed for {hostname}")


# ──────────────────────────────────────────────
# STEP 3 — Parse log file
# ──────────────────────────────────────────────

def parse_log(filepath: str, error_threshold: int = 10) -> dict:
    """
    Parses a log file and counts log levels.

    Args:
        filepath: path to local log file
        error_threshold: ERROR count above this triggers CRITICAL alert
    Returns:
        dict: counts of INFO, WARNING, ERROR, total lines, and alert
    Raises:
        FileNotFoundError: if log file not found
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Log file not found: '{filepath}'")

    counts = defaultdict(int)
    total_lines = 0

    logger.info(f"Parsing log file: {filepath}")

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            total_lines += 1

            # ── Count log levels
            if "ERROR" in line:
                counts["ERROR"] += 1
            elif "WARNING" in line:
                counts["WARNING"] += 1
            elif "INFO" in line:
                counts["INFO"] += 1
            else:
                counts["OTHER"] += 1

    # ── Check alert threshold
    error_count = counts["ERROR"]
    if error_count > error_threshold:
        alert = f"CRITICAL — ERROR count {error_count} above threshold {error_threshold}"
        logger.warning(f"CRITICAL ALERT: {alert}")
    else:
        alert = "None"

    result = {
        "total_lines": total_lines,
        "INFO": counts["INFO"],
        "WARNING": counts["WARNING"],
        "ERROR": counts["ERROR"],
        "OTHER": counts["OTHER"],
        "alert": alert
    }

    logger.info(
        f"Parse complete — Total: {total_lines} | "
        f"INFO: {counts['INFO']} | "
        f"WARNING: {counts['WARNING']} | "
        f"ERROR: {counts['ERROR']}"
    )

    return result


# ──────────────────────────────────────────────
# STEP 4 — Generate JSON report
# ──────────────────────────────────────────────

def generate_report(results: list, output_dir: str = ".") -> str:
    """
    Generates a JSON summary report for all servers.

    Args:
        results: list of server result dicts
        output_dir: directory to save report
    Returns:
        str: path to generated report file
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    report_filename = f"report_{date_str}.json"
    report_path = os.path.join(output_dir, report_filename)

    report = {
        "date": date_str,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_servers": len(results),
        "reachable": sum(1 for r in results if r["status"] == "OK"),
        "unreachable": sum(
            1 for r in results if r["status"] == "UNREACHABLE"
        ),
        "critical_alerts": sum(
            1 for r in results if "CRITICAL" in r.get("alert", "")
        ),
        "servers": results
    }

    os.makedirs(output_dir, exist_ok=True)

    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Report generated: '{report_path}'")
    return report_path


# ──────────────────────────────────────────────
# STEP 5 — Process all servers
# ──────────────────────────────────────────────

def process_servers(
    servers: list,
    remote_log_path: str,
    temp_dir: str,
    error_threshold: int
) -> list:
    """
    Processes all servers — SSH, download, parse log.

    Args:
        servers: list of server dicts
        remote_log_path: path to log file on remote servers
        temp_dir: local directory to store downloaded logs
        error_threshold: ERROR count threshold for CRITICAL alert
    Returns:
        list: results for all servers
    """
    os.makedirs(temp_dir, exist_ok=True)
    results = []

    for i, server in enumerate(servers, 1):
        hostname = server["hostname"]
        logger.info(
            f"Processing server {i}/{len(servers)}: {hostname}"
        )

        # ── Local path for downloaded log
        local_log = os.path.join(temp_dir, f"{hostname}_app.log")

        # ── Try to download log
        success = download_log(
            hostname=hostname,
            username=server["username"],
            key_path=server["key_path"],
            remote_path=remote_log_path,
            local_path=local_log
        )

        # ── Server unreachable
        if not success:
            logger.warning(f"Marking {hostname} as UNREACHABLE")
            results.append({
                "hostname": hostname,
                "status": "UNREACHABLE",
                "total_lines": 0,
                "INFO": 0,
                "WARNING": 0,
                "ERROR": 0,
                "OTHER": 0,
                "alert": "Server unreachable"
            })
            continue

        # ── Parse downloaded log
        try:
            parse_result = parse_log(local_log, error_threshold)
            results.append({
                "hostname": hostname,
                "status": "OK",
                **parse_result
            })

        except Exception as e:
            logger.error(f"Failed to parse log for {hostname}: {e}")
            results.append({
                "hostname": hostname,
                "status": "PARSE_ERROR",
                "total_lines": 0,
                "INFO": 0,
                "WARNING": 0,
                "ERROR": 0,
                "OTHER": 0,
                "alert": f"Parse error: {e}"
            })

        finally:
            # ── Clean up temp file
            if os.path.exists(local_log):
                os.remove(local_log)
                logger.debug(f"Cleaned up temp file: {local_log}")

    return results


# ──────────────────────────────────────────────
# ARGS & MAIN
# ──────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Collect and analyze logs from multiple servers"
    )
    parser.add_argument(
        "--csv",
        default="servers.csv",
        help="Path to servers CSV file (default: servers.csv)"
    )
    parser.add_argument(
        "--remote-log",
        default="/var/log/app.log",
        help="Remote log file path (default: /var/log/app.log)"
    )
    parser.add_argument(
        "--temp-dir",
        default="/tmp/log_collector",
        help="Temp directory for downloaded logs"
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save JSON report (default: current dir)"
    )
    parser.add_argument(
        "--error-threshold",
        type=int,
        default=10,
        help="ERROR count threshold for CRITICAL alert (default: 10)"
    )
    parser.add_argument(
        "--audit-log",
        default="audit.log",
        help="Path to audit log file (default: audit.log)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logger.info("=" * 60)
    logger.info("Log Collector Started")
    logger.info(f"CSV: {args.csv}")
    logger.info(f"Remote log: {args.remote_log}")
    logger.info(f"Error threshold: {args.error_threshold}")
    logger.info("=" * 60)

    try:
        # ── Read servers
        servers = read_servers(args.csv)

        # ── Process all servers
        results = process_servers(
            servers=servers,
            remote_log_path=args.remote_log,
            temp_dir=args.temp_dir,
            error_threshold=args.error_threshold
        )

        # ── Generate report
        report_path = generate_report(results, args.output_dir)

        # ── Print summary
        reachable = sum(1 for r in results if r["status"] == "OK")
        unreachable = sum(
            1 for r in results if r["status"] == "UNREACHABLE"
        )
        critical = sum(
            1 for r in results if "CRITICAL" in r.get("alert", "")
        )

        print("\n" + "=" * 60)
        print(" LOG COLLECTION SUMMARY")
        print("=" * 60)
        print(f" Total servers   : {len(results)}")
        print(f" Reachable        : {reachable}")
        print(f" Unreachable      : {unreachable}")
        print(f" Critical alerts  : {critical}")
        print(f" Report saved to  : {report_path}")
        print("=" * 60)

        # ── Print critical alerts
        if critical > 0:
            print("\n CRITICAL ALERTS:")
            for r in results:
                if "CRITICAL" in r.get("alert", ""):
                    print(f"   ⚠️  {r['hostname']}: {r['alert']}")
            print()

        # ── Exit with error code if any critical alerts
        if critical > 0:
            sys.exit(2)

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)

    except ValueError as e:
        logger.error(f"Value error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

    finally:
        logger.info("Log Collector Finished")


if __name__ == "__main__":
    main()