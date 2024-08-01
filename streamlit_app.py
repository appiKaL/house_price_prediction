import streamlit as st
import requests

st.title("House Price Prediction")

feature_names = [
    'bathroomcount', 'bedroomcount', 'constructionyear', 'fireplace',
    'floodingzone', 'furnished', 'garden', 'gardenarea', 'kitchen', 
    'livingarea', 'monthlycharges', 'numberoffacades', 'peb', 'postalcode', 
    'roomcount', 'showercount', 'stateofbuilding', 'subtypeofproperty', 
    'surfaceofplot', 'swimmingpool', 'terrace', 'toiletcount', 
    'typeofproperty', 'typeofsale'
]

feature_inputs = {}

for feature in feature_names:
    feature_inputs[feature] = st.number_input(feature, format="%.5f")

API_URL = "https://your-fastapi-service-url.onrender.com/predict"

if st.button("Predict Price"):
    payload = {feature: feature_inputs[feature] for feature in feature_names}
    
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Price: {result['predicted_price']}")
    else:
        st.error("Error occurred while predicting the price.")
