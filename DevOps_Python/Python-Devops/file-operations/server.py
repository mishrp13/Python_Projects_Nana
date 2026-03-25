
#----------------------

def count_in_lines(file_path):
    try:
        with open(file_path,'r') as file:
            lines=file.readlines()
            return len(lines)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist")
        return None
    
count=count_in_lines("new.txt")
print(count)


#---------------------------------------------------


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
        logging.FileHandler("line_counter.log")
    ]
)
logger = logging.getLogger(__name__)



def count_lines(filepath: str) -> int:
    """
    Reads a file and returns total number of lines.
    
    Args:
        filepath: path to the file
    Returns:
        int: total line count
    Raises:
        FileNotFoundError: if file doesn't exist
        PermissionError: if file can't be read
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"No read permission for: {filepath}")

    logger.info(f"Reading file: {filepath}")

    count = 0
    with open(filepath, "r") as f:
        for _ in f:
            count += 1

    logger.info(f"Total lines counted: {count}")
    return count


def parse_args():
    parser = argparse.ArgumentParser(
        description="Count total number of lines in a file"
    )
    parser.add_argument(
        "--file",
        default="server.log",
        help="Path to the log file (default: server.log)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        total = count_lines(args.file)
        print(f"\n Total lines in '{args.file}': {total}\n")

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)

    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


