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
        print(f"source file not found: {source_file}")

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
        
    )


    
     

    








