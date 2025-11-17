# CAGE — Cloud Architecture Gap Evaluation

CAGE is a complete testing framework designed to evaluate **latency**, **throughput**, and **payload processing performance** in distributed **Cloud–Edge** architectures.

The goal of CAGE is to identify architectural gaps, performance bottlenecks, and network limitations across different connectivity environments such as 4G/5G, Starlink, WiFi, fiber, or satellite links.

This repository includes two main components:

- **Client Module** → generates telemetry and image payloads and sends them at controlled rates  
- **Server Module** → receives payloads, logs ingestion metrics, and supports end-to-end KPI analysis  

Together, they form a reproducible measurement suite useful for research, benchmarking, and Cloud–Edge system evaluation.

---

## 📦 Repository Structure

```
CAGE/
│── client/         # Payload generator and KPI test executor
│── server/         # FastAPI ingestion service and CSV logger
│── README.md       # (this file)
```

---

## 🎯 Project Purpose

CAGE helps evaluate:

- Cloud–Edge architectural gaps  
- real network performance under different conditions  
- effects of payload size on network behavior  
- ingestion speed and throughput of backend services  
- end-to-end telemetry delays  
- suitability of Cloud, Edge, or Hybrid processing  

You can use CAGE for:

- research experiments  
- infrastructure benchmarking  
- performance comparisons between ISPs  
- KPI validation (e.g., OA4.1, cloud/edge split)  
- system capacity planning   

---

## 🚀 System Overview

### ✔ **Client Module**  
Simulates IoT/Edge devices by sending:

- weather telemetry JSON payloads  
- image payloads encoded in Base64  
- configurable batch sizes  
- latency patterns (batch + frequency)  
- throughput stress bursts  

All sent metadata is logged into CSV files.

📄 Documentation:  
➡️ **client/README.md**

---

### ✔ **Server Module**  
A FastAPI service that:

- receives all client payloads  
- timestamps arrival time  
- measures payload size  
- sanitizes image fields  
- appends full records to CSV for later analysis  
- exposes a `/ping` health endpoint  

📄 Documentation:  
➡️ **server/README.md**

---

## 🛠 Technologies Used

- Python 3.8+  
- FastAPI  
- Uvicorn  
- Requests  
- python-dotenv  
- CSV logging for reproducibility  

---

## 🔧 Setup and Usage

### 1. Configure environment variables  
Each module has its own `.env.example`.  
Copy and rename to `.env`:

```
cp client/.env.example client/.env
cp server/.env.example server/.env
```

### 2. Install dependencies  
```bash
pip install -r client/requirements.txt
pip install -r server/requirements.txt
```

### 3. Start the KPI ingestion server  
```bash
cd server
uvicorn app:app --reload
```

### 4. Run the KPI client  
```bash
cd client
python3 client.py
```

---

## 📊 Output & Analysis

CAGE produces:

### **Client-side logs**
- timestamps of sending  
- JSON payload sizes  
- test parameters (batch, frequency, throughput type)  

### **Server-side logs**
- timestamps of reception  
- payload size  
- sanitized payload fields  

Use these logs for:
- latency curves  
- throughput charts  
- jitter estimation  
- network performance comparison  
- Cloud–Edge gap analysis  

---
