from fastapi import APIRouter
from config.db import engine
from models.user import *
from schemas.user_schema import *
from starlette.status import *
from werkzeug.security import generate_password_hash, check_password_hash
from validations.user_data import *
from fastapi import Body
from datetime import date
# from typing import List

root = APIRouter()


@root.post("/users/register")
async def register(data: Register = Body(..., embed=True)):
    with engine.connect() as conn:
        # try:
        if exist_username(data.username):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "Este nombre de usuario ya está en uso"
            }
        if exist_email(data.email):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "Este correo electrónico ya pertenece a otra cuenta"
            }
        if not validate_string(data.first_name):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "Nombres no pueden contener números o simbolos"
            }
        if not validate_string(data.last_name):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "Nombres no pueden contener números o simbolos"
            }
        if not validate_username(data.username):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "Nombres de usuario solo pueden contener letras y números"
            }
        if not validate_email(data.email):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "Correo electrónico en el formato incorrecto"
            }
        if not validate_secure_password(data.password):
            return {
                "status": HTTP_400_BAD_REQUEST,
                "message": "La contraseña debe tener 8 caracteres como mínimo, una mayúscula, una minúscula, un número y un carácter especial"
            }
        new_user = dict(data)
        new_user["first_name"] = format_string(data.first_name)
        new_user["last_name"] = format_string(data.last_name)
        new_user["password"] = generate_password_hash(
            data.password, "pbkdf2:sha256:30", 30)
        result = conn.execute(user.insert().values(new_user))
        return conn.execute(user.select().where(user.c.id_user == result.lastrowid)).first()
        # except:
        #     return {
        #         "status": HTTP_500_INTERNAL_SERVER_ERROR,
        #         "message": "Ha ocurrido un error inesperado"
        #     }

# * Ruta para hacer login


@root.post("/users/login")
async def login(user_login: Login = Body(..., embed=True)):
    with engine.connect() as conn:
        # try:
        if validate_email(user_login.email):
            result = conn.execute(user.select().where(
                user.c.email == user_login.email)).first()

            if result != None:
                # print(dict(result))
                check_password = check_password_hash(
                    result[5], user_login.password)

                if check_password:
                    return {
                        "status": HTTP_202_ACCEPTED,
                        "message": "Ha iniciado sesión correctamente"
                    }
                return {
                    "status": HTTP_400_BAD_REQUEST,
                    "message": "Contraseña incorrecta"
                }
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Correo no asignado a ninguna cuenta"
            }
        return {
            "status": HTTP_400_BAD_REQUEST,
            "message": "Ingrese un correo electrónico válido"
        }
        # except:
        #     return {
        #         "status": HTTP_500_INTERNAL_SERVER_ERROR,
        #         "message": "Ha ocurrido un error inesperado"
        #     }


@root.post("/user/medicaments/{user_id}")
async def add_medicament(user_id: int, data: Medicaments = Body(..., embed=True), medicament_data: UserMedicament = Body(..., embed=True)):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.id_user == user_id)).first()
        if result != None:
            if not len(data.name) > 0 and len(data.name) < 50:
                return {
                    "detail": "El nombre no puede superar los 50 caracteres"
                }
            if not len(data.description) >= 0 and len(data.description) < 150:
                return {
                    "detail": "La descripcion no puede superar los 150 caracteres"
                }
            new_medicament = dict(data)
            new_medicament["id_user"] = result[0]
            last_row_id = conn.execute(
                medicaments.insert().values(new_medicament))
            data_medicament = dict(medicament_data)
            data_medicament["id_medicament"] = last_row_id.lastrowid
            data_medicament["id_user"] = result[0]
            return HTTP_201_CREATED, conn.execute(medicaments.select().where(medicaments.c.id_medicament == last_row_id.lastrowid)).first()
        return {
            "detail": "Este usuario no existe"
        }


@root.post("/user/reminder-medicament/{user_id}/{medicament_id}")
async def create_reminder_medicament(user_id: int, medicament_id: int, data: ReminderMedicament = Body(..., embed=True)):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.id_user == user_id)).first()
        medicament_id = conn.execute(medicaments.select().where(
            medicaments.c.id_medicament == medicament_id)).first()
        if not result != None:
            return {
                "detail": "Este usuario no existe"
            }
        if not medicament_id != None:
            return {
                "detail": "Este medicamento no existe"
            }
        if not len(data.text) > 0 and len(data.text) < 150:
            return {
                "detail": "El texto supera los 150 caracteres"
            }
        if not validate_date(data.date_):
            return {
                "detail": "Formato de fecha incorrecto"
            }
        try:
            if not validate_time(data.time_):
                return {
                    "detail": "Formato de hora incorrecto"
                }
        except:
            return {
                "detail": "Ingrese una hora correcta"
            }
        new_reminder = dict(data)
        new_reminder["id_medicament"] = medicament_id[0]
        new_reminder["id_user"] = result[0]
        try:
            new_reminder["date_"] = format_date(data.date_)
        except:
            return {
                "detail": "Fecha fuera de rango"
            }
        last_row_id = conn.execute(
            reminder_medicament.insert().values(new_reminder))
        return conn.execute(reminder_medicament.select().where(reminder_medicament.c.id_reminder_medicament == last_row_id.lastrowid)).first()


@root.post("/users/measurements/{user_id}")
async def add_measurement(user_id: int, data: Measurements = Body(..., embed=True)):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.id_user == user_id)).first()
        if result != None:
            if not len(data.glycemia) > 0 and len(data.glycemia) < 10:
                return {
                    "detail": "Se ha pasado el límite de caracteres"
                }
            if not validate_blood_pressure(data.blood_presure):
                return {
                    "detail": "Presión sanguínea en el formato incorrecto"
                }
            new_measurement = dict(data)
            new_measurement["id_user"] = result[0]
            new_measurement["date_"] = date.today()
            last_row_id = conn.execute(
                measurements.insert().values(new_measurement))
            return conn.execute(measurements.select().where(measurements.c.id_measurements == last_row_id.lastrowid)).first()
        return {
            "detail": "Este usuario no existe"
        }


@root.post("/users/appointment/{user_id}")
async def create_appointment(user_id: int, data: Appointment = Body(..., embed=True)):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.id_user == user_id)).first()
        if result != None:
            if not validate_date(data.date_):
                return {
                    "detail": "Ingrese una fecha correcta"
                }
            if not validate_time(data.time_):
                return {
                    "detail": "Ingrese una hora correcta"
                }
            try:
                if not len(data.place) > 0 and len(data.place) < 50:
                    return {
                        "detail": "El texto no puede superar los 50 carácteres"
                    }
            except:
                return {
                    "detail": "Debe introducir el lugar de la cita"
                }
            if not validate_string(data.doctor):
                return {
                    "detail": "Nombres no pueden contener números o símbolos"
                }
            new_appointment = dict(data)
            new_appointment["id_user"] = result[0]
            try:
                new_appointment["date_"] = format_date(data.date_)
            except:
                return {
                    "detail": "Fecha fuera de rango"
                }
            last_row_id = conn.execute(
                appointment.insert().values(new_appointment))
            return conn.execute(appointment.select().where(appointment.c.id_appointment == last_row_id.lastrowid)).first()
        return {
            "detail": "Este usuario no existe"
        }


@root.post("/users/reminder-appointment/{user_id}/{appointment_id}")
async def create_appointment_reminder(user_id: int, appointment_id: int, data: ReminderAppointment = Body(..., embed=True)):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.id_user == user_id)).first()
        appointment_id = conn.execute(appointment.select().where(
            appointment.c.id_appointment == appointment_id)).first()
        if not result != None:
            return {
                "detail": "Este usuario no existe"
            }
        if not appointment_id != None:
            return {
                "detail": "Esta cita no existe"
            }
        if not validate_date(data.date_):
            return {
                "detail": "Formato de fecha incorrecto"
            }
        try:
            if not validate_time(data.time_):
                return {
                    "detail": "Formato de hora incorrecto"
                }
        except:
            return {
                "La hora introducida no es correcta"
            }
        new_reminder = dict(data)
        new_reminder["id_appointment"] = appointment_id[0]
        new_reminder["id_user"] = result[0]
        try:
            new_reminder["date_"] = format_date(data.date_)
        except:
            return {
                "detail": "Fecha fuera de rango"
            }
        last_row_id = conn.execute(
            reminder_appointment.insert().values(new_reminder))
        return conn.execute(reminder_appointment.select().where(reminder_appointment.c.id_reminder == last_row_id.lastrowid)).first()

# * Ruta para obtener todos los usuarios


@root.get("/users")
async def get_users():
    with engine.connect() as conn:
        try:
            result = conn.execute(user.select()).fetchall()
            return result
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error inesperado"
            }

# * Ruta para obtener un usuario mediante su ID


@root.get("/user/{user_id}")
async def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.id_user == user_id)).first()
        if result != None:
            return result
        return {
            "detail": "Este usuario no existe"
        }

# * Ruta para obtener todas las mediciones de un usuario


@root.get("/measurements/{user_id}")
async def get_measurements(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(measurements.select().where(
            measurements.c.id_user == user_id)).fetchall()
        if result != None:
            return result
        return {
            "detail": "Este usuario no existe"
        }

# @root.post("/users/personal-data/{user_id}")
# def additional_user_info(user_id: int, data_user: UserData):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(user.select().where(
#                 user.c.id_user == user_id)).first()

#             if exist_id != None:
#                 if validate_date(data_user.birth_date):
#                     new_data = dict(data_user)
#                     new_data["id_user"] = exist_id[0]
#                     try:
#                         new_data["birth_date"] = format_date(
#                             data_user.birth_date)
#                     except:
#                         return {
#                             "status": HTTP_422_UNPROCESSABLE_ENTITY,
#                             "message": "Ingrese una fecha valida"
#                         }
#                     new_data["status_"] = True
#                     result = conn.execute(user_data.insert().values(new_data))
#                     return conn.execute(user_data.select().where(user_data.c.id_user_data == result.lastrowid)).first()
#                 return {
#                     "status": HTTP_422_UNPROCESSABLE_ENTITY,
#                     "message": "Formato de fecha no valido"
#                 }
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Este usuario no existe"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error inesperado"
#             }

# # * Ruta para crear un contacto de emergencia


# @root.post("/users/user-contact/{user_id}")
# def create_user_contact(user_id: int, data: UserContact):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(
#                 user.select().where(user.c.id_user == user_id)).first()

#             if exist_id != None:
#                 if not validate_string(data.name):
#                     return {
#                         "detail": "Ingrese un nombre correcto"
#                     }
#                 if not validate_string(data.relationship):
#                     return {
#                         "detail": "Ingrese un parentesco valido"
#                     }
#                 if not validate_phone_number(data.phone_number):
#                     return {
#                         "detail": "Ingrese un número telefónico válido"
#                     }
#                 new_contact = dict(data)
#                 new_contact["id_user"] = exist_id[0]
#                 new_contact["name"] = format_string(data.name)
#                 new_contact["relationship"] = format_string(
#                     data.relationship)
#                 result = conn.execute(
#                     user_contact.insert().values(new_contact))
#                 return conn.execute(user_contact.select().where(user_contact.c.id_user_contact == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Este usuario no existe"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para agregar un recordatorio


# @root.post("/users/reminder/{user_id}")
# def create_reminder(user_id: int, data: Reminder):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(
#                 user.select().where(user.c.id_user == user_id)).first()

#             if exist_id != None:

#                 if not validate_date(data.date_):
#                     return {
#                         "detail": "Formato de fecha DD-MM-YYYY"
#                     }
#                 try:
#                     validate_time(data.time_)
#                 except:
#                     return {
#                         "detail": "Ingrese una hora valida"
#                     }
#                 new_reminder = dict(data)
#                 new_reminder["id_user"] = exist_id[0]
#                 try:
#                     new_reminder["date_"] = format_date(data.date_)
#                 except:
#                     return {
#                         "detail": "Fecha fuera de rango"
#                     }
#                 new_reminder["status_"] = True
#                 result = conn.execute(reminder.insert().values(new_reminder))
#                 return conn.execute(reminder.select().where(reminder.c.id_reminder == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Este usuario no existe"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para agregar la dirección de un usuario


# @root.post("/users/address/{user_id}")
# def add_address(user_id: int, data: Address):
#     with engine.connect() as conn:
#         try:

#             exist_id = conn.execute(user.select().where(
#                 user.c.id_user == user_id)).first()

#             if exist_id != None:

#                 new_address = dict(data)
#                 new_address["id_user"] = exist_id[0]
#                 result = conn.execute(
#                     user_address.insert().values(new_address))
#                 return conn.execute(user_address.select().where(user_address.c.id_user_address == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Usuario no encontrado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para agregar una cita


# @root.post("/users/appointment/{user_id}")
# def create_appointment(user_id: int, data: Appointment):
#     with engine.connect() as conn:
#         try:

#             exist_id = conn.execute(user.select().where(
#                 user.c.id_user == user_id)).first()

#             if exist_id != None:

#                 if not validate_date(data.appointment_date):
#                     return {
#                         "detail": "Ingrese una fecha valida"
#                     }

#                 new_appointment = dict(data)
#                 new_appointment["id_user"] = exist_id[0]
#                 try:
#                     new_appointment["appointment_date"] = format_date(
#                         data.appointment_date)
#                 except:
#                     return {
#                         "detail": "Esta fecha no es correcta"
#                     }
#                 new_appointment["status_"] = True
#                 result = conn.execute(
#                     appointment.insert().values(new_appointment))
#                 return conn.execute(appointment.select().where(appointment.c.id_appointment == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Usuario no encontrado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para agregar información de una cita


# @root.post("/users/info-appointments/{user_id}")
# def create_info_appointment(appointment_id: int, data: InfoAppointment):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(appointment.select().where(
#                 appointment.c.id_appointment == appointment_id)).first()

#             if exist_id != None:

#                 if not validate_blood_pressure(data.blood_pressure):
#                     return {
#                         "detail": "Formato incorrecto para presión sanguínea"
#                     }
#                 if not validate_date(data.next_appointment_date):
#                     return {
#                         "detail": "Ingrese una fecha válida"
#                     }
#                 new_info = dict(data)
#                 new_info["id_appointment"] = exist_id[0]
#                 try:
#                     new_info["next_appointment_date"] = format_date(
#                         data.next_appointment_date)
#                 except:
#                     return {
#                         "detail": "Esta fecha no es correcta"
#                     }
#                 result = conn.execute(
#                     info_appointment.insert().values(new_info))
#                 return conn.execute(info_appointment.select().where(info_appointment.c.id_info_appointment == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Cita no encontrada"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para agregar un medicamento


# @root.post("/users/drug/{user_id}")
# def add_drug(user_id: int, data: Drug):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(
#                 user.select().where(user.c.id_user == user_id)).first()

#             if exist_id != None:
#                 new_drug = dict(data)
#                 new_drug["id_user"] = exist_id[0]
#                 result = conn.execute(drug.insert().values(new_drug))

#                 conn.execute(user_drug.insert().values(
#                     id_user=exist_id[0], id_drug=result.lastrowid, status_=True))

#                 return conn.execute(drug.select().where(drug.c.id_drug == result.lastrowid)).first()

#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Usuario no encontrado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para agregar una alergia


# @root.post("/users/allergy/{user_id}")
# def add_allergy(user_id: int, data: Allergy):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(
#                 user.select().where(user.c.id_user == user_id)).first()

#             if exist_id != None:
#                 new_allergy = dict(data)
#                 new_allergy["id_user"] = exist_id[0]
#                 result = conn.execute(allergy.insert().values(new_allergy))

#                 conn.execute(user_allergy.insert().values(
#                     id_user=exist_id[0], id_allergy=result.lastrowid, status_=True))

#                 return conn.execute(allergy.select().where(allergy.c.id_allergy == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Usuario no encontrado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "detail": "Ha ocurrido un error"
#             }

# # * Ruta para agregar una enfermedad crónica


# @root.post("/users/chronic-disease/{user_id}")
# def add_chronic_disease(user_id: int, data: ChronicDiseases):
#     with engine.connect() as conn:
#         try:
#             exist_id = conn.execute(user.select().where(
#                 user.c.id_user == user_id)).first()

#             if exist_id != None:
#                 new_chronic_disease = dict(data)
#                 new_chronic_disease["id_user"] = exist_id[0]
#                 result = conn.execute(
#                     chronic_diseases.insert().values(new_chronic_disease))

#                 conn.execute(user_chronic_diseases.insert().values(
#                     id_user=exist_id[0], id_chronic_disease=result.lastrowid, status_=True))

#                 return conn.execute(chronic_diseases.select().where(chronic_diseases.c.id_chronic_disease == result.lastrowid)).first()
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Usuario no encontrado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver a todos los usuarios


# @root.get("/users")
# def get_users():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user.select()).fetchall()
#             return result
#         except:
#             return {
#                 "detail": "Ha ocurrido un error"
#             }

# # * Ruta para ver un solo usuario


# @root.get("/user/{user_id}")
# def get_user(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user.select().where(
#                 user.c.id_user == user_id)).first()
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "Usuario no encontrado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver la data de todos los usuarios


# @root.get("/all-personal-data")
# def get_all_user_data():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user_data.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver la data de un usuario


# @root.get("/personal-data/{user_id}")
# def get_user_data(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user_data.select().where(
#                 user_data.c.id_user == user_id)).first()
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver todos los contactos de emergencia


# @root.get("/user_contact/")
# def get_all_user_contact():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user_contact.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para los contactos de un usuario


# @root.get("/user_contact/{user_id}")
# def get_user_contact(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user_contact.select().where(
#                 user_contact.c.id_user == user_id)).fetchall()
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver todos los recordatorios


# @root.get("/reminder/")
# def get_reminder():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(reminder.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver los recordatorios de un usuario


# @root.get("/reminder/{user_id}")
# def get_reminder(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(reminder.select().where(
#                 reminder.c.id_user == user_id)).fetchall()
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }


# # * Ruta para ver todas las direcciones

# @root.get("/address/")
# def get_user_address():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user_address.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver la direccion de un usuario


# @root.get("/address/{user_id}")
# def get_user_address(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(user_address.select().where(
#                 user_address.c.id_user == user_id)).first()
#             print(result)
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }


# # * Ruta para ver todas las citas

# @root.get("/appointment/")
# def get_appointment():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(appointment.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver las citas de un usuario


# @root.get("/appointment/{user_id}")
# def get_appointment(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(appointment.select().where(
#                 appointment.c.id_user == user_id)).fetchall()
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver la info de todas las citas


# @root.get("/info-appointments/")
# def get_all_info_appointment():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(info_appointment.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }


# # * Ruta para ver la info de las citas de un usuario

# @root.get("/info-appointments/{appointment_id}")
# def get_info_appointment(appointment_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(info_appointment.select().where(
#                 info_appointment.c.id_appointment == appointment_id)).fetchall()
#             if result != None:
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver todos los medicamentos


# @root.get("/drug/")
# def get_user_drug():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(drug.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver los medicamentos de un usuario


# @root.get("/drug/{user_id}")
# def get_user_drug(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(drug.select().where(
#                 drug.c.id_user == user_id)).fetchall()
#             result_user_drug = conn.execute(user_drug.select().where(
#                 user_drug.c.id_drug == user_id)).fetchall()
#             if result != None:
#                 return result, result_user_drug
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver todas las alergias


# @root.get("/allergy/")
# def get_allergy():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(allergy.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver las alergias de un usuario


# @root.get("/allergy/{user_id}")
# def get_allergy(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(allergy.select().where(
#                 allergy.c.id_user == user_id)).fetchall()
#             result_user_allergy = conn.execute(user_allergy.select().where(
#                 user_allergy.c.id_user == user_id)).fetchall()
#             if result != None:
#                 return result, result_user_allergy
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver todas las enfermedades


# @root.get("/chronic-disease/")
# def get_chronic_disease():
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(chronic_diseases.select()).fetchall()
#             return result
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }

# # * Ruta para ver las enfermedades crónicas de un usuario


# @root.get("/chronic-disease/{user_id}")
# def get_chronic_disease(user_id: int):
#     with engine.connect() as conn:
#         try:
#             result = conn.execute(chronic_diseases.select().where(
#                 chronic_diseases.c.id_user == user_id)).fetchall()
#             result_chronic_diseases = conn.execute(user_chronic_diseases.select().where(
#                 user_chronic_diseases.c.id_user == user_id)).fetchall()
#             if result != None:
#                 return result, result_chronic_diseases
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "No hay datos relacionados con el ID proporcionado"
#             }
#         except:
#             return {
#                 "status": HTTP_500_INTERNAL_SERVER_ERROR,
#                 "message": "Ha ocurrido un error"
#             }


# # Ruta que permite actualizar un usuario a traves de su ID
# @user.put("/api/users/{user_id}")
# def update_user(data_update: UserSchema, user_id: int):
#     with engine.connect() as conn:
#         exist_id = conn.execute(users.select().where(
#             users.c.id == user_id)).first()
#         if check_email(data_update.user_mail):
#             if exist_id != None:
#                 encrypt_password = generate_password_hash(
#                     data_update.user_password, "pbkdf2:sha256:30", 30)
#                 conn.execute(users.update().values(user_name=data_update.user_name, user_mail=data_update.user_mail,
#                                                    user_password=encrypt_password).where(users.c.id == user_id))
#                 # conn.commit()
#                 result = conn.execute(users.select().where(
#                     users.c.id == user_id)).first()
#                 return result
#             return {
#                 "status": HTTP_404_NOT_FOUND,
#                 "message": "User doesn't exist"
#             }
#         return {
#             "status": HTTP_400_BAD_REQUEST,
#             "message": "Email addres is not valid"
#         }


# # Ruta que permite eliminar usuarios por ID
# @user.delete("/api/users/{user_id}", status_code=HTTP_200_OK)
# def delete_user(user_id: int):
#     with engine.connect() as conn:
#         result = conn.execute(users.select().where(
#             users.c.id == user_id)).first()
#         if result != None:
#             conn.execute(users.delete().where(users.c.id == user_id))
#             return {
#                 "detail": "Sucessful deleted"
#             }
#         return {
#             "status": HTTP_404_NOT_FOUND,
#             "message": "User doesn't exist"
#         }
