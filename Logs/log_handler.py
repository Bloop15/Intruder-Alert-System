import csv
import os
from datetime import datetime

def log_intrusion(image_filename, alert_status):
    log_file= os.path.join("Logs", "intruder_log.csv")
    log_exists= os.path.exists(log_file)

    with open(log_file, mode= 'a', newline= '') as file:
        writer= csv.writer(file)
        if not log_exists:
            writer.writerow(["Timestamp", "Image Filename", "Alert Status"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            image_filename,
            alert_status
        ])