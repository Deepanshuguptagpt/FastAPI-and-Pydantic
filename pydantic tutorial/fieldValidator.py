from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated 


class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str, str]

    # ---------------- MODEL VALIDATOR ----------------
    # model_validator is used when validation depends on
    # MULTIPLE fields together (not just one field)
    #
    # mode='after' means:
    # 👉 This validation runs AFTER:
    #    1. All fields are validated
    #    2. Type coercion is done
    #
    # 'model' is the complete validated Patient object
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):

        # If patient's age is greater than 60
        # AND emergency contact is missing
        if model.age > 60 and 'emergency' not in model.contact_details:
            # Raise error if condition fails
            raise ValueError(
                'patients older than 60 must have an emergency contact'
            )

        # Must return the model after validation
        return model


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('inserted')


patient_info = {
    'name': 'arjun',
    'email': 'avb@hdfc.com',
    'age': '20',
    'weight': '70',
    'married': 'False',
    'allergies': ['dust', 'gays'],
    'contact_details': {
        'phone': '2354678',
        'emergency': '8838828282'
    }
}

patient1 = Patient(**patient_info)  # full model validation happens here
insert_patient_data(patient1)




'''field_validator → ek single field ke liye hota hai

model_validator → jab rule multiple fields pe depend karta ho

Jaise:
👉 age > 60
👉 AND emergency contact hona chahiye

Isliye model_validator use hota hai
kyunki pura object ek saath check karna hota hai
'''