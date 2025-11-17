import time
import requests
import json
from config import CONFIG
from utils import (
    random_prefix,
    json_size,
    load_image_base64,
    write_csv_row
)

### --- LOAD CONFIG ---
SERVER_URL = CONFIG["SERVER_URL"]
PING_ENDPOINT = CONFIG["PING_ENDPOINT"]
WEATHER_URL = CONFIG["ORION_WEATHER_URL"]
IMG_URL = CONFIG["ORION_IMG_URL"]
CONNECTION_TYPE = CONFIG["CONNECTION_TYPE"]

BATCH_SIZES = CONFIG["BATCH_SIZES"]
FREQUENCIES = CONFIG["FREQUENCIES"]
THROUGHPUT_BATCH_SIZES = CONFIG["THROUGHPUT_BATCH_SIZES"]

IMG_FILE = CONFIG["IMG_FILE"]
IMAGE_BASE64 = load_image_base64(IMG_FILE)

### --- Prefix identifiers ---
prefix_weather = random_prefix()
prefix_img = random_prefix()
weather_id = 1
img_id = 1

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


### --- Server ping ---
def check_server():
    try:
        res = requests.get(SERVER_URL + PING_ENDPOINT)
        return res.status_code == 200
    except:
        return False


### --- Payload builders ---
def build_weather_payload():
    global weather_id
    rid = f"{prefix_weather}{weather_id}"
    weather_id += 1

    return {
        "id_request": {"type": "Property", "value": rid},
        "timestamp_send": {"type": "Property", "value": int(time.time() * 1000)},
        "temperature": {"type": "Property", "value": 22.5},
        "humidity": {"type": "Property", "value": 60},
        "pressure": {"type": "Property", "value": 1013},
        "wind_speed": {"type": "Property", "value": 5.5},
        "wind_direction": {"type": "Property", "value": "N"},
    }


def build_img_payload():
    global img_id
    rid = f"{prefix_img}{img_id}"
    img_id += 1

    return {
        "id_request": {"type": "Property", "value": rid},
        "timestamp_send": {"type": "Property", "value": int(time.time() * 1000)},
        "img": {"type": "Property", "value": [IMAGE_BASE64] * 10},
    }


### --- CSV Filename builders ---
def csv_weather_file():
    return f"{CONNECTION_TYPE}_{prefix_weather}_weather.csv"

def csv_img_file():
    return f"{CONNECTION_TYPE}_{prefix_img}_img.csv"


### ===============================
### MAIN TEST ROUTINE
### ===============================
if __name__ == "__main__":

    if not check_server():
        print("❌ Server unreachable, aborting.")
        exit()

    print(f"✅ Connected. Running tests for network: {CONNECTION_TYPE}")

    csv_w = csv_weather_file()

    # --- Weather latency tests ---
    print("\n🌦 WEATHER LATENCY TESTS")
    for batch in BATCH_SIZES:
        for freq in FREQUENCIES:
            print(f"→ Batch {batch}, Frequency {freq}")
            interval = freq / batch
            for _ in range(batch):
                payload = build_weather_payload()
                size = json_size(payload)

                write_csv_row(csv_w, {
                    "id_request": payload["id_request"]["value"] + "_latency",
                    "timestamp_send": payload["timestamp_send"]["value"],
                    "batch_size": batch,
                    "frequency": freq,
                    "json_size": size
                })

                requests.post(WEATHER_URL, headers=HEADERS, data=json.dumps(payload))
                time.sleep(interval)

    # --- Weather throughput ---
    print("\n🌦 WEATHER THROUGHPUT TESTS")
    for batch in THROUGHPUT_BATCH_SIZES:
        print(f"→ Throughput Batch {batch}")
        for _ in range(batch):
            payload = build_weather_payload()
            size = json_size(payload)

            write_csv_row(csv_w, {
                "id_request": payload["id_request"]["value"] + "_throughput",
                "timestamp_send": payload["timestamp_send"]["value"],
                "batch_size": batch,
                "frequency": "null",
                "json_size": size
            })

            requests.post(WEATHER_URL, headers=HEADERS, data=json.dumps(payload))

    time.sleep(1)

    ### --- IMG TESTS ---
    csv_i = csv_img_file()

    print("\n🖼 IMAGE LATENCY TESTS")
    for batch in BATCH_SIZES:
        for freq in FREQUENCIES:
            print(f"→ Batch {batch}, Frequency {freq}")
            interval = freq / batch
            for _ in range(batch):
                payload = build_img_payload()
                size = json_size(payload)

                write_csv_row(csv_i, {
                    "id_request": payload["id_request"]["value"] + "_latency",
                    "timestamp_send": payload["timestamp_send"]["value"],
                    "batch_size": batch,
                    "frequency": freq,
                    "json_size": size
                })

                requests.post(IMG_URL, headers=HEADERS, data=json.dumps(payload))
                time.sleep(interval)

    print("\n🖼 IMAGE THROUGHPUT TESTS")
    for batch in THROUGHPUT_BATCH_SIZES:
        print(f"→ Throughput Batch {batch}")
        for _ in range(batch):
            payload = build_img_payload()
            size = json_size(payload)

            write_csv_row(csv_i, {
                "id_request": payload["id_request"]["value"] + "_throughput",
                "timestamp_send": payload["timestamp_send"]["value"],
                "batch_size": batch,
                "frequency": "null",
                "json_size": size
            })

            requests.post(IMG_URL, headers=HEADERS, data=json.dumps(payload))

    print("\n✅ TEST COMPLETED")
