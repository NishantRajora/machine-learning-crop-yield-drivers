"""
FastAPI Backend for Crop Yield Prediction
==========================================
Host this on: Render, Railway, Hugging Face Spaces, or any cloud server.

Install dependencies:
    pip install fastapi uvicorn pandas joblib scikit-learn xgboost

Run locally:
    uvicorn api:app --reload

Then deploy and note your public URL, e.g.:
    https://your-app.onrender.com
"""

from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(title="Crop Yield Prediction API")

# --- LOAD MODEL & SCALER ---
model = joblib.load("xgboost_model.pkl")
scaler = joblib.load("scaler.pkl")

# --- ENCODINGS ---
STATE_MAP = {
    "Andhra Pradesh": 0, "Assam": 1, "Bihar": 2, "Chhattisgarh": 3,
    "Gujarat": 4, "Haryana": 5, "Himachal Pradesh": 6, "Jharkhand": 7,
    "Karnataka": 8, "Kerala": 9, "Madhya Pradesh": 10, "Maharashtra": 11,
    "Orissa": 12, "Punjab": 13, "Rajasthan": 14, "Tamil Nadu": 15,
    "Telangana": 16, "Uttar Pradesh": 17, "Uttarakhand": 18, "West Bengal": 19
}
CROP_MAP = {"Chickpea": 0, "Cotton": 1, "Maize": 2, "Rice": 3}
SEASON_MAP = {
    "Autumn": 0, "Kharif": 1, "Rabi": 2, "Summer": 3,
    "Unknown": 4, "Whole Year": 5, "Winter": 6
}

# --- REQUEST SCHEMA ---
class PredictionRequest(BaseModel):
    State: str
    Crop: str
    Season: str
    Year: int
    Temp: float
    Rainfall: float
    N: float
    P: float
    K: float
    pH: float
    Area_ha: float


# --- HEALTH CHECK ---
@app.get("/")
def root():
    return {"status": "Crop Yield API is running ✅"}


# --- PREDICTION ENDPOINT ---
@app.post("/predict")
def predict(data: PredictionRequest):
    try:
        year_val = data.Year

        ui_data = {
            'Year': year_val,
            'Decade': (year_val // 10) * 10,
            'State_encoded': STATE_MAP[data.State],
            'Crop_encoded': CROP_MAP[data.Crop],
            'Season_encoded': SEASON_MAP[data.Season],
            'Area_ha': data.Area_ha,
            'N_req_kg_per_ha': data.N,
            'P_req_kg_per_ha': data.P,
            'K_req_kg_per_ha': data.K,
            'Temperature_C': data.Temp,
            'Humidity_%': 80,             # Default constant
            'pH': data.pH,
            'Rainfall_mm': data.Rainfall,
            'Wind_Speed_m_s': 2.0,        # Default constant
            'Solar_Radiation_MJ_m2_day': 18  # Default constant
        }

        df = pd.DataFrame([ui_data])
        scaled_data = scaler.transform(df)
        scaled_df = pd.DataFrame(scaled_data, columns=scaler.feature_names_in_)

        model_features = model.get_booster().feature_names
        prediction = model.predict(scaled_df[model_features])[0]

        return {"prediction_kg_per_ha": round(float(prediction), 2)}

    except KeyError as e:
        return {"error": f"Invalid input value: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}
