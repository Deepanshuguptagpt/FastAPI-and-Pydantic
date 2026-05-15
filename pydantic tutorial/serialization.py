from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Patient(BaseModel):   
    name: str
    age: int
    gender : str
    address: Address

address_dict = {'street':'123 Main St','city':'New York','state':'NY','zip_code':'10001'}
address = Address(**address_dict)

patient_info = {'name':'Deepak','age':30,'gender':'male','address':address}
patient = Patient(**patient_info)

print(patient)
print(patient.address.city)

temp = patient.model_dump()
print(temp)
print(type(temp))