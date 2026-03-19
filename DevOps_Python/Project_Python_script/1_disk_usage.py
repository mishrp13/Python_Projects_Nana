
# Write a script to check disk usage and alert if usage exceeds a threshold.

import shutil

THRESHOLD = 80  # percentage
PARTITION = "/"

total, used, free = shutil.disk_usage(PARTITION)
usage_percent = (used / total) * 100

if usage_percent >= THRESHOLD:
    print(f"ALERT: Disk usage on {PARTITION} is {usage_percent:.2f}%")
else:
    print(f"Disk usage on {PARTITION} is normal: {usage_percent:.2f}%")

