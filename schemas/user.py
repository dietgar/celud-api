from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    height: float
    weight: float


class Login(BaseModel):
    user_name: str
    user_mail: str
    password: str


class MedicalInfo(BaseModel):
    allergy: str
    chronic_disease: str
    active_drugs: str


class Adress(BaseModel):
    adress: str


class Appointments(BaseModel):
    date: str
    place: str
    clinic_name: str
