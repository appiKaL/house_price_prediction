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
    features_array = np.array([[
        features.bathroomcount, features.bedroomcount, features.constructionyear,
        features.fireplace, features.floodingzone, features.furnished,
        features.garden, features.gardenarea, features.kitchen, features.livingarea,
        features.monthlycharges, features.numberoffacades, features.peb, features.postalcode,
        features.roomcount, features.showercount, features.stateofbuilding,
        features.subtypeofproperty, features.surfaceofplot, features.swimmingpool,
        features.terrace, features.toiletcount, features.typeofproperty,
        features.typeofsale
    ]])
    
    features_scaled = scaler.transform(features_array)
    
    prediction = model.predict(features_scaled)
    
    return {"predicted_price": prediction[0]}
