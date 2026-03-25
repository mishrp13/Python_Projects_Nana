
#-------------------------------------
from datetime import datetime

with open("output.txt", "a") as f:
    f.write(f"{datetime.now()} - Hello this is a custom message\n")

#-----------------------------------------------

import argparse
import logging
import os
import sys
from datetime import datetime

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("script.log")
    ]
)
logger = logging.getLogger(__name__)


def write_message(filepath: str, message: str) -> None:
    """
    Appends current timestamp + custom message to a file.
    Creates the file if it doesn't exist.

    Args:
        filepath: path to the output file
        message:  custom message to write
    Raises:
        PermissionError: if file cannot be written
        OSError: if directory doesn't exist
    """
    # ── Create directory if it doesn't exist
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        logger.info(f"Creating directory: {directory}")
        os.makedirs(directory)

    # ── Build the log entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}\n"

    logger.info(f"Writing to file: {filepath}")

    # ── Append to file (creates if not exists)
    with open(filepath, "a") as f:
        f.write(entry)

    logger.info(f"Successfully written: {entry.strip()}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Write timestamp + custom message to a file"
    )
    parser.add_argument(
        "--file",
        default="output.txt",
        help="Path to output file (default: output.txt)"
    )
    parser.add_argument(
        "--message",
        default="Automated log entry",
        help="Custom message to write (default: 'Automated log entry')"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        write_message(args.file, args.message)
        print(f"\n Entry written to '{args.file}' successfully\n")

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        sys.exit(1)

    except OSError as e:
        logger.error(f"OS error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

