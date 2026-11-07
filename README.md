# Airbnb Price Predictor Engine 🏡🤖

An end-to-end Machine Learning web application that predicts the optimal nightly price for Airbnb listings based on property details, host reputation metrics, and guest review scores. 

This project features a fully optimized Random Forest regression model served via a FastAPI REST API, connected to a responsive, dark-themed Next.js dashboard.

## 🚀 Live Demo
* **Frontend UI (Vercel):**  https://airbnb-prediction-engine.vercel.app
* **Backend API Docs (Render):** https://airbnb-prediction-engine.onrender.com/docs

## 🛠️ Tech Stack
* **Frontend:** Next.js, React, TypeScript, Tailwind CSS
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **Machine Learning:** Scikit-learn, Pandas, Joblib, Random Forest Regressor
* **Deployment:** Vercel (Frontend), Render (Backend)

## 🧠 Machine Learning Pipeline
The predictive model was trained on historical Airbnb data, optimizing for a balance between accuracy and production-ready lightweight deployment:
* **Algorithm:** Random Forest Regressor
* **Optimization:** Bounded depth (`max_depth=15`) and leaf constraints (`min_samples_leaf=5`) to prevent overfitting and drastically reduce the `.joblib` payload size for cloud memory limits.
* **Features Used:** Accommodates, Bedrooms, Minimum Nights, Host Response/Acceptance Rates, Superhost Status, and 5-point Review Metrics (Cleanliness, Location, Value, etc.).

## 📁 Project Structure
```text
airbnb-prediction-engine/
├── backend/
│   ├── models/            # Saved lightweight .joblib artifacts
│   ├── src/               # ML training and preprocessing scripts
│   ├── main.py            # FastAPI server & CORS configuration
│   └── requirements.txt   # Python dependencies (Linux/Render compatible)
└── frontend/
    ├── app/               # Next.js App Router UI
    ├── public/            # Static assets
    ├── package.json       # Node dependencies
    └── tailwind.config.js # Styling configurations
