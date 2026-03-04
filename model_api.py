from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load model and scaler
model = joblib.load("xgboost_model.pkl")
scaler = joblib.load("scaler.pkl")

STATE_MAP = {"Andhra Pradesh": 0, "Assam": 1, "Bihar": 2, "Chhattisgarh": 3, "Gujarat": 4, "Haryana": 5,
             "Himachal Pradesh": 6, "Jharkhand": 7, "Karnataka": 8, "Kerala": 9, "Madhya Pradesh": 10,
             "Maharashtra": 11, "Orissa": 12, "Punjab": 13, "Rajasthan": 14, "Tamil Nadu": 15,
             "Telangana": 16, "Uttar Pradesh": 17, "Uttarakhand": 18, "West Bengal": 19}

CROP_MAP = {"Chickpea": 0, "Cotton": 1, "Maize": 2, "Rice": 3}

SEASON_MAP = {"Autumn": 0, "Kharif": 1, "Rabi": 2, "Summer": 3, "Unknown": 4, "Whole Year": 5, "Winter": 6}


@app.route("/predict", methods=["POST"])
def predict():

    data = request.json

    year_val = int(data["Year"])

    ui_data = {
        'Year': year_val,
        'Decade': (year_val // 10) * 10,
        'State_encoded': STATE_MAP[data["State"]],
        'Crop_encoded': CROP_MAP[data["Crop"]],
        'Season_encoded': SEASON_MAP[data["Season"]],
        'Area_ha': float(data["Area_ha"]),
        'N_req_kg_per_ha': float(data["N"]),
        'P_req_kg_per_ha': float(data["P"]),
        'K_req_kg_per_ha': float(data["K"]),
        'Temperature_C': float(data["Temp"]),
        'Humidity_%': 80,
        'pH': float(data["pH"]),
        'Rainfall_mm': float(data["Rainfall"]),
        'Wind_Speed_m_s': 2.0,
        'Solar_Radiation_MJ_m2_day': 18
    }

    df = pd.DataFrame([ui_data])

    scaled = scaler.transform(df)

    scaled_df = pd.DataFrame(scaled, columns=scaler.feature_names_in_)

    model_features = model.get_booster().feature_names

    prediction = model.predict(scaled_df[model_features])[0]

    return jsonify({"prediction": float(prediction)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)