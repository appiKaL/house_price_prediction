from fastapi import FastAPI
import pickle
import numpy as np
from pydantic import BaseModel
import xgboost as xgb

model = xgb.Booster()
model.load_model('xgboost_model.json')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

class HouseFeatures(BaseModel):
    feature1: float
    feature2: float
    feature3: float
    
app = FastAPI()

@app.post("/predict")
def predict(features: HouseFeatures):
    
    features_array = np.array([[features.feature1, features.feature2, features.feature3]])
    
    features_scaled = scaler.transform(features_array)
    
    prediction = model.predict(features_scaled)
    
    return {"predicted_price": prediction[0]}