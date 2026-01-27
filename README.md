# F1 Race Prediction Simulator

## Overview
This project is a **Formula 1 Race Prediction Simulator**. It allows users to:

- View all F1 drivers with profile details and photos
- Filter drivers by year
- Select a race and simulate race predictions using a trained machine learning model
- Explore race results and historical data

The system is built as a **full-stack application** with a **Django REST API backend**, **React frontend**, and **ML model integration**.

---

## Inspiration
The inspiration for this project came from the fascination with Formula 1 racing and the challenge of **predicting race outcomes** using real-world data. F1 fans are eager to analyze drivers’ performances, and combining historical data with machine learning allows creating an interactive simulator.

---

## Project Goal
- Provide **accurate race predictions** based on historical race results and driver performance
- Visualize **driver statistics**, teams, flags, and race results
- Fetch any race by **year** and **name**
- Build a **user-friendly web interface** for exploring F1 drivers and races

---

## Problem it Solves
- F1 fans usually love to predict and see which drivers are likely to perform well in upcoming races,
- Historical performance analysis is scattered and difficult to interpret
- The project provides centralized, interactive insights and data-driven predictions

---

## Why it is Important
- Helps fans **engage with F1 data** and understand trends
- Can be used by analysts for **performance assessment**
- Shows practical application of **ML in sports analytics**
- Demonstrates **full-stack development with Python and React**

---

## Solution & Distinctiveness
- **Backend:** Django REST framework exposes APIs for drivers, races, and race results
- **Frontend:** React with Tailwind CSS for responsive UI
- **ML Integration:** Python-based **Random Forest model** trained on historical F1 data (2022–2025) predicts race outcomes
  - Features include driver past positions, average finishing positions, number of podiums, team, and race-specific attributes
  - Random Forest was chosen because it:
    - Handles **non-linear relationships** well
    - Can manage **categorical features** like teams and drivers
    - Is robust to **outliers** and missing data
    - Produces **probabilistic predictions**, allowing us to rank likely winners
- **Driver Cards:** Unique design with gradient backgrounds, flag icons, and headshots
- **Dynamic Features:** Filters by year and nationality, selectable races for predictions
- **Distinctiveness:** Combines **real F1 data**, **custom ML model**, and **interactive web interface** in one platform

---

## Technologies Used
- **Backend:** Django, Django REST Framework  
  - Provides robust APIs for drivers, races, and predictions
- **Frontend:** React, Tailwind CSS  
  - Fast, interactive UI, responsive design, reusable components
- **Machine Learning:** Python, Scikit-learn / Pandas / NumPy  
  - Random Forest classifier for race prediction
- **Data Sources:** FastF1 API, historical race results
- **Docker:** Containerized backend and frontend for easy deployment
- **Axios:** Handles API requests from React

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
- Learned how **React state management** interacts with backend APIs
- Understood **ML feature building** based on historical sequences
- Gained experience in **deploying a full-stack ML-powered application**

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

# Open backend container shell
docker compose exec web bash


# (Optional) Create superuser
python manage.py createsuperuser

# Run backend server
docker compose exec web python manage.py runserver 0.0.0.0:8000

# Run tests
docker compose exec web python manage.py test

