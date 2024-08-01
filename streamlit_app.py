import streamlit as st
import requests

st.title("House Price Prediction")

feature1 = st.number_input("Feature 1")
feature2 = st.number_input("Feature 2")
feature3 = st.number_input("Feature 3")

API_URL = "https://house-price-prediction-qd90.onrender.com"

if st.button("Predict Price"):
    payload = {
        "feature1": feature1,
        "feature2": feature2,
        "feature3": feature3,
    }
    response = requests.post(API_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Price: {result['predicted_price']}")
    else:
        st.error("Error occurred while predicting the price.")
