# 🔐 Password Hasher DB (FastAPI + MongoDB + Prometheus)

## 📖 Overview
This project is a **FastAPI web application** that allows users to upload files containing `username:password` pairs.  
The app will:  
- Parse the file and extract users.  
- Hash all passwords using **SHA-512**.  
- Store results in **MongoDB** with unique file hashes.  
- Provide REST API endpoints for CRUD operations.  
- Expose **Prometheus metrics** for monitoring.

It also serves a simple **HTML frontend** with forms for file upload, user search, and database management.

---

## ⚙️ Features
- 📂 **Upload file** with `username:password` format.  
- 🔑 **Password hashing** with SHA-512.  
- 🗂️ **Store hashed data** in MongoDB (with unique file hash).  
- 🔎 **Search users** by ID or username.  
- 📜 **CRUD operations** for files:
  - List all files
  - Get file by ID
  - Delete file
  - Update file contents  
- 📊 **Prometheus metrics** at `/metrics` (including request counters).  
- 🌐 Built-in HTML interface for easier usage.

---

