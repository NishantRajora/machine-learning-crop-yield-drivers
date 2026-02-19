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

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# ================================
# HTML Template (Inside Python)
# ================================

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Crop Yield Prediction</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f4f4f4;
            text-align: center;
        }
        .container {
            background: white;
            padding: 20px;
            margin: auto;
            width: 50%;
            border-radius: 10px;
            box-shadow: 0px 0px 10px gray;
        }
        input {
            margin: 5px;
            padding: 5px;
            width: 60%;
        }
        button {
            padding: 10px;
            background-color: green;
            color: white;
            border: none;
            border-radius: 5px;
        }
        h2 {
            color: green;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>🌾 Crop Yield Prediction</h2>

        <form method="POST">
            <input type="number" name="Year" placeholder="Year" required><br>
            <input type="number" name="Decade" placeholder="Decade" required><br>
            <input type="number" name="State_encoded" placeholder="State Encoded" required><br>
            <input type="number" name="Crop_encoded" placeholder="Crop Encoded" required><br>
            <input type="number" name="Season_encoded" placeholder="Season Encoded" required><br>
            <input type="number" step="any" name="Area_ha" placeholder="Area (ha)" required><br>
            <input type="number" step="any" name="N_req_kg_per_ha" placeholder="N (kg/ha)" required><br>
            <input type="number" step="any" name="P_req_kg_per_ha" placeholder="P (kg/ha)" required><br>
            <input type="number" step="any" name="K_req_kg_per_ha" placeholder="K (kg/ha)" required><br>
            <input type="number" step="any" name="Temperature_C" placeholder="Temperature (C)" required><br>
            <input type="number" step="any" name="Humidity_%" placeholder="Humidity (%)" required><br>
            <input type="number" step="any" name="pH" placeholder="Soil pH" required><br>
            <input type="number" step="any" name="Rainfall_mm" placeholder="Rainfall (mm)" required><br>
            <input type="number" step="any" name="Wind_Speed_m_s" placeholder="Wind Speed (m/s)" required><br>
            <input type="number" step="any" name="Solar_Radiation_MJ_m2_day" placeholder="Solar Radiation" required><br>
            
            <br>
            <button type="submit">Predict Yield</button>
        </form>

        <h3>{{ prediction }}</h3>
    </div>
</body>
</html>
"""

# ================================
# Route
# ================================

@app.route("/", methods=["GET", "POST"])
def home():
    prediction_text = ""

    if request.method == "POST":
        try:
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

            prediction_text = f"🌾 Predicted Yield: {round(prediction[0],2)} kg/ha"

        except Exception as e:
            prediction_text = f"Error: {str(e)}"

    return render_template_string(HTML_PAGE, prediction=prediction_text)

# ================================
# Run Server
# ================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)