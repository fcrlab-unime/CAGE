import os
from dotenv import load_dotenv

load_dotenv()

def get_list(key):
    value = os.getenv(key, "")
    return [int(x) for x in value.split(",") if x.strip()]

CONFIG = {
    "SERVER_URL": os.getenv("SERVER_URL"),
    "PING_ENDPOINT": os.getenv("PING_ENDPOINT"),
    "ORION_WEATHER_URL": os.getenv("ORION_WEATHER_URL"),
    "ORION_IMG_URL": os.getenv("ORION_IMG_URL"),
    "CONNECTION_TYPE": os.getenv("CONNECTION_TYPE"),
    "BATCH_SIZES": get_list("BATCH_SIZES"),
    "FREQUENCIES": get_list("FREQUENCIES"),
    "THROUGHPUT_BATCH_SIZES": get_list("THROUGHPUT_BATCH_SIZES"),
    "IMG_FILE": os.getenv("IMG_FILE")
}
