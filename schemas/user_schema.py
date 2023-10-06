from pydantic import BaseModel


class Register(BaseModel):
    id_user: int | None = None
    first_name: str
    last_name: str
    phone_number: str
    username: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class UserData(BaseModel):
    id_user_data: int | None = None
    id_user: int | None = None
    height: float
    weight: float
    birth_date: str
    blood_type: str
    status_: bool | None = None


class UserContact(BaseModel):
    id_user_contact: int | None = None
    id_user: int | None = None
    name: str
    relationship: str
    phone_number: str


class Reminder(BaseModel):
    id_reminder: int | None = None
    id_user: int | None = None
    date_: str
    time_: str
    reminder_text: str
    status_: bool | None = None


class Address(BaseModel):
    id_user_address: int | None = None
    id_user: int | None = None
    address: str


class Appointment(BaseModel):
    id_appointment: int | None = None
    id_user: int | None = None
    appointment_date: str
    appointment_place: str
    clinic_name: str
    status_: bool | None = None


class InfoAppointment(BaseModel):
    id_info_appointment: int | None = None
    id_appointment: int | None = None
    blood_pressure: str
    temperature: str
    heart_rate: str
    weight: str
    next_appointment_date: str
    observation: str


class Drug(BaseModel):
    id_drug: int | None = None
    id_user: int | None = None
    drug_name: str


class Allergy(BaseModel):
    id_allergy: int | None = None
    id_user: int | None = None
    allergy_name: str


class ChronicDiseases(BaseModel):
    id_chronic_disease: int | None = None
    id_user: int | None = None
    disease_name: str


# class UserDrug(BaseModel):
#     id_user_drug: int | None = None
#     id_user: int | None = None
#     id_drug: int | None = None
#     status_: bool | None = None


# class UserAllergy(BaseModel):
#     id_user_allergy: int | None = None
#     id_user: int | None = None
#     id_allegry: int | None = None
#     status_: bool | None = None


# class UserChronicDisease(BaseModel):
#     id_user_chronic_disease: int | None = None
#     id_user: int | None = None
#     id_chronic_disease: int | None = None
#     status_: int | None = None
