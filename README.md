# F1 Race Prediction Simulator

## Link to the Frontend Repository:
**https://github.com/HiraethSerra/ProjectF1.git**

## Overview
This project is a **Formula 1 Race Prediction Simulator**. It allows users to:

- View all F1 drivers with profile details and photos
- Filter drivers by year
- Select a race and simulate race predictions using a trained machine learning model
- Explore race results and historical data

The system is built with a **Django REST API backend** and **ML model integration**.

---

## Inspiration
The inspiration for this project came from the fascination with Formula 1 racing and the challenge of **predicting race outcomes** using real-world data. F1 fans are eager to analyze drivers’ performances, and combining historical data with machine learning allows creating an interactive simulator.

---

## Project Goal
- Provide **accurate race predictions** based on historical race results and driver performance
- Return **driver statistics**, teams, flags, and race results
- Fetch any race by **year** and **name**

---

## Technologies Used
- **Backend:** Django, Django REST Framework, PostgreSQL
  - Provides robust APIs for drivers, races, and predictions
- **Machine Learning:** Python, Scikit-learn / Pandas / NumPy  
  - Random Forest classifier for race prediction
- **Data Sources:** FastF1 API
- **Docker:** Containerized backend and frontend for easy deployment

---

## Why this Project is the Best
- Interactive, real-time F1 simulation
- Combines **data analysis, ML, and full-stack development**
- Unique driver cards with team gradients, flags, and headshots
- Predicts upcoming races using **historical data**, not just static results

---

## Lessons Learned
- Working with **real-world F1 datasets** requires careful preprocessing
- Learned **dynamic filtering in Django** and **relationship handling in models**
- Understood **ML feature building** based on historical sequences

---

## Project Setup / Installation

### Clone Repository
```bash
git clone https://github.com/lyes0000/ProjectF1-API.git
cd ProjectF1-API

# Build Docker images
docker compose build

# Start containers
docker compose up

# Make migrations
docker compose exec web python manage.py makemigrations

# Apply migrations
docker compose exec web python manage.py migrate

# Fetch seasons to train the model:
docker compose exec web python manage.py fetch_all_seasons # this is set to fetch from 2022 to 2024 by default

# Fetch a specific season by year:
docker compose exec web python manage.py fetch_season --year 2022

# Fetch one specific race in a given year: 
docker compose exec web python manage.py fetch_f1_data

# Run ML model training
docker compose exec web python manage.py train_ml_model

# (Optional) Create superuser
python manage.py createsuperuser

# Run backend server
docker compose exec web python manage.py runserver 0.0.0.0:8000
