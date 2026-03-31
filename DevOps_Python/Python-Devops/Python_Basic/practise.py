import argparse
import logging
import sys
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("boto3_validator.log")
    ]
)

logger = logging.getLogger(__name__)


def safe_int(value: Any, field_name: str) -> int:

    if value is None:
        raise TypeError(f"Field '{field_name}' is none - cannot convert to int")
    
    try:
        return int(value)
    except (ValueError,TypeError) as e:
        raise TypeError(
            f"Field '{field_name}' expected in-compatible int type"
            f"got: '{value} (type: {type(value).__name__}))"

        ) from e
    

def safe_str(value: Any, field_name: str) -> str:
    if value is None:
        raise ValueError(f"Field Value : {field_name} is None")
    
    result= str(value).strip()

    if not result:
        raise ValueError(f"Field value '{field_name}' is empty string")
    
    return result


def safe_bool(value: Any, filed_name: str) -> bool:

    if isinstance(value, bool):
        return True
    
    if isinstance(value, int):
        return value!=0
    
    if isinstance(value, str):
        normalized= value.strip().lower()
        if normalized in ("true", "1", "yes", "enabled"):
            return True
        if normalized in ("false", "0", "no", "disabled"):
            return False
        
    raise ValueError(
        f"field_value : {filed_name} cannot be parsed to bool"
        f"{value} is (type : {type(value).__name__})"
    )