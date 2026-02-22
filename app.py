import pandas as pd
import joblib
from flask import Flask, render_template, request

app = Flask(__name__)

# --- LOAD ASSETS ---
model = joblib.load("xgboost_model.pkl")
scaler = joblib.load("scaler.pkl")

# --- MAPPINGS ---
STATE_MAP = {"Andhra Pradesh": 0, "Assam": 1, "Bihar": 2, "Chhattisgarh": 3, "Gujarat": 4, "Haryana": 5, "Himachal Pradesh": 6, "Jharkhand": 7, "Karnataka": 8, "Kerala": 9, "Madhya Pradesh": 10, "Maharashtra": 11, "Orissa": 12, "Punjab": 13, "Rajasthan": 14, "Tamil Nadu": 15, "Telangana": 16, "Uttar Pradesh": 17, "Uttarakhand": 18, "West Bengal": 19}
CROP_MAP = {"Chickpea": 0, "Cotton": 1, "Maize": 2, "Rice": 3}
SEASON_MAP = {"Autumn": 0, "Kharif": 1, "Rabi": 2, "Summer": 3, "Unknown": 4, "Whole Year": 5, "Winter": 6}

@app.route('/')
def home():
    return render_template('index.html', 
                           states=sorted(STATE_MAP.keys()), 
                           crops=sorted(CROP_MAP.keys()), 
                           seasons=sorted(SEASON_MAP.keys()),
                           inputs={})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        year_val = int(request.form['Year'])
        
        # Build dictionary for Scaling
        ui_data = {
            'Year': year_val,
            'Decade': (year_val // 10) * 10,
            'State_encoded': STATE_MAP[request.form['State']],
            'Crop_encoded': CROP_MAP[request.form['Crop']],
            'Season_encoded': SEASON_MAP[request.form['Season']],
            'Area_ha': float(request.form['Area_ha']),
            'N_req_kg_per_ha': float(request.form['N']),
            'P_req_kg_per_ha': float(request.form['P']),
            'K_req_kg_per_ha': float(request.form['K']),
            'Temperature_C': float(request.form['Temp']),
            'Humidity_%': 80, # Default constant
            'pH': float(request.form['pH']),
            'Rainfall_mm': float(request.form['Rainfall']),
            'Wind_Speed_m_s': 2.0, # Default constant
            'Solar_Radiation_MJ_m2_day': 18 # Default constant
        }
        
        # Scale and Predict
        df = pd.DataFrame([ui_data])
        scaled_data = scaler.transform(df)
        scaled_df = pd.DataFrame(scaled_data, columns=scaler.feature_names_in_)
        
        model_features = model.get_booster().feature_names
        prediction = model.predict(scaled_df[model_features])[0]
        
        return render_template('index.html', 
                               prediction=round(float(prediction), 2), 
                               states=sorted(STATE_MAP.keys()), 
                               crops=sorted(CROP_MAP.keys()),
                               seasons=sorted(SEASON_MAP.keys()),
                               inputs=request.form)
    except Exception as e:
        return f"Prediction Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)