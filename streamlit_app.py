import streamlit as st
import requests
import json

st.set_page_config(
    page_title="House Price Prediction",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://your-image-url.com/background.jpg");
        background-size: cover;
    }
    .sidebar .sidebar-content {
        background: rgba(255, 255, 255, 0.9);
    }
    .css-18e3th9 {
        font-family: 'Arial', sans-serif;
        color: #333333;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #333333;
        font-family: 'Arial', sans-serif;
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
    BathroomCount = st.number_input('Bathroom Count', format="%.1f")
    BedroomCount = st.number_input('Bedroom Count', format="%.1f")
    ConstructionYear = st.number_input('Construction Year', format="%.0f")
    Fireplace = st.number_input('Fireplace', format="%.1f")
    FloodingZone = st.selectbox('Flooding Zone', list(floodingzone_options.values()))
    Furnished = st.number_input('Furnished', format="%.1f")
    Garden = st.number_input('Garden', format="%.1f")
    GardenArea = st.number_input('Garden Area', format="%.1f")
    Kitchen = st.selectbox('Kitchen', list(kitchen_options.values()))

with col2:
    LivingArea = st.number_input('Living Area', format="%.1f")
    MonthlyCharges = st.number_input('Monthly Charges', format="%.1f")
    NumberOfFacades = st.number_input('Number of Facades', format="%.1f")
    PEB = st.selectbox('PEB', list(peb_options.values()))
    PostalCode = st.number_input('Postal Code', format="%.0f")
    RoomCount = st.number_input('Room Count', format="%.1f")
    ShowerCount = st.number_input('Shower Count', format="%.1f")
    StateOfBuilding = st.selectbox('State of Building', list(stateofbuilding_options.values()))
    SubtypeOfProperty = st.selectbox('Subtype of Property', list(subtypeofproperty_options.values()))

SurfaceOfPlot = st.number_input('Surface of Plot', format="%.1f")
SwimmingPool = st.number_input('Swimming Pool', format="%.1f")
Terrace = st.number_input('Terrace', format="%.1f")
ToiletCount = st.number_input('Toilet Count', format="%.1f")
TypeOfProperty = st.number_input('Type of Property', format="%.0f")
TypeOfSale = st.selectbox('Type of Sale', list(typeofsale_options.values()))

API_URL = "https://house-price-prediction-qd90.onrender.com"

if st.button("Predict Price"):
    payload = {
        "BathroomCount": BathroomCount,
        "BedroomCount": BedroomCount,
        "ConstructionYear": ConstructionYear,
        "Fireplace": Fireplace,
        "FloodingZone": [key for key, value in floodingzone_options.items() if value == FloodingZone][0],
        "Furnished": Furnished,
        "Garden": Garden,
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
        "SwimmingPool": SwimmingPool,
        "Terrace": Terrace,
        "ToiletCount": ToiletCount,
        "TypeOfProperty": TypeOfProperty,
        "TypeOfSale": [key for key, value in typeofsale_options.items() if value == TypeOfSale][0]
    }

    # Debugging: Log the payload being sent
    st.write("Payload being sent to API:", payload)

    try:
        # Send the request to the FastAPI backend
        response = requests.post(API_URL, json=payload)

        # Log the raw response for debugging purposes
        st.write("Raw response:", response.content)

        # Attempt to parse the response as JSON
        response_data = response.json()

        # Log the parsed response
        st.write("Parsed response:", response_data)

        if response.status_code == 200:
            st.success(f"Predicted Price: {response_data['predicted_price']}")
        else:
            st.error(f"API returned an error: {response_data.get('detail', 'Unknown error')}")
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error: {str(e)}")
        st.write("Response content that caused the error:", response.content)
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {str(e)}")
