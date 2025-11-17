import csv
import os
import time
from fastapi import Request

def save_to_csv(data: dict, raw_body: bytes, csv_file: str):
    timestamp_received = int(time.time() * 1000)
    payload_size = len(raw_body)

    # Merge metadata + payload
    combined = {
        "timestamp_received": timestamp_received,
        "payload_size": payload_size,
        **data
    }

    # Remove raw base64 images to avoid CSV explosion
    if "data" in combined:
        for entity in combined["data"]:
            if "img" in entity:
                entity["img"] = {
                    "type": "Property",
                    "value": "img_base64_code"
                }

    file_exists = os.path.isfile(csv_file)

    # Write row to CSV
    with open(csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=combined.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(combined)
