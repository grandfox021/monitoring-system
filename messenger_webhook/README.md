# 🔗 Django Webhook for Alertmanager → Bale Messenger

## 📖 Overview
This Django application acts as a **webhook receiver** for **Prometheus Alertmanager** and forwards alerts to **Bale Messenger**.  
It provides:  
- `/post-alert/` endpoint to receive alerts from Alertmanager.  
- Automatic formatting of alerts (name, severity, instance, description).  
- Forwarding of alerts to a **Bale bot** in a readable format.  
- Handles multiple alerts per payload.  

---

## ⚙️ Features
- Receives alerts via POST from Alertmanager.  
- Formats messages with **severity-specific emojis** and labels.  
- Sends messages to **Bale Messenger** using the bot API.  
- Safe handling of errors and invalid payloads.  
- Easily extensible for other messaging platforms.  

---

## 📂 Project Structure
