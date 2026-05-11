from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator, computed_field
from typing import List, Dict, Optional, Annotated 


class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    height: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # ---------------- COMPUTED FIELD ----------------
    # computed_field is used to create a field
    # that is NOT provided by the user
    # but is DERIVED from existing fields
    #
    # This value:
    # ✔ is calculated automatically
    # ✔ behaves like a normal model field
    # ✔ is included in model output (dict / json)
    #
    # @property is required so we can access it like:
    # patient.bmi (not patient.bmi())
    @computed_field
    @property
    def bmi(self) -> float:
        # BMI formula = weight / (height^2)
        # round() is used to simplify the value
        bmi = round(self.weight / (self.height ** 2))
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('inserted')

    # Accessing computed field like a normal attribute
    print('BMI', patient.bmi)


patient_info = {
    'name': 'arjun',
    'email': 'avb@hdfc.com',
    'age': '20',
    'weight': '70',
    'height': 1.72,
    'married': 'False',
    'allergies': ['dust', 'gays'],
    'contact_details': {
        'phone': '2354678',
        'emergency': '8838828282'
    }
}

# computed_field is NOT passed here
# it is calculated internally
patient1 = Patient(**patient_info)

insert_patient_data(patient1)
