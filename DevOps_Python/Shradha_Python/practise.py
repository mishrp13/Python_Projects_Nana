import argparse
import logging
import os
import sys


logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("script.log")
    ]
)



logger = logging.getLogger(__name__)

def extract_errors(source_file: str, output_file: str) -> int:

    if not os.path.exists(source_file):
        raise FileNotFoundError(f"source file not found: {source_file}")

    if not os.access(source_file, os.R_OK):
        raise PermissionError(f"No read permission: {source_file}")
    
    output_dir= os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        logger.info(f"creating a directory: {output_dir}")
        os.makedirs(output_dir)


    logger.info(f"Reading  source file: {source_file}")

    err_count =0

    with open(source_file, "r") as infile, open (output_file, "a") as outfile:
        for line in infile:
            if "ERROR" in line:
                outfile.write(line)
                err_count += 1
                logger.debug(f"ERROR line found: {line.strip()}")

    logger.info(f"Total ERROR lines found: {err_count}")
    logger.info(f"Error appended to: {output_file}")
    
    
    return err_count 

def parse_args():

    parser= argparse.ArgumentParser(
        description=" Extract Error lines from log file and append to errors.log "
    )

    parser.add_argument(
        "--source",
        default="errors.log",
        help = "source log file to read ( default: server.log)"
    )

    parser.add_argument(
        "--output",
        default="server.log",
        help="Output file to append errors to (default: error.log)"
    )

    parser.add_argument(
        "--case-insensitive",
        action="store_true",
        help = "Match ERROR regardless of case(error,ERROR, Error)"
    )

    return parser.parse_args()


def main():

    args= parse_args()

    try:

        if args.case_insensitive:
            logger.info("Running incase-sensitive mode")

        total = extract_errors(args.source, args.output)

        if total==0:
            print(f"\n NO ERROR lines found in '{args.source}'\n")
        else:
            print(f"\n {total} ERROR lines appended to '{args.output}'\n")

    except FileNotFoundError as e:
        logger.error(f"File Error : {e}")
        sys.exit(1)

    except PermissionError as e:
        logger.error(f"Permission error: {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"unexpected error  {e}")
        sys.exit(1)

if __name__=="__main__":
    main()



    
     

    








