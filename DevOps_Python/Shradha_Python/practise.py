#Write a script to read a file called server.log and count the total number of lines

import argparse
import logging
import os
import sys


logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("line_counter.log")
    ]
)

logger= logging.getLogger(__name__)


def count_lines(filepath :str)-> int:

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if not os.access(filepath, os.R_OK):
        raise PermissionError(f" No permission for: {filepath}")
    
    logger.info(f"Reading file: {filepath}")

    count = 0
    with open(filepath, "r") as f:
        for _ in f:
            count += 1

    logger.info(f"Total lines counted..{count}")
    return count

def parse_args():
    parser = argparse.ArgumentParser(
        description= "count total no of files"
    )

    parser.add_argument(
        "--file",
        default="server.log",
        help="Path to the log file(default: server.log)"
    )

    return parser.parse_args();


def main():
    args=parse_args()

    try:
        total = count_lines(args.file)
        print(f"\n Total lines in '{args.file}': {total}\n")

    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
        sys.exit(1)


