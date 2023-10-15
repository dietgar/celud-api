from pydantic import BaseModel


class Register(BaseModel):
    id_user: int | None = None
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class Medicaments(BaseModel):
    id_medicament: int | None = None
    id_user: int | None = None
    name: str
    description: str | None = None


class UserMedicament(BaseModel):
    id_user_medicament: int | None = None
    id_medicament: int | None = None
    id_user: int | None = None
    cantity: str
    frecuency: str
    duration: str


class ReminderMedicament(BaseModel):
    id_reminder_medicament: int | None = None
    id_medicament: int | None = None
    id_user: int | None = None
    text: str
    date_: str
    time_: str


class Measurements(BaseModel):
    id_measurements: int | None = None
    id_user: int | None = None
    weight: float
    glycemia: str
    blood_presure: str
    date_: str | None = None


class Appointment(BaseModel):
    id_appointment: int | None = None
    id_user: int | None = None
    date_: str
    time_: str
    place: str
    doctor: str


class ReminderAppointment(BaseModel):
    id_reminder: int | None = None
    id_appointment: int | None = None
    id_user: int | None = None
    text: str
    date_: str
    time_: str

# class UserData(BaseModel):
#     id_user_data: int | None = None
#     id_user: int | None = None
#     height: float
#     weight: float
#     birth_date: str
#     blood_type: str
#     status_: bool | None = None


# class UserContact(BaseModel):
#     id_user_contact: int | None = None
#     id_user: int | None = None
#     name: str
#     relationship: str
#     phone_number: str


# class Reminder(BaseModel):
#     id_reminder: int | None = None
#     id_user: int | None = None
#     date_: str
#     time_: str
#     reminder_text: str
#     status_: bool | None = None


# class Address(BaseModel):
#     id_user_address: int | None = None
#     id_user: int | None = None
#     address: str


# class Appointment(BaseModel):
#     id_appointment: int | None = None
#     id_user: int | None = None
#     appointment_date: str
#     appointment_place: str
#     clinic_name: str
#     status_: bool | None = None


# class InfoAppointment(BaseModel):
#     id_info_appointment: int | None = None
#     id_appointment: int | None = None
#     blood_pressure: str
#     temperature: str
#     heart_rate: str
#     weight: str
#     next_appointment_date: str
#     observation: str


# class Drug(BaseModel):
#     id_drug: int | None = None
#     id_user: int | None = None
#     drug_name: str


# class Allergy(BaseModel):
#     id_allergy: int | None = None
#     id_user: int | None = None
#     allergy_name: str


# class ChronicDiseases(BaseModel):
#     id_chronic_disease: int | None = None
#     id_user: int | None = None
#     disease_name: str
