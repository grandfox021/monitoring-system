# 🔎 Monitoring Project with FastAPI, MongoDB, Prometheus & Grafana

## 📖 Overview
This project is a **monitoring-enabled web application stack** running on **three isolated VMs** (via VMware).  
It demonstrates how to:  
- Run a **FastAPI-based web application** (containerized with Docker Compose).  
- Store user credentials securely in **MongoDB** (with password hashing).  
- Collect system and application metrics using **Prometheus exporters**.  
- Visualize monitoring data in **Grafana dashboards**.  

---

## 🏗️ Architecture
The system is divided into **three servers (VMs)**:

### 1️⃣ Web Application Server
- **FastAPI application** (Dockerized, managed with Docker Compose).  
- Uses **Prometheus Client Library** for custom metrics.  
- **cAdvisor** → Collects container-level metrics.  
- **node_exporter** → Collects OS-level metrics.  

### 2️⃣ MongoDB Server
- **MongoDB** (installed bare-metal).  
- **mongodb_exporter** → Provides database metrics.  
- **node_exporter** → Collects OS-level metrics.  

### 3️⃣ Monitoring Server (Prometheus + Grafana)
- **Prometheus** → Scrapes metrics from all exporters.  
- **Grafana** → Visualization layer with dashboards for:  
  - MongoDB  
  - cAdvisor (container metrics)  
  - Custom-built dashboards for the application  
- **blackbox_exporter** → Probes endpoints for uptime monitoring.  
- **node_exporter** → Collects OS-level metrics.  

---

## 📂 Data Flow
1. User uploads a **file containing `username:password` pairs**.  
2. The **FastAPI application**:  
   - Reads the file.  
   - Converts it into **JSON format**.  
   - Hashes all passwords securely.  
   - Stores the result in **MongoDB**.  
3. Metrics from the **web app, MongoDB, system resources, and containers** are scraped by **Prometheus**.  
4. **Grafana dashboards** visualize the data for real-time monitoring.  

---

## ⚙️ Tech Stack

| Component         | Technology Used |
|-------------------|-----------------|
| **Frontend**      | Grafana Dashboards |
| **Backend**       | FastAPI |
| **Database**      | MongoDB |
| **Containerization** | Docker Compose (for web app) |
| **Monitoring**    | Prometheus, Grafana, node_exporter, cAdvisor, mongodb_exporter, blackbox_exporter |
| **Infrastructure** | VMware (3 VMs) |

---

## 📊 Example Grafana Dashboards
- **MongoDB Dashboard** → Connections, operations, memory, oplog size.  
- **cAdvisor Dashboard** → Container CPU, memory, network, storage.  
- **Web App Metrics** → Custom Prometheus metrics from FastAPI.  
- **System Metrics** → Exported by node_exporter (CPU, memory, disk, network).  
- **Blackbox Dashboard** → Endpoint availability & latency.  

---

## 🚀 Deployment

### 1️⃣ Web Application Server (Dockerized FastAPI + cAdvisor + node_exporter)
```bash
# Start FastAPI app (inside project folder)
docker compose up -d
