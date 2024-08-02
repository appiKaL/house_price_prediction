from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel
import xgboost as xgb
import logging
import joblib
from sklearn.preprocessing import RobustScaler
import pandas as pd

scaler = joblib.load("scaler.pkl")
encoders = joblib.load("encoders.pkl")
feature_names = joblib.load("feature_names.pkl")

if not isinstance(scaler, RobustScaler):
    raise ValueError("Loaded scaler is not a RobustScaler instance")

def transform_data(data):
    return scaler.transform(data)

logging.basicConfig(level=logging.INFO)

model = xgb.Booster()
model.load_model('xgboost_model.json')

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
        logging.info(f"Received data: {features}")

        features_dict = features.dict()
        for column, categories in encoders.items():
            if column in features_dict:
                features_dict[column] = categories.get_loc(features_dict[column])

        features_array = np.array([[
            features_dict['BathroomCount'], features_dict['BedroomCount'], features_dict['ConstructionYear'],
            features_dict['Fireplace'], features_dict['FloodingZone'], features_dict['Furnished'],
            features_dict['Garden'], features_dict['GardenArea'], features_dict['Kitchen'], features_dict['LivingArea'],
            features_dict['MonthlyCharges'], features_dict['NumberOfFacades'], features_dict['PEB'], features_dict['PostalCode'],
            features_dict['RoomCount'], features_dict['ShowerCount'], features_dict['StateOfBuilding'],
            features_dict['SubtypeOfProperty'], features_dict['SurfaceOfPlot'], features_dict['SwimmingPool'],
            features_dict['Terrace'], features_dict['ToiletCount'], features_dict['TypeOfProperty'],
            features_dict['TypeOfSale']
        ]])

        features_df = pd.DataFrame(features_array, columns=feature_names)

        logging.info(f"Feature array before scaling: {features_df}")

        features_scaled = transform_data(features_df)

        logging.info(f"Feature array after scaling: {features_scaled}")

        dmatrix = xgb.DMatrix(features_scaled)
        prediction = model.predict(dmatrix)

        logging.info(f"Prediction result: {prediction}")

        return {"predicted_price": prediction[0]}
    except Exception as e:
        logging.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")