import logging
import sys

def setup_script_logger(logger_name):

    if not isinstance(logger_name,str):
        raise TypeError("logger_name must be a string")
    
    if not logger_name:
        raise ValueError("logger_name cannot be an empty string")
    

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    handler= logging.StreamHandler(sys.stdout)
    formatter= logging.Formatter("%(actime)s -%(levelname)s -%(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger


