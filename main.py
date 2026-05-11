import json
from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict, Optional,Annotated

class Patient(BaseModel):
    name : Annotated[str,Field(max_length=50, description="Name must be a string with a maximum length of 50 characters", example="John Doe")]
    email: EmailStr
    LinkedIn : Optional[AnyUrl] = None
    age : int = Field(..., gt=0, description="Age must be a positive integer")
    height : float = Field(..., gt=0, description="Height must be a positive number")
    allergies : Annotated[Optional[List[str]], Field(default=None,max_length = 5, description="Maximum of 5 allergies allowed")]
    contact_info : Dict[str, str]

app = FastAPI()

def insert_patient_data(patient:Patient):
    print(patient.name,patient.age)
    print(patient.email,patient.LinkedIn)

patient_info = {'name':'Deepak','email':'deepak@gmail.com','LinkedIn':'https://www.linkedin.com/in/deepak','age':30,'height':5.9,'allergies':['pollen','dust'],'contact_info':{'phone':'123-456-7890'}}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)

def load_data():
    with open('patient.json', 'r') as file:
        data = json.load(file)
    return data

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is the about page."}

@app.get("/view")
def view():
    data = load_data()
    return {"patients": data}

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", examples='P001')):
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    raise HTTPException(status_code = 404, detail = "patient not found")

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description="The field to sort patients by"),order:str = Query('asc',description="The sort order, either 'asc' or 'desc'")):
    valid_fields = ['age','height']

    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f'Invlaid field, select from {valid_fields}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code = 400, detail = "Invalid order, select 'asc' or 'desc'")
    
    data = load_data()

    sort_order = True if order == 'desc' else False
    sorted_data = sorted(data.values(), key = lambda x : x.get(sort_by,0),reverse =(sort_order))

    return sorted_data 