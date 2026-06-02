
from __future__ import annotations
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal
import pickle
import pandas as pd

#Import the ML model
with open('model.pkl','rb') as f:
    model = pickle.load(f)

app = FastAPI()

#Building a pydantic model to validate data
class UserInput(BaseModel):
    age: int = Field(..., gt=0, lt=120)
    weight: float = Field(..., gt=0, description="Weight in kg")
    height: float = Field(..., gt=0, description="Height in meters")
    income_lpa: float = Field(..., gt=0, description="Income in lakhs per annum")
    smoker: bool = Field(..., description="Whether the person is a smoker or not")
    city: str = Field(..., description="City of residence")
    occupation:Literal['retired', 'Free-lancer', 'student', 'Government Job','Business_owner',"Unemployed","Private_job"]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def Lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def occupation_risk(self) -> str:
        if self.occupation in ['retired', 'Unemployed']:
            return "High"
        elif self.occupation in ['Free-lancer', 'student']:
            return "Medium"
        else:
            return "Low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 30:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in ['Mumbai', 'Delhi', 'Bangalore']:
            return 1
        elif self.city in ['Pune', 'Chennai', 'Hyderabad']:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: UserInput):
    input_df = pd.DataFrame(
        [{'bmi': data.bmi,
          'age_group': data.age_group,
          'lifestyle_risk': data.Lifestyle_risk,
          'city_tier' : data.city_tier,
          'income_lpa' : data.income_lpa,
          'occupation' : data.occupation.lower().replace('-', '').replace(' ', '_')
         }]
    )

    prediction = str(model.predict(input_df)[0])

    return JSONResponse(status_code = 200, content = {'predicted_category' : prediction})