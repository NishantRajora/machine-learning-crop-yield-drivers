from flask import Flask, request, render_template
import pandas as pd
import joblib
import os

# Initialize Flask and explicitly tell it where templates are
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))

# ================================
# Load model & scaler
# ================================
try:
    model = joblib.load(os.path.join(BASE_DIR, "xgboost_model.pkl"))
    scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
except Exception as e:
    print(f"Error loading model files: {e}")

# ================================
# Mappings
# ================================
STATE_MAP = {
    "Andhra Pradesh": 0, "Assam": 1, "Bihar": 2, "Chhattisgarh": 3, "Gujarat": 4,
    "Haryana": 5, "Himachal Pradesh": 6, "Jharkhand": 7, "Karnataka": 8, "Kerala": 9,
    "Madhya Pradesh": 10, "Maharashtra": 11, "Orissa": 12, "Punjab": 13, 
    "Rajasthan": 14, "Tamil Nadu": 15, "Telangana": 16, "Uttar Pradesh": 17, 
    "Uttarakhand": 18, "West Bengal": 19
}

CROP_MAP = {"Chickpea": 0, "Cotton": 1, "Maize": 2, "Rice": 3}

SEASON_MAP = {
    "Autumn": 0, "Kharif": 1, "Rabi": 2, "Summer": 3, 
    "Unknown": 4, "Whole Year": 5, "Winter": 6
}

@app.route("/", methods=["GET", "POST"])
def home():
    prediction_text = ""
    if request.method == "POST":
        try:
            # Collect data from form
            input_data = {
                'Year': float(request.form['Year']),
                'Decade': float(request.form['Decade']),
                'State_encoded': float(request.form['State_encoded']),
                'Crop_encoded': float(request.form['Crop_encoded']),
                'Season_encoded': float(request.form['Season_encoded']),
                'Area_ha': float(request.form['Area_ha']),
                'N_req_kg_per_ha': float(request.form['N_req_kg_per_ha']),
                'P_req_kg_per_ha': float(request.form['P_req_kg_per_ha']),
                'K_req_kg_per_ha': float(request.form['K_req_kg_per_ha']),
                'Temperature_C': float(request.form['Temperature_C']),
                'Humidity_%': float(request.form['Humidity_%']),
                'pH': float(request.form['pH']),
                'Rainfall_mm': float(request.form['Rainfall_mm']),
                'Wind_Speed_m_s': float(request.form['Wind_Speed_m_s']),
                'Solar_Radiation_MJ_m2_day': float(request.form['Solar_Radiation_MJ_m2_day'])
            }

            df_input = pd.DataFrame([input_data])
            
            # Use the feature names the scaler expects
            df_input = df_input[scaler.feature_names_in_]
            df_scaled = scaler.transform(df_input)
            prediction = model.predict(df_scaled)

            prediction_text = f"✅ Predicted Yield: {round(float(prediction[0]), 2)} kg/ha"

        except Exception as e:
            prediction_text = f"❌ Error: {str(e)}"

    return render_template(
        "index.html", 
        prediction=prediction_text, 
        states=STATE_MAP, 
        crops=CROP_MAP, 
        seasons=SEASON_MAP
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)