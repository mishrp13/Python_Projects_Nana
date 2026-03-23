#Write a script to read a file called server.log and count the total number of lines

import argparse
import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO
    format="%(asctime)s | %(levelname)s | %(message)s)"
    handlers=[
        logging.streamHandler(sys.stdout)
    ]
)
