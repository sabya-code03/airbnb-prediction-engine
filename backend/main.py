from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os

app = FastAPI(title="Airbnb Price Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load artifacts safely on startup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    model = joblib.load(os.path.join(BASE_DIR, 'models', 'best_model.joblib'))
    preprocessor = joblib.load(os.path.join(BASE_DIR, 'models', 'preprocessor.joblib'))
except Exception as e:
    print(f"Error loading artifacts: {e}")

# Define the expected input payload
class ListingData(BaseModel):
    # Update these fields to match your exact retained numeric and categorical columns
    accommodates: int
    bedrooms: int
    minimum_nights: int
    room_type: str
    city: str 
    # Add the missing model features with their correct data types
    host_has_profile_pic: str
    instant_bookable: str
    longitude: float
    host_response_time: str
    review_scores_checkin: float
    review_scores_rating: float
    host_acceptance_rate: float
    review_scores_value: float
    host_response_rate: float
    host_total_listings_count: int
    latitude: float
    review_scores_communication: float
    review_scores_cleanliness: float
    host_identity_verified: str
    review_scores_location: float
    maximum_nights: int
    host_is_superhost: str
    review_scores_accuracy: float

@app.post("/predict")
def predict_price(data: ListingData):
    try:
        # Convert incoming JSON payload to a DataFrame
        input_df = pd.DataFrame([data.model_dump()])
        
        # Apply the exact scaling and encoding from training
        processed_input = preprocessor.transform(input_df)
        
        # Generate the prediction
        prediction = model.predict(processed_input)
        
        return {"predicted_price": round(float(prediction[0]), 2)}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))