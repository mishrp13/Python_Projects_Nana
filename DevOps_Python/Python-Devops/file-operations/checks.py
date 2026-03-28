#
import os

filepath = "server.log"

if os.path.exists(filepath):
    with open(filepath, "r") as f:
        print(f.read())
else:
    print(f"File not found: {filepath}")

#

import argparse
import logging
import os
import sys

# ── Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("file_checker.log")
    ]
)
logger = logging.getLogger(__name__)


def check_and_read_file(filepath: str) -> str:
    """
    Checks if a file exists and reads its content.

    Args:
        filepath: path to the file to check and read
    Returns:
        str: file content if file exists
    Raises:
        FileNotFoundError: if file does not exist
        PermissionError: if file cannot be read
        IsADirectoryError: if path is a directory not a file
    """
    # ── Check if path exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"File does not exist: '{filepath}'"
        )

    # ── Check if it is a file not a directory
    if not os.path.isfile(filepath):
        raise IsADirectoryError(
            f"Path exists but is a directory, not a file: '{filepath}'"
        )

    # ── Check read permission
    if not os.access(filepath, os.R_OK):
        raise PermissionError(
            f"No read permission for file: '{filepath}'"
        )

    # ── Get file size before reading
    file_size = os.path.getsize(filepath)
    logger.info(f"File found: '{filepath}' ({file_size} bytes)")

    # ── Check if file is empty
    if file_size == 0:
        logger.warning(f"File exists but is empty: '{filepath}'")
        return ""

    # ── Read and return content
    logger.info(f"Reading file: '{filepath}'")
    with open(filepath, "r") as f:
        content = f.read()

    logger.info(f"Successfully read {len(content.splitlines())} lines")
    return content


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check if a file exists and read its content"
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the file to check and read"
    )
    parser.add_argument(
        "--show-content",
        action="store_true",
        help="Print file content to console (default: False)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        content = check_and_read_file(args.file)

        if content == "":
            print(f"\n File '{args.file}' exists but is empty\n")
        else:
            print(f"\n File '{args.file}' exists and is readable")
            print(f" Total lines: {len(content.splitlines())}\n")

            # ── Only print content if flag passed
            if args.show_content:
                print("─" * 50)
                print(content)
                print("─" * 50)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\n ERROR: {e}")
        print(f" Please check the file path and try again\n")
        sys.exit(1)

    except IsADirectoryError as e:
        logger.error(f"Path is a directory: {e}")
        print(f"\n ERROR: {e}")
        print(f" Please provide a file path, not a directory\n")
        sys.exit(1)

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        print(f"\n ERROR: {e}")
        print(f" Try running with sudo or check file permissions\n")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()