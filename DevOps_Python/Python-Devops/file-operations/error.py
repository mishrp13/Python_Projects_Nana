#

with open("server.log", "r") as infile:
    with open("errors.log", "a") as outfile:
        for line in infile:
            if "ERROR" in line:
                outfile.write(line)


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
        logging.FileHandler("script.log")
    ]
)
logger = logging.getLogger(__name__)


def extract_errors(source_file: str, output_file: str) -> int:
    """
    Reads source log file and appends ERROR lines to output file.

    Args:
        source_file: path to the source log file to read
        output_file: path to the output file to append errors to
    Returns:
        int: total number of ERROR lines found
    Raises:
        FileNotFoundError: if source file doesn't exist
        PermissionError: if files cannot be read or written
    """
    # ── Validate source file exists
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"Source file not found: {source_file}")

    # ── Validate source file is readable
    if not os.access(source_file, os.R_OK):
        raise PermissionError(f"No read permission for: {source_file}")

    # ── Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        logger.info(f"Creating directory: {output_dir}")
        os.makedirs(output_dir)

    logger.info(f"Reading source file: {source_file}")

    error_count = 0

    # ── Read source, append ERROR lines to output
    with open(source_file, "r") as infile, open(output_file, "a") as outfile:
        for line in infile:
            if "ERROR" in line:
                outfile.write(line)
                error_count += 1
                logger.debug(f"ERROR line found: {line.strip()}")

    logger.info(f"Total ERROR lines found: {error_count}")
    logger.info(f"Errors appended to: {output_file}")

    return error_count


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract ERROR lines from log file and append to errors.log"
    )
    parser.add_argument(
        "--source",
        default="server.log",
        help="Source log file to read (default: server.log)"
    )
    parser.add_argument(
        "--output",
        default="errors.log",
        help="Output file to append errors to (default: errors.log)"
    )
    parser.add_argument(
        "--case-insensitive",
        action="store_true",
        help="Match ERROR regardless of case (error, Error, ERROR)"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        # ── Handle case insensitive flag
        if args.case_insensitive:
            logger.info("Running in case-insensitive mode")

        total = extract_errors(args.source, args.output)

        if total == 0:
            print(f"\n No ERROR lines found in '{args.source}'\n")
        else:
            print(f"\n {total} ERROR lines appended to '{args.output}'\n")

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