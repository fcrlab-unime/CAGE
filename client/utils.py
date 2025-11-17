import base64
import json
import csv
import os
import time
import random
import string

def load_image_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def json_size(payload: dict):
    return len(json.dumps(payload).encode("utf-8"))

def random_prefix():
    return ''.join(random.choices(string.ascii_lowercase, k=5))

def write_csv_row(csv_file, data):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
