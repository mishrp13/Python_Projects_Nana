import logging
import yaml
import psutil
import argparse

parser= argparse.ArgumentParser(description="System Monitoring script")
parser.add_argument("--config" , default="config.yaml", help="path to config file")
args= parser.parse_args()


try:
    with open(args.config, "r") as file:
        config= yaml.safe_load(file)
except Exception as e:
    print("Error loading file",e)
    exit(1)

cpu_threshold = config["cpu_threshold"]
memory_threshold = config["memory_threshold"]
disk_threshold = config["disk_threshold"]
log_file= config["load_file"]

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


try:
    cpu= psutil.cpu_percent()
    memory=psutil.virtual_memory().percent
    disk= psutil.disk_usage("/").percent

    print(f"CPU: {cpu}%")
    print(f"Memory: {memory}%")
    print(f"Disk: {disk}%")

    if cpu > cpu_threshold:
        logging.warning(f" CPU usage is high: {cpu}%")

    if memory> memory_threshold:
        logging.warning(f"Memory usage is high: {memory}")
    
    if disk > disk_threshold:
        logging.warning(f"disk usage is htigh: {disk} ")


except Exception as e:
    logging.error(f"Script failed: ",e)


