# KPI Client Tester

A Python client designed to automatically send JSON payloads (sensor data and images) to NGSI-LD endpoints for **latency** and **throughput** testing across different network conditions such as 4G/5G, Starlink, or other ISP connections.

This tool is used to simulate real IoT/Edge workloads by sending controlled bursts of traffic and logging key performance metrics into CSV files for further analysis.

---

## 🚀 Features

### ✔ Weather Payload Testing  
Sends structured JSON packets representing temperature, humidity, pressure, and wind telemetry.

### ✔ Image Payload Testing  
Sends 10-frame Base64-encoded image payloads to evaluate bandwidth usage, network buffering, and throughput.

### ✔ Latency Tests  
Sends batches at controlled frequencies (packets/second) to measure network + processing latency.

### ✔ Throughput Tests  
Sends large bursts of packets without delay to test maximum send rate.

### ✔ CSV Logging  
Automatically generates standardized CSV files for weather and image tests with:
- request ID  
- timestamp  
- batch size  
- frequency  
- JSON size  

### ✔ Complete `.env` Configuration  
No hardcoded values. All endpoints, test sizes, file paths, and connection type are configurable.

### ✔ Modular Codebase  
The client follows a clean structure with separated modules for configuration, utilities, payload building, and testing logic.

---

## 🗂 Project Structure

```
client/
│── client.py           # Main execution script
│── config.py           # Loads environment variables
│── utils.py            # Helper functions (CSV, Base64, etc.)
│── .env                # Configuration file
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
```

---

## ⚙ Requirements

- Python 3.8 or later  
- pip  
- Internet connectivity to send traffic

---

## 🔧 Installation

### 1️⃣ Clone the repository
```bash
git clone <repository_url>
cd client
```

### 2️⃣ (Optional) Create a virtual environment
```bash
python3 -m venv env
source env/bin/activate   # Linux/macOS
env\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📝 Configuration (`.env`)

The `.env` file controls all operational parameters.

### Example:

```
# ============================================
# Server Under Test (KPI Server)
# ============================================
SERVER_URL=https://your-server-url.com
PING_ENDPOINT=/your-ping-endpoint

# ============================================
# NGSI-LD / API Endpoints
# Replace with your target endpoints
# ============================================
ORION_WEATHER_URL=https://your-api-domain.com/ngsi-ld/v1/entities/your-weather-entity/attrs
ORION_IMG_URL=https://your-api-domain.com/ngsi-ld/v1/entities/your-image-entity/attrs

# ============================================
# Network Type Used for the Test
# Examples: 4G_5G, Starlink, Fiber, WiFi, Satellite
# ============================================
CONNECTION_TYPE=YourNetworkType

# ============================================
# Test Parameters
# Comma-separated numeric lists
# ============================================
BATCH_SIZES=10,20,60
FREQUENCIES=60,30,20
THROUGHPUT_BATCH_SIZES=10,50,100

# ============================================
# Image Payload
# Path to the file that will be converted to Base64
# ============================================
IMG_FILE=your_image.jpg

```

---

## ▶️ Running the Client

To start the test, simply run:

```bash
python3 client.py
```

The workflow includes:

1. Server ping check  
2. Weather latency tests  
3. Weather throughput tests  
4. Image latency tests  
5. Image throughput tests  

---

## 📊 Output

The client generates two CSV files:

### Weather tests:
```
<CONNECTION_TYPE>_<random_prefix>_weather.csv
```

### Image tests:
```
<CONNECTION_TYPE>_<random_prefix>_img.csv
```

### Each CSV row includes:
- `id_request`  
- `timestamp_send`  
- `batch_size`  
- `frequency`  
- `json_size`  

These files are suitable for:
- latency analysis  
- throughput graphs  
- KPI reporting (e.g., OA4.1 in Cloud-Edge architectures)

---

## 🔍 How It Works

### 1. Payload Generation  
Each payload contains:
- unique incremental request ID  
- timestamp in milliseconds  
- telemetry or Base64 image data  

### 2. Latency Tests  
Packets are distributed evenly using:
```
interval = frequency / batch_size
```

### 3. Throughput Tests  
Packets are sent without waiting.

### 4. CSV Logging  
All metadata needed for KPI analysis is appended in real time.

---
