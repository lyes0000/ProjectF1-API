# 🏎️ ProjectF1 API

ProjectF1 is a **Django REST API** that provides Formula 1 data such as race results, driver standings, and more.  
It integrates with the **[FastF1](https://github.com/theOehrly/Fast-F1)** library to fetch and process real-time and historical F1 data, exposing it through clean API endpoints.

---

## 🚀 Features

- 📊 Fetch Formula 1 race results and driver data  
- 🧠 FastF1 data integration for advanced F1 analytics  
- ⚙️ PostgreSQL-backed Django project  
- 🧩 Modular app structure (`core`, `api`, `drivers`, `races`...)  
- 🐳 Fully containerized with Docker & Docker Compose  

---

## ⚙️ Prerequisites

Every team member needs the following installed **before running the project**:

| Tool | Version (or higher) | Download |
|------|---------------------|-----------|
| **Git** | any recent |
| **Docker Desktop** | 4.x or higher | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) |
| **Python** | 3.12+ | [python.org/downloads](https://www.python.org/downloads/) |

> ⚠️ Make sure Docker Desktop is **running** before continuing.  

---

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/lyes0000/ProjectF1-API.git
cd ProjectF1-API

```bash
Docker compose up