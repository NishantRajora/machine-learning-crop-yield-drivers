"""
Streamlit Frontend for Crop Yield Prediction
=============================================
This app sends user inputs to your hosted FastAPI backend and displays results.

Install dependencies:
    pip install streamlit requests

Run:
    streamlit run streamlit_app.py

⚠️ IMPORTANT: Replace API_URL below with your deployed FastAPI URL.
"""

import streamlit as st
import requests

# =============================================
# 🔧 CHANGE THIS to your deployed API URL
API_URL = "https://your-app.onrender.com/predict"
# =============================================

# --- DATA ---
STATES = sorted([
    "Andhra Pradesh", "Assam", "Bihar", "Chhattisgarh", "Gujarat",
    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Orissa", "Punjab", "Rajasthan",
    "Tamil Nadu", "Telangana", "Uttar Pradesh", "Uttarakhand", "West Bengal"
])
CROPS = sorted(["Chickpea", "Cotton", "Maize", "Rice"])
SEASONS = sorted(["Autumn", "Kharif", "Rabi", "Summer", "Unknown", "Whole Year", "Winter"])

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🌱 Crop Yield Intelligence",
    page_icon="🌾",
    layout="centered"
)

# --- HEADER ---
st.markdown("""
    <h1 style='color:#2ecc71; text-align:center;'>🌱 Crop Yield Intelligence</h1>
    <p style='text-align:center; color:gray;'>Predict crop yield using soil, climate & crop data</p>
    <hr>
""", unsafe_allow_html=True)

# --- SAMPLE DATA BUTTON ---
if st.button("🧪 Load Sample Data"):
    st.session_state.update({
        "state": "Chhattisgarh", "crop": "Rice", "season": "Rabi",
        "year": 1966, "temp": 25.0, "rainfall": 1200.0,
        "n": 8.44, "p": 4.05, "k": 7.43, "ph": 6.5, "area": 548000.0
    })

# --- INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Crop & Location")
    state   = st.selectbox("State",  STATES,  index=STATES.index(st.session_state.get("state", STATES[0])))
    crop    = st.selectbox("Crop",   CROPS,   index=CROPS.index(st.session_state.get("crop", CROPS[0])))
    season  = st.selectbox("Season", SEASONS, index=SEASONS.index(st.session_state.get("season", SEASONS[0])))
    year    = st.number_input("Year",        min_value=1900, max_value=2100, value=st.session_state.get("year", 2010))
    temp    = st.number_input("Temperature (°C)", value=st.session_state.get("temp", 25.0), step=0.1)
    rainfall= st.number_input("Rainfall (mm)",    value=st.session_state.get("rainfall", 1200.0), step=1.0)

with col2:
    st.subheader("🧪 Soil Nutrients")
    n    = st.number_input("Nitrogen (N)",   value=st.session_state.get("n", 8.44),   step=0.01)
    p    = st.number_input("Phosphorus (P)", value=st.session_state.get("p", 4.05),   step=0.01)
    k    = st.number_input("Potassium (K)",  value=st.session_state.get("k", 7.43),   step=0.01)
    ph   = st.number_input("Soil pH",        value=st.session_state.get("ph", 6.5),   step=0.1,  min_value=0.0, max_value=14.0)
    area = st.number_input("Area (ha)",      value=st.session_state.get("area", 548000.0), step=100.0)

# --- PREDICT BUTTON ---
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Analyze & Predict Yield", use_container_width=True, type="primary"):
    payload = {
        "State": state, "Crop": crop, "Season": season,
        "Year": year, "Temp": temp, "Rainfall": rainfall,
        "N": n, "P": p, "K": k, "pH": ph, "Area_ha": area
    }

    with st.spinner("Contacting prediction server..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=15)
            result = response.json()

            if "prediction_kg_per_ha" in result:
                pred = result["prediction_kg_per_ha"]
                st.markdown(f"""
                    <div style='background:#f0fff4; border:2px solid #2ecc71; border-radius:15px;
                                padding:25px; text-align:center; margin-top:20px;'>
                        <h2 style='color:#155724; margin:0;'>🌾 Predicted Yield</h2>
                        <h1 style='color:#2ecc71; font-size:3rem; margin:10px 0;'>{pred} kg/ha</h1>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"API Error: {result.get('error', 'Unknown error')}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the API. Make sure your FastAPI server is running and the URL is correct.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The server may be starting up (cold start). Try again in a moment.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
