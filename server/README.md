# KPI Server (FastAPI)

The KPI Server is a lightweight FastAPI-based service designed to receive telemetry and image notifications from distributed IoT/Edge clients.  
Its purpose is to support **latency**, **throughput**, and **payload size** measurements during Cloud–Edge performance evaluations.

All incoming data is logged to a CSV file, including:
- reception timestamp
- payload size in bytes
- sanitized payload (images removed)
- all fields included in the client request

The server is designed to be **simple, fast, and fully configurable** through environment variables.

---

## 🚀 Features

### ✔ FastAPI backend  
High-performance asynchronous server for receiving a high volume of requests.

### ✔ JSON ingestion endpoint  
Receives NGSI-LD-like payloads or generic JSON structures.

### ✔ CSV Logging  
Stores:
- timestamp of reception (ms)
- payload size
- payload content (with images sanitized)

### ✔ Environment-based Configuration  
File paths, server host/port, and debug mode configured via `.env`.

### ✔ Health Check Endpoint  
Lightweight `/server-kpi/ping` route for client connectivity testing.

---

## 🗂 Project Structure

```
server/
│── app.py            # FastAPI application
│── utils.py          # CSV handling & sanitization
│── .env              # Configuration file
│── requirements.txt  # Python dependencies
│── README.md         # Documentation
```

---

## ⚙ Requirements

- Python 3.8+  
- FastAPI  
- uvicorn  
- python-dotenv  

---

## 🔧 Installation

### 1️⃣ Clone the repository

```bash
git clone <your_repository_url>
cd server
```

### 2️⃣ (Optional) Create a virtual environment
```bash
python3 -m venv env
source env/bin/activate       # Linux/macOS
env\Scripts\activate          # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

---

## 📝 Configuration (`.env`)

The `.env` file allows full customization of the server behavior.

### Example:

```
CSV_FILE=notifications.csv
SERVER_HOST=0.0.0.0
SERVER_PORT=9999
DEBUG=true
```

### Available variables:

| Variable       | Description                                   | Default             |
|----------------|-----------------------------------------------|---------------------|
| `CSV_FILE`     | Output CSV file path                          | notifications.csv   |
| `SERVER_HOST`  | Host to bind the server                       | 0.0.0.0             |
| `SERVER_PORT`  | Port to listen on                             | 9999                |
| `DEBUG`        | Enable FastAPI debug mode                     | false               |

---

## ▶️ Running the Server

### Standard launch:
```bash
uvicorn app:app --host 0.0.0.0 --port 9999
```

### Using values from `.env` (recommended):

```bash
uvicorn app:app --host $SERVER_HOST --port $SERVER_PORT --reload
```

---

## 📡 API Endpoints

### **GET /server-kpi/ping**
Health-check endpoint used by clients to validate connectivity.

**Response Example**
```json
{
  "status": "ok"
}
```

---

### **POST /server-kpi/notify**
Receives JSON payloads and logs them to CSV.

**Expected Input**
Any JSON object.  
Image fields under `data[*].img` are sanitized to:

```json
"img": { "type": "Property", "value": "img_base64_code" }
```

**Successful Response**
```json
{
  "status": "success",
  "message": "Notification received and saved!"
}
```

**Error Response**
```json
{
  "status": "error",
  "message": "Exception message..."
}
```

---

## 📊 CSV Logging Format

Each line in the CSV contains:

| Field               | Description                              |
|---------------------|-------------------------------------------|
| timestamp_received  | Reception UNIX time in milliseconds       |
| payload_size        | Raw JSON payload size in bytes            |
| ...other fields     | All additional JSON fields received       |

---

## 🧩 How It Works

1. Client sends a JSON payload via POST  
2. Server:
   - captures reception timestamp  
   - measures payload size  
   - sanitizes image fields  
   - merges metadata + payload  
3. Data is appended to a CSV file  
4. CSV can be analyzed later for latency and throughput metrics

---

