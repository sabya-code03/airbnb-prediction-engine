import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
import joblib

# 1. FAIL FAST ON STARTUP
# If the model doesn't exist or fails to load, the server crashes immediately
# instead of returning confusing 400 errors to the user later.
MODEL_PATH = "models/best_model.joblib"
if not os.path.exists(MODEL_PATH):
    print(f"CRITICAL ERROR: Model file not found at {MODEL_PATH}")
    sys.exit(1) 

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(f"CRITICAL ERROR: Failed to load model: {e}")
    sys.exit(1)

app = FastAPI(title="Airbnb Price Predictor API")

# Locked down CORS to your specific frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://airbnb-prediction-engine.vercel.app"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. STRICT PYDANTIC VALIDATION
class ListingData(BaseModel):
    # Capacity constraints
    accommodates: int = Field(..., ge=1, le=16)
    bedrooms: int = Field(..., ge=0)
    minimum_nights: int = Field(..., ge=1)
    
    # Rates strictly bound between 0 and 1
    host_response_rate: float = Field(..., ge=0.0, le=1.0)
    host_acceptance_rate: float = Field(..., ge=0.0, le=1.0)
    
    # Categorical Literals
    room_type: Literal["Entire home/apt", "Private room", "Shared room", "Hotel room"]
    city: Literal["Paris"] # Add your exact dataset cities here
    
    # Booleans explicitly mapped to "t" or "f"
    host_is_superhost: Literal["t", "f"]
    host_has_profile_pic: Literal["t", "f"]
    host_identity_verified: Literal["t", "f"]
    instant_bookable: Literal["t", "f"]
    
    # Review scores bound between 0 and 5
    review_scores_rating: float = Field(..., ge=0.0, le=5.0)
    review_scores_cleanliness: float = Field(..., ge=0.0, le=5.0)
    review_scores_location: float = Field(..., ge=0.0, le=5.0)
    review_scores_value: float = Field(..., ge=0.0, le=5.0)
    review_scores_communication: float = Field(..., ge=0.0, le=5.0)
    review_scores_accuracy: float = Field(..., ge=0.0, le=5.0)
    review_scores_checkin: float = Field(..., ge=0.0, le=5.0)

# 3. HEALTH ENDPOINT
@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

# 4. PREDICT ENDPOINT WITH RANGE AND 500 ERRORS
@app.post("/predict")
def predict_price(data: ListingData):
    try:
        # Convert incoming validated model to DataFrame
        df = pd.DataFrame([data.model_dump()])
        
        # Generate prediction
        predicted_price = float(model.predict(df)[0])
        
        # Calculate a reasonable price range (e.g., +/- 15% for market variance)
        lower_bound = round(predicted_price * 0.85, 2)
        upper_bound = round(predicted_price * 1.15, 2)
        
        return {
            "predicted_price": round(predicted_price, 2),
            "price_range": [lower_bound, upper_bound]
        }
    except Exception as e:
        # Return a clean 500 Internal Server Error if something breaks during prediction
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")