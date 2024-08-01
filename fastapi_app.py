from fastapi import FastAPI, HTTPException
import pickle
import numpy as np
from pydantic import BaseModel
import xgboost as xgb
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

model = xgb.Booster()
model.load_model('xgboost_model.json')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

class HouseFeatures(BaseModel):
    BathroomCount: float
    BedroomCount: int
    ConstructionYear: float
    Fireplace: float
    FloodingZone: str
    Furnished: float
    Garden: float
    GardenArea: float
    Kitchen: str
    LivingArea: float
    MonthlyCharges: float
    NumberOfFacades: float
    PEB: str
    PostalCode: int
    RoomCount: float
    ShowerCount: float
    StateOfBuilding: str
    SubtypeOfProperty: str
    SurfaceOfPlot: float
    SwimmingPool: float
    Terrace: float
    ToiletCount: float
    TypeOfProperty: int
    TypeOfSale: str

app = FastAPI()

@app.post("/predict")
def predict(features: HouseFeatures):
    try:
        # Log received data
        logging.info(f"Received data: {features}")

        # Prepare the feature array for prediction
        features_array = np.array([[
            features.BathroomCount, features.BedroomCount, features.ConstructionYear,
            features.Fireplace, features.FloodingZone, features.Furnished,
            features.Garden, features.GardenArea, features.Kitchen, features.LivingArea,
            features.MonthlyCharges, features.NumberOfFacades, features.PEB, features.PostalCode,
            features.RoomCount, features.ShowerCount, features.StateOfBuilding,
            features.SubtypeOfProperty, features.SurfaceOfPlot, features.SwimmingPool,
            features.Terrace, features.ToiletCount, features.TypeOfProperty,
            features.TypeOfSale
        ]])

        # Log the feature array before scaling
        logging.info(f"Feature array before scaling: {features_array}")

        # Scale the features
        features_scaled = scaler.transform(features_array)

        # Log the feature array after scaling
        logging.info(f"Feature array after scaling: {features_scaled}")

        # Make prediction
        prediction = model.predict(features_scaled)

        # Log the prediction result
        logging.info(f"Prediction result: {prediction}")

        return {"predicted_price": prediction[0]}
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
