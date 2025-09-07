# 🔎 Monitoring Project with FastAPI, MongoDB, Prometheus, Grafana & Alerting

## 📖 Overview
This project is a **monitoring-enabled web application stack** running on **three isolated VMs** (via VMware).  
It demonstrates how to:  
- Run a **FastAPI-based or Django-based web application** (containerized with Docker Compose).  
- Store user credentials securely in **MongoDB** (with password hashing).  
- Collect system and application metrics using **Prometheus exporters**.  
- Visualize monitoring data in **Grafana dashboards**.  
- Send **real-time alerts** to messaging apps (e.g., **Bale**) using **Alertmanager + webhooks**.  

---

## 🏗️ Architecture
The system is divided into **three servers (VMs)**:

### 1️⃣ Web Application Server
- **FastAPI or Django application** (Dockerized, managed with Docker Compose).  
- Uses **Prometheus Client Library** for custom metrics.  
- Exposes **webhook endpoint** to receive alerts from Alertmanager.  
- Sends alerts to **Bale messenger** via bot API.  
- **cAdvisor** → Collects container-level metrics.  
- **node_exporter** → Collects OS-level metrics.  

### 2️⃣ MongoDB Server
- **MongoDB** (installed bare-metal).  
- **mongodb_exporter** → Provides database metrics.  
- **node_exporter** → Collects OS-level metrics.  

### 3️⃣ Monitoring Server (Prometheus + Grafana + Alertmanager)
- **Prometheus** → Scrapes metrics from all exporters.  
- **Grafana** → Visualization layer with dashboards for:  
  - MongoDB  
  - cAdvisor (container metrics)  
  - Custom-built dashboards for the application  
- **Alertmanager** → Receives alerts from Prometheus and forwards them to the webhook.  
- **blackbox_exporter** → Probes endpoints for uptime monitoring.  
- **node_exporter** → Collects OS-level metrics.  

---

## 📂 Data Flow
1. User uploads a **file containing `username:password` pairs**.  
2. The **FastAPI/Django application**:  
   - Reads the file.  
   - Converts it into **JSON format**.  
   - Hashes all passwords securely.  
   - Stores the result in **MongoDB**.  
3. Metrics from the **web app, MongoDB, system resources, and containers** are scraped by **Prometheus**.  
4. **Grafana dashboards** visualize the data for real-time monitoring.  
5. When a **metric crosses a threshold**, Prometheus fires an alert.  
6. **Alertmanager** receives the alert and sends it to the **webhook endpoint**.  
7. The web app processes the alert and sends a **formatted notification to Bale messenger**.  

---

## 📊 Alerting Flow
- Alerts are **grouped and throttled** in Alertmanager:
  - `group_wait`: wait time before sending first message for grouped alerts.  
  - `group_interval`: interval between messages for the same group.  
  - `repeat_interval`: how often a still-active alert repeats.  
- The webhook formats alerts for readability (name, severity, instance, description).  
- Example formatted alert sent to Bale:
🚨 instanceDown (Severity: critical)
Instance: VM1
Target VM1 on localhost is down for more than 1 minute.
🚨 CPUHigh (Severity: warning)
Instance: VM2
CPU usage is above 90%.


---

## ⚙️ Tech Stack

| Component         | Technology Used |
|-------------------|-----------------|
| **Frontend**      | Grafana Dashboards |
| **Backend**       | FastAPI / Django |
| **Database**      | MongoDB |
| **Containerization** | Docker Compose (for web app) |
| **Monitoring**    | Prometheus, Grafana, node_exporter, cAdvisor, mongodb_exporter, blackbox_exporter, Alertmanager |
| **Alerting / Messaging** | Bale Messenger via webhook |
| **Infrastructure** | VMware (3 VMs) |

---

## 📊 Example Grafana Dashboards
- **MongoDB Dashboard** → Connections, operations, memory, oplog size.  
- **cAdvisor Dashboard** → Container CPU, memory, network, storage.  
- **Web App Metrics** → Custom Prometheus metrics from FastAPI/Django.  
- **System Metrics** → Exported by node_exporter (CPU, memory, disk, network).  
- **Blackbox Dashboard** → Endpoint availability & latency.  

---

## 🚀 Deployment

### 1️⃣ Web Application Server (Dockerized FastAPI/Django + cAdvisor + node_exporter)
```bash
# Start FastAPI/Django app (inside project folder)
docker compose up -d
