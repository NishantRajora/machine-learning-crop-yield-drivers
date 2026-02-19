from flask import Flask, request, render_template_string
import pandas as pd
import joblib
import os

app = Flask(__name__)

# ================================
# Load model & scaler safely
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "xgboost_model.pkl")
scaler_path = os.path.join(BASE_DIR, "scaler.pkl")

# Note: Ensure these files exist in your directory
model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# ================================
# Mappings (State, Crop, Season)
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

# ================================
# HTML Template
# ================================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Crop Yield Prediction</title>
    <style>
        body { font-family: 'Segoe UI', Arial; background-color: #f0f2f5; text-align: center; padding: 20px; }
        .container { background: white; padding: 30px; margin: auto; width: 60%; border-radius: 15px; box-shadow: 0px 4px 15px rgba(0,0,0,0.1); }
        .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align: left; }
        .input-group { margin-bottom: 15px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; color: #333; }
        input, select { padding: 10px; width: 90%; border: 1px solid #ccc; border-radius: 5px; }
        button { grid-column: span 2; padding: 15px; background-color: #28a745; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 10px; }
        button:hover { background-color: #218838; }
        h2 { color: #2d5a27; }
        .result { margin-top: 20px; padding: 15px; background: #e9f7ef; border-radius: 10px; color: #155724; font-weight: bold; }
    </style>
    <script>
        function updateDecade() {
            const year = document.getElementById('Year').value;
            if (year) {
                // Logic: 2024 -> 2020
                const decade = Math.floor(year / 10) * 10;
                document.getElementById('Decade').value = decade;
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h2>🌾 Crop Yield Prediction</h2>
        <form method="POST">
            <div class="grid-container">
                <div class="input-group">
                    <label>Year</label>
                    <input type="number" id="Year" name="Year" oninput="updateDecade()" placeholder="e.g. 2024" required>
                </div>
                <div class="input-group">
                    <label>Decade</label>
                    <input type="number" id="Decade" name="Decade" readonly style="background-color: #eee;">
                </div>
                
                <div class="input-group">
                    <label>State</label>
                    <select name="State_encoded" required>
                        {% for state in states %}<option value="{{ states[state] }}">{{ state }}</option>{% endfor %}
                    </select>
                </div>

                <div class="input-group">
                    <label>Crop</label>
                    <select name="Crop_encoded" required>
                        {% for crop in crops %}<option value="{{ crops[crop] }}">{{ crop }}</option>{% endfor %}
                    </select>
                </div>

                <div class="input-group">
                    <label>Season</label>
                    <select name="Season_encoded" required>
                        {% for season in seasons %}<option value="{{ seasons[season] }}">{{ season }}</option>{% endfor %}
                    </select>
                </div>

                <div class="input-group">
                    <label>Area (ha)</label>
                    <input type="number" step="any" name="Area_ha" required>
                </div>

                <div class="input-group"><label>N (kg/ha)</label><input type="number" step="any" name="N_req_kg_per_ha" required></div>
                <div class="input-group"><label>P (kg/ha)</label><input type="number" step="any" name="P_req_kg_per_ha" required></div>
                <div class="input-group"><label>K (kg/ha)</label><input type="number" step="any" name="K_req_kg_per_ha" required></div>
                <div class="input-group"><label>Temp (°C)</label><input type="number" step="any" name="Temperature_C" required></div>
                <div class="input-group"><label>Humidity (%)</label><input type="number" step="any" name="Humidity_%" required></div>
                <div class="input-group"><label>Soil pH</label><input type="number" step="any" name="pH" required></div>
                <div class="input-group"><label>Rainfall (mm)</label><input type="number" step="any" name="Rainfall_mm" required></div>
                <div class="input-group"><label>Wind (m/s)</label><input type="number" step="any" name="Wind_Speed_m_s" required></div>
                <div class="input-group"><label>Solar Rad.</label><input type="number" step="any" name="Solar_Radiation_MJ_m2_day" required></div>
                
                <button type="submit">Analyze & Predict Yield</button>
            </div>
        </form>

        {% if prediction %}
        <div class="result">{{ prediction }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

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
            df_input = df_input[scaler.feature_names_in_]
            df_scaled = scaler.transform(df_input)
            prediction = model.predict(df_scaled)

            prediction_text = f"✅ Predicted Yield: {round(float(prediction[0]), 2)} kg/ha"

        except Exception as e:
            prediction_text = f"❌ Error: {str(e)}"

    return render_template_string(
        HTML_PAGE, 
        prediction=prediction_text, 
        states=STATE_MAP, 
        crops=CROP_MAP, 
        seasons=SEASON_MAP
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)