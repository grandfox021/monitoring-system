# 🚨 Alertmanager Setup & Integration with Bale Messenger

## 📖 Overview
This README explains how to configure **Prometheus Alertmanager** for sending alerts to a web application and forwarding notifications to **Bale messenger** using a webhook.  
It covers:  
- Alertmanager installation & basic configuration  
- Webhook integration  
- Sending alerts to Bale  
- Example test alert  

---

## ⚙️ Alertmanager Configuration

### 1️⃣ Global Settings
```yaml
global:
  resolve_timeout: 5m
