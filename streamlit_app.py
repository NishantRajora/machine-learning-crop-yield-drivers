import streamlit as st
import requests

st.title("Crop Yield Intelligence")

state = st.selectbox("State",
["Andhra Pradesh","Assam","Bihar","Chhattisgarh","Gujarat","Haryana",
"Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
"Maharashtra","Orissa","Punjab","Rajasthan","Tamil Nadu",
"Telangana","Uttar Pradesh","Uttarakhand","West Bengal"])

crop = st.selectbox("Crop",["Chickpea","Cotton","Maize","Rice"])

season = st.selectbox("Season",
["Autumn","Kharif","Rabi","Summer","Unknown","Whole Year","Winter"])

year = st.number_input("Year")
temp = st.number_input("Temperature")
rainfall = st.number_input("Rainfall")

n = st.number_input("Nitrogen")
p = st.number_input("Phosphorus")
k = st.number_input("Potassium")

ph = st.number_input("Soil pH")
area = st.number_input("Area (ha)")

if st.button("Predict Yield"):

    data = {
        "State":state,
        "Crop":crop,
        "Season":season,
        "Year":year,
        "Temp":temp,
        "Rainfall":rainfall,
        "N":n,
        "P":p,
        "K":k,
        "pH":ph,
        "Area_ha":area
    }

    response = requests.post(
        "http://10.248.84.97:5000",
        json=data
    )

    result = response.json()

    st.success(f"Predicted Yield: {result['prediction']} kg/ha")