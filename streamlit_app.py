import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="House Price Prediction",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.9);
    }
    .css-18e3th9 {
        font-family: 'Arial', sans-serif;
        color: #333333;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
        font-family: 'Arial', sans-serif';
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center; color: #333;'>House Price Prediction</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

floodingzone_options = {
    'NON_FLOOD_ZONE': 'Non flood zone', 
    'POSSIBLE_FLOOD_ZONE': 'Possible flood zone', 
    'RECOGNIZED_FLOOD_ZONE': 'Recognized flood zone', 
    'CIRCUMSCRIBED_WATERSIDE_ZONE': 'Circumscribed waterside zone', 
    'POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE': 'Possible and circumscribed flood zone', 
    'RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE': 'Recognized and circumscribed waterside flood zone', 
    'RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE': 'Recognized and circumscribed flood zone', 
    'CIRCUMSCRIBED_FLOOD_ZONE': 'Circumscribed flood zone', 
    'POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE': 'Possible and circumscribed waterside zone'
}

kitchen_options = {
    'INSTALLED': 'Installed', 
    'HYPER_EQUIPPED': 'Hyper equipped', 
    'SEMI_EQUIPPED': 'Semi equipped', 
    'USA_INSTALLED': 'USA installed', 
    'NOT_INSTALLED': 'Not installed', 
    'USA_HYPER_EQUIPPED': 'USA hyper equipped', 
    'USA_SEMI_EQUIPPED': 'USA semi equipped', 
    'USA_UNINSTALLED': 'USA uninstalled'
}

peb_options = {
    'D': 'D', 'B': 'B', 'F': 'F', 'E': 'E', 'C': 'C', 
    'A': 'A', 'G': 'G', 'A++': 'A++', 'A+': 'A+', 'B_A': 'B/A', 
    'A_A+': 'A/A+', 'E_D': 'E/D', 'E_C': 'E/C', 'F_C': 'F/C', 
    'F_D': 'F/D', 'G_F': 'G/F', 'G_C': 'G/C', 'F_E': 'F/E'
}

stateofbuilding_options = {
    'GOOD': 'Good', 
    'TO_BE_DONE_UP': 'To be done up', 
    'AS_NEW': 'As new', 
    'TO_RENOVATE': 'To renovate', 
    'TO_RESTORE': 'To restore', 
    'JUST_RENOVATED': 'Just renovated'
}

subtypeofproperty_options = {
    'flat_studio': 'Flat/Studio', 
    'apartment_block': 'Apartment block', 
    'house': 'House', 
    'apartment': 'Apartment', 
    'villa': 'Villa', 
    'kot': 'Kot', 
    'ground_floor': 'Ground floor', 
    'mixed_use_building': 'Mixed use building', 
    'penthouse': 'Penthouse', 
    'loft': 'Loft', 
    'duplex': 'Duplex', 
    'town_house': 'Town house', 
    'service_flat': 'Service flat', 
    'mansion': 'Mansion', 
    'triplex': 'Triplex', 
    'exceptional_property': 'Exceptional property', 
    'farmhouse': 'Farmhouse', 
    'bungalow': 'Bungalow', 
    'country_cottage': 'Country cottage', 
    'castle': 'Castle', 
    'manor_house': 'Manor house', 
    'chalet': 'Chalet', 
    'other_property': 'Other property', 
    'show_house': 'Show house', 
    'pavilion': 'Pavilion'
}

typeofsale_options = {
    'residential_sale': 'Residential sale', 
    'residential_monthly_rent': 'Residential monthly rent', 
    'annuity_without_lump_sum': 'Annuity without lump sum', 
    'annuity_monthly_amount': 'Annuity monthly amount', 
    'homes_to_build': 'Homes to build', 
    'annuity_lump_sum': 'Annuity lump sum'
}

with col1:
    BathroomCount = st.number_input('Bathroom Count', format="%.0f")
    BedroomCount = st.number_input('Bedroom Count', format="%.0f")
    ConstructionYear = st.number_input('Construction Year', format="%.0f")
    Fireplace = st.checkbox('Fireplace')
    FloodingZone = st.selectbox('Flooding Zone', list(floodingzone_options.values()))
    Furnished = st.checkbox('Furnished')
    Garden = st.checkbox('Garden')
    GardenArea = st.number_input('Garden Area', format="%.0f")
    Kitchen = st.selectbox('Kitchen', list(kitchen_options.values()))

with col2:
    LivingArea = st.number_input('Living Area', format="%.0f")
    MonthlyCharges = st.number_input('Monthly Charges', format="%.0f")
    NumberOfFacades = st.number_input('Number of Facades', format="%.0f")
    PEB = st.selectbox('PEB', list(peb_options.values()))
    PostalCode = st.number_input('Postal Code', format="%.0f")
    RoomCount = st.number_input('Room Count', format="%.0f")
    ShowerCount = st.number_input('Shower Count', format="%.0f")
    StateOfBuilding = st.selectbox('State of Building', list(stateofbuilding_options.values()))
    SubtypeOfProperty = st.selectbox('Subtype of Property', list(subtypeofproperty_options.values()))

SurfaceOfPlot = st.number_input('Surface of Plot', format="%.0f")
SwimmingPool = st.checkbox('Swimming Pool')
Terrace = st.checkbox('Terrace')
ToiletCount = st.number_input('Toilet Count', format="%.0f")

house = st.checkbox('House')
apartment = st.checkbox('Apartment')

if house and apartment:
    st.error("Please select either 'House' or 'Apartment', not both.")
    TypeOfProperty = None
elif house:
    TypeOfProperty = 1
elif apartment:
    TypeOfProperty = 2
else:
    st.error("Please select one of 'House' or 'Apartment'.")
    TypeOfProperty = None

TypeOfSale = st.selectbox('Type of Sale', list(typeofsale_options.values()))

model = joblib.load("xgboost_model.pkl")
feature_names = joblib.load("feature_names.pkl")

if st.button("Predict Price") and TypeOfProperty is not None:
    payload = {
        "BathroomCount": BathroomCount,
        "BedroomCount": BedroomCount,
        "ConstructionYear": ConstructionYear,
        "Fireplace": 1 if Fireplace else 0,
        "FloodingZone": [key for key, value in floodingzone_options.items() if value == FloodingZone][0],
        "Furnished": 1 if Furnished else 0,
        "Garden": 1 if Garden else 0,
        "GardenArea": GardenArea,
        "Kitchen": [key for key, value in kitchen_options.items() if value == Kitchen][0],
        "LivingArea": LivingArea,
        "MonthlyCharges": MonthlyCharges,
        "NumberOfFacades": NumberOfFacades,
        "PEB": [key for key, value in peb_options.items() if value == PEB][0],
        "PostalCode": PostalCode,
        "RoomCount": RoomCount,
        "ShowerCount": ShowerCount,
        "StateOfBuilding": [key for key, value in stateofbuilding_options.items() if value == StateOfBuilding][0],
        "SubtypeOfProperty": [key for key, value in subtypeofproperty_options.items() if value == SubtypeOfProperty][0],
        "SurfaceOfPlot": SurfaceOfPlot,
        "SwimmingPool": 1 if SwimmingPool else 0,
        "Terrace": 1 if Terrace else 0,
        "ToiletCount": ToiletCount,
        "TypeOfProperty": TypeOfProperty,
        "TypeOfSale": [key for key, value in typeofsale_options.items() if value == TypeOfSale][0]
    }

    st.write("Payload being used for prediction:", payload)

    input_df = pd.DataFrame([payload])

    input_df = input_df[feature_names]

    prediction = model.predict(input_df)
    predicted_price = prediction[0]

    st.success(f"Predicted Price: {predicted_price}")