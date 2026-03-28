#

with open("file1.txt", "r") as f1, \
     open("file2.txt", "r") as f2, \
     open("merged.txt", "w") as out:
    out.write(f1.read())
    out.write(f2.read())

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
        logging.FileHandler("merge.log")
    ]
)
logger = logging.getLogger(__name__)


def merge_files(file1: str, file2: str, output_file: str) -> int:
    """
    Reads two files and merges their content into a third file.

    Args:
        file1: path to first input file
        file2: path to second input file
        output_file: path to output merged file
    Returns:
        int: total number of lines written
    Raises:
        FileNotFoundError: if either input file doesn't exist
        PermissionError: if files cannot be read or written
    """
    # ── Validate both input files exist
    for filepath in [file1, file2]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"No read permission: {filepath}")

    # ── Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        logger.info(f"Creating directory: {output_dir}")
        os.makedirs(output_dir)

    total_lines = 0

    logger.info(f"Merging '{file1}' and '{file2}' into '{output_file}'")

    with open(output_file, "w") as outfile:

        # ── Write file1
        logger.info(f"Reading file1: {file1}")
        with open(file1, "r") as f1:
            for line in f1:
                outfile.write(line)
                total_lines += 1

        # ── Add separator between files
        outfile.write("\n")

        # ── Write file2
        logger.info(f"Reading file2: {file2}")
        with open(file2, "r") as f2:
            for line in f2:
                outfile.write(line)
                total_lines += 1

    logger.info(f"Total lines written: {total_lines}")
    logger.info(f"Merged file saved: {output_file}")

    return total_lines


def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge two files into a third file"
    )
    parser.add_argument(
        "--file1",
        default="file1.txt",
        help="Path to first input file (default: file1.txt)"
    )
    parser.add_argument(
        "--file2",
        default="file2.txt",
        help="Path to second input file (default: file2.txt)"
    )
    parser.add_argument(
        "--output",
        default="merged.txt",
        help="Path to output merged file (default: merged.txt)"
    )
    parser.add_argument(
        "--separator",
        default="",
        help="Custom separator line between files (default: empty line)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        total = merge_files(args.file1, args.file2, args.output)
        print(f"\n Successfully merged '{args.file1}' and '{args.file2}'")
        print(f" Total lines written to '{args.output}': {total}\n")

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
