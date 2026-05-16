import json
from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,EmailStr,AnyUrl,Field,computed_field
from typing import List,Dict, Optional,Annotated,Literal

class Patient(BaseModel):
    id: str =Annotated[str,Field(..., description="The unique identifier for the patient", example="P001")]
    name: str= Annotated[str,Field(..., description="The name of the patient", example="John Doe")]
    age: int = Annotated[int,Field(..., description="The age of the patient", example=30)]
    gender: str = Annotated[Literal['male','female','other'],Field(..., description="The gender of the patient  (male, female, other)", example="male")]
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    height: int = Annotated[int,Field(...,gt=0, description="The height of the patient in centimeters", example=175)]
    weight: int = Annotated[int,Field(...,gt=0, description="The weight of the patient in kilograms", example=70)]
    
    @computed_field
    @property
    def bmi(self)->float:
            bmi = self.weight / (self.height ** 2)
            return round(bmi, 2)
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 25:
            return "Normal weight"
        elif 25 <= self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class patientUpdate(BaseModel):
    name: Optional[str] = Annotated[Optional[str],Field(None, description="The name of the patient", example="John Doe")]
    age: Optional[int] = Annotated[Optional[int],Field(None, description="The age of the patient", example=30)]
    gender: Optional[str] = Annotated[Optional[str],Field(None, description="The gender of the patient", example="male")]
    diagnosis: Optional[str] = Annotated[Optional[str],Field(None, description="The diagnosis of the patient", example="Hypertension")]
    treatment: Optional[str] = Annotated[Optional[str],Field(None, description="The treatment of the patient", example="Medication")]
    height: Optional[int] = Annotated[Optional[int],Field(None,gt=0, description="The height of the patient in centimeters", example=175)]
    weight: Optional[int] = Annotated[Optional[int],Field(None,gt=0, description="The weight of the patient in kilograms", example=70)]







app = FastAPI()

def insert_patient_data(patient:Patient):
    print(patient.name,patient.age)

patient_info = {'id':'P001','name':'Deepak','age':30,'gender':'male','diagnosis':'Hypertension','treatment':'Medication','height':175,'weight':70}
patient1 = Patient(**patient_info)
insert_patient_data(patient1)

def load_data():
    with open('patient.json', 'r') as file:
        data = json.load(file)
    return data

def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f)


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

@app.post('/create')
def create_patient(patient:Patient):
    data = load_data()

    # Check if patient with the same ID already exists    
    if patient.id in data:
        raise HTTPException(status_code = 400, detail = "Patient with this ID already exists")
    
    #Add new Patient to data
    data[patient.id] = patient.model_dump(exclude=['id'])


    #save into the json file
    save_data(data)

    return JSONResponse(content={"message": "Patient created successfully", "patient_id": patient.id}, status_code=201)
    
@app.put("/update/{patient_id}")
def update_patient(patient_id:str, patient_update:patientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code = 404, detail = "Patient not found")
    
    existing_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value 

        #existing_patient_info -> Pydantic_object -> Updated BMI + Verdict
        existing_patient_info['id'] = patient_id
        patient_pydantic_object = Patient(**existing_patient_info)

        #pydantic object -> Dict
        existing_patient_info = patient_pydantic_object.model_dump(exclude=['id'])
        save_data(data)

        return JSONResponse(status_code= 200, content={'message':'Patient Updated Successfully'})
    
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):
    #load_data
    data = load_data()

    if patient_id not in data:
        raise HTTPException('patient not found')

    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=201, content = 'Patient deleted successfully')