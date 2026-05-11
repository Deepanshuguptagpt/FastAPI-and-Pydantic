from pydantic import BaseModel,EmailStr,AnyUrl,model_validator
from typing import List,Dict, Optional,Annotated

class Patient(BaseModel):
    name : str
    LinkedIn : Optional[AnyUrl] = None
    email : EmailStr
    age : int 
    height : float 
    allergies : Optional[List[str]] = None
    contact_info : Dict[str, str]

    @model_validator(mode = 'after')
    @classmethod
    def emergency_contact_info(self):
        if 'emergency' not in self.contact_info:
            raise ValueError("Emergency contact info is required")
        return self

def insert_patient_data(patient:Patient):
    print(patient.name,patient.age)
    print(patient.email,patient.LinkedIn)

patient_info = {'name':'Deepak','email':'deepak@hdfc.com','LinkedIn':'https://www.linkedin.com/in/deepak','age':30,'height':5.9,'allergies':['pollen','dust'],'contact_info':{'phone':'123-456-7890','emergency':'987-654-3210'}}

patient1 = Patient(**patient_info)
insert_patient_data(patient1)