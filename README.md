# Airbnb Price Predictor Engine (Paris Edition) 🏡🇫🇷

An end-to-end Machine Learning web application that predicts the optimal nightly price for Airbnb listings based on property details, location, host reputation metrics, and guest review scores.

This project features a fully optimized Random Forest regression model served via a FastAPI REST API, connected to a responsive Next.js dashboard.

## 🚀 Live Demo

* **Frontend UI (Vercel):** [Insert your Vercel URL here]
* **Backend API Docs (Render):** [Insert your Render URL here]

## 📊 Dataset & Attribution

* **Source:** [Inside Airbnb](http://insideairbnb.com/)
* **Region:** Paris, Ile-de-France, France
* **Size:** [Insert N] listings (Scraped on [Insert Date])
* **License:** This data is sourced from Inside Airbnb and is used under a [Creative Commons CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/).

### ⚠️ Limitations & Scope

* **Geographical Constraint:** This model was trained exclusively on listings within Paris. Predictions made for properties in other cities or countries will not be accurate.
* **Currency:** All predicted prices are output in **Euros (€)**.

## 🧠 Machine Learning Pipeline

The predictive model was trained on historical Airbnb data, optimizing for a balance between accuracy and production-ready lightweight deployment:

* **Algorithm:** Random Forest Regressor
* **Optimization:** Bounded depth (`max_depth=15`) and leaf constraints (`min_samples_leaf=5`) to prevent overfitting and drastically reduce the `.joblib` payload size for cloud memory limits.
* **Feature Engineering & Selection:**
  * **Geospatial & Property:** `latitude`, `longitude`, `room_type`, `accommodates`, `bedrooms`, `minimum_nights`
  * **Host Metrics:** `host_is_superhost`, `host_response_time`, `host_response_rate`, `host_acceptance_rate`, `host_total_listings_count`
  * **Reviews:** 5-point scores for Rating, Cleanliness, Location, Value, Accuracy, Check-in, and Communication.
  * *Note: Zero-variance or highly redundant columns (like `host_location` being uniformly "Paris") were dropped to reduce noise.*
* **Data Imputation:** Missing values for host response rates and times were handled using median/mode imputation. The imputer was fit strictly on the training set to prevent test data leakage.

## 🛠️ Tech Stack

* **Frontend:** Next.js, React, TypeScript, Tailwind CSS
* **Backend:** Python, FastAPI, Uvicorn, Pydantic
* **Machine Learning:** Scikit-learn, Pandas, Joblib, Random Forest Regressor
* **Deployment:** Vercel (Frontend), Render (Backend)

## 📁 Project Structure

```text
airbnb-prediction-engine/
├── backend/
│   ├── models/            # Saved lightweight .joblib artifacts (train data ignored via LFS/gitignore)
│   ├── src/               # ML training and preprocessing scripts
│   ├── main.py            # FastAPI server & CORS configuration
│   └── requirements.txt   # Python dependencies (Linux/Render compatible)
└── frontend/
    ├── app/               # Next.js App Router UI
    ├── public/            # Static assets
    ├── package.json       # Node dependencies
    └── tailwind.config.js # Styling configurations
```

## 💻 Local Setup Instructions

### 1. Backend (FastAPI + ML Model)

Navigate to the backend directory and set up your Python environment:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

Start the local API server:

```bash
uvicorn main:app --reload
```

*The API will be available at `http://127.0.0.1:8000`. You can view the interactive Swagger UI at `http://127.0.0.1:8000/docs`.*

### 2. Frontend (Next.js)

Open a new terminal, navigate to the frontend directory, and install dependencies:

```bash
cd frontend
npm install
```

Start the development server:

```bash
npm run dev
```

*The UI will be available at `http://localhost:3000`.*

## 👨‍💻 Author

**Sabyasachi Ghosh**

* GitHub: [@sabya-code03](https://github.com/sabya-code03)
