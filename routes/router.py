from fastapi import APIRouter
from config.db import engine
from models.user import *
from schemas.user_schema import *
from starlette.status import *
from werkzeug.security import generate_password_hash, check_password_hash
from validations.user_data import *
# import uuid
# from typing import List


root = APIRouter()


@root.post("/api/users/register")
def register(data_user: Register):
    with engine.connect() as conn:
        try:
            if exist_phone_number(data_user.phone_number):
                return {
                    "detail": "Este número telefónico ya está en uso"
                }

            if exist_username(data_user.username):
                return {
                    "detail": "Este nombre de usuario ya está en uso"
                }

            if exist_email(data_user.email):
                return {
                    "detail": "Este correo electrónico ya pertenece a otra cuenta"
                }

            if validate_data_user(data_user):
                new_user = dict(data_user)
                new_user["first_name"] = format_string(data_user.first_name)
                new_user["last_name"] = format_string(data_user.last_name)
                new_user["password"] = generate_password_hash(
                    data_user.password, "pbkdf2:sha256:30", 30)
                result = conn.execute(user.insert().values(new_user))
                return conn.execute(user.select().where(user.c.id_user == result.lastrowid)).first()

        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error inesperado"
            }


@root.post("/api/users/login")
def login(user_login: Login):
    with engine.connect() as conn:
        try:
            if validate_email(user_login.email):
                result = conn.execute(user.select().where(
                    user.c.email == user_login.email)).first()

                if result != None:
                    check_password = check_password_hash(
                        result[7], user_login.password)

                    if check_password:
                        return {
                            "status": HTTP_202_ACCEPTED,
                            "detail": "Acceso exitoso!"
                        }
                    return {
                        "status": HTTP_400_BAD_REQUEST,
                        "detail": "Contraseña incorrecta"
                    }
                return {
                    "status": HTTP_404_NOT_FOUND,
                    "detail": "Correo no asignado a ninguna cuenta"
                }
            return {
                "status": HTTP_400_BAD_REQUEST,
                "detail": "Ingrese un correo electrónico válido"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error inesperado"
            }


@root.post("/api/users/personal-data/{user_id}")
def additional_user_info(user_id: int, data_user: UserData):
    with engine.connect() as conn:
        try:
            exist_id = conn.execute(user.select().where(
                user.c.id_user == user_id)).first()

            if exist_id != None:
                if validate_date(data_user.birth_date):
                    new_data = dict(data_user)
                    new_data["id_user"] = exist_id[0]
                    try:
                        new_data["birth_date"] = format_date(
                            data_user.birth_date)
                    except:
                        return {
                            "status": HTTP_422_UNPROCESSABLE_ENTITY,
                            "message": "Ingrese una fecha valida"
                        }
                    new_data["status_"] = True
                    result = conn.execute(user_data.insert().values(new_data))
                    return conn.execute(user_data.select().where(user_data.c.id_user_data == result.lastrowid)).first()
                return {
                    "status": HTTP_422_UNPROCESSABLE_ENTITY,
                    "message": "Formato de fecha no valido"
                }
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Este usuario no existe"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error inesperado"
            }


@root.post("/api/users/user_contact/{user_id}")
def create_user_contact(user_id: int, data: UserContact):
    with engine.connect() as conn:
        try:
            exist_id = conn.execute(
                user.select().where(user.c.id_user == user_id)).first()

            if exist_id != None:
                if not validate_string(data.name):
                    return {
                        "detail": "Ingrese un nombre correcto"
                    }
                if not validate_string(data.relationship):
                    return {
                        "detail": "Ingrese un parentesco valido"
                    }
                if not validate_phone_number(data.phone_number):
                    return {
                        "detail": "Ingrese un número telefónico válido"
                    }
                new_contact = dict(data)
                new_contact["id_user"] = exist_id[0]
                new_contact["name"] = format_string(data.name)
                new_contact["relationship"] = format_string(
                    data.relationship)
                result = conn.execute(
                    user_contact.insert().values(new_contact))
                return conn.execute(user_contact.select().where(user_contact.c.id_user_contact == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Este usuario no existe"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }


@root.post("/api/users/reminder")
def create_reminder(user_id: int, data: Reminder):
    with engine.connect() as conn:
        try:

            exist_id = conn.execute(
                user.select().where(user.c.id_user == user_id)).first()

            if exist_id != None:

                if not validate_date(data.date_):
                    return {
                        "detail": "Ingrese una fecha válida"
                    }
                try:
                    validate_time(data.time_)
                except:
                    return {
                        "detail": "Ingrese una hora valida"
                    }
                new_reminder = dict(data)
                new_reminder["id_user"] = exist_id[0]
                new_reminder["date_"] = format_date(data.date_)
                new_reminder["status_"] = True
                result = conn.execute(reminder.insert().values(new_reminder))
                return conn.execute(reminder.select().where(reminder.c.id_reminder == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Este usuario no existe"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }


@root.post("/api/users/address/{user_id}")
def address(user_id: int, data: Address):
    with engine.connect() as conn:
        try:

            exist_id = conn.execute(user.select().where(
                user.c.id_user == user_id)).first()

            if exist_id != None:

                new_address = dict(data)
                new_address["id_user"] = exist_id[0]
                result = conn.execute(
                    user_address.insert().values(new_address))
                return conn.execute(user_address.select().where(user_address.c.id_user_address == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Usuario no encontrado"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }


@root.post("/api/users/appointment/{user_id}")
def create_appointment(user_id: int, data: Appointment):
    with engine.connect() as conn:
        try:

            exist_id = conn.execute(user.select().where(
                user.c.id_user == user_id)).first()

            if exist_id != None:

                if not validate_date(data.appointment_date):
                    return {
                        "detail": "Ingrese una fecha valida"
                    }

                new_appointment = dict(data)
                new_appointment["id_user"] = exist_id[0]
                try:
                    new_appointment["appointment_date"] = format_date(
                        data.appointment_date)
                except:
                    return {
                        "detail": "Esta fecha no es correcta"
                    }
                new_appointment["status_"] = True
                result = conn.execute(
                    appointment.insert().values(new_appointment))
                return conn.execute(appointment.select().where(appointment.c.id_appointment == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Usuario no encontrado"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }


@root.post("/api/users/info-appointments/{user_id}")
def create_info_appointment(appointment_id: int, data: InfoAppointment):
    with engine.connect() as conn:
        try:
            exist_id = conn.execute(appointment.select().where(
                appointment.c.id_appointment == appointment_id)).first()

            if exist_id != None:

                if not validate_blood_pressure(data.blood_pressure):
                    return {
                        "detail": "Formato incorrecto para presión sanguínea"
                    }
                if not validate_date(data.next_appointment_date):
                    return {
                        "detail": "Ingrese una fecha válida"
                    }
                new_info = dict(data)
                new_info["id_appointment"] = exist_id[0]
                try:
                    new_info["next_appointment_date"] = format_date(
                        data.next_appointment_date)
                except:
                    return {
                        "detail": "Esta fecha no es correcta"
                    }
                result = conn.execute(
                    info_appointment.insert().values(new_info))
                return conn.execute(info_appointment.select().where(info_appointment.c.id_info_appointment == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Cita no encontrada"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }


@root.post("/api/users/drug/{user_id}")
def add_drug(user_id: int, data: Drug):
    with engine.connect() as conn:
        try:
            exist_id = conn.execute(
                user.select().where(user.c.id_user == user_id)).first()

            if exist_id != None:
                new_drug = dict(data)
                new_drug["id_user"] = exist_id[0]
                result = conn.execute(drug.insert().values(new_drug))

                conn.execute(user_drug.insert().values(
                    id_user=exist_id[0], id_drug=result.lastrowid, status_=True))

                return conn.execute(drug.select().where(drug.c.id_drug == result.lastrowid)).first()

            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Usuario no encontrado"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }


@root.post("/api/users/allergy/{user_id}")
def add_allergy(user_id: int, data: Allergy):
    with engine.connect() as conn:
        try:
            exist_id = conn.execute(
                user.select().where(user.c.id_user == user_id)).first()

            if exist_id != None:
                new_allergy = dict(data)
                new_allergy["id_user"] = exist_id[0]
                result = conn.execute(allergy.insert().values(new_allergy))

                conn.execute(user_allergy.insert().values(
                    id_user=exist_id[0], id_allergy=result.lastrowid, status_=True))

                return conn.execute(allergy.select().where(allergy.c.id_allergy == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Usuario no encontrado"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "detail": "Ha ocurrido un error"
            }


@root.post("/api/users/chronic-disease/{user_id}")
def add_chronic_disease(user_id: int, data: ChronicDiseases):
    with engine.connect() as conn:
        try:
            exist_id = conn.execute(user.select().where(
                user.c.id_user == user_id)).first()

            if exist_id != None:
                new_chronic_disease = dict(data)
                new_chronic_disease["id_user"] = exist_id[0]
                result = conn.execute(
                    chronic_diseases.insert().values(new_chronic_disease))

                conn.execute(user_chronic_diseases.insert().values(
                    id_user=exist_id[0], id_chronic_disease=result.lastrowid, status_=True))

                return conn.execute(chronic_diseases.select().where(chronic_diseases.c.id_chronic_disease == result.lastrowid)).first()
            return {
                "status": HTTP_404_NOT_FOUND,
                "message": "Usuario no encontrado"
            }
        except:
            return {
                "status": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Ha ocurrido un error"
            }

# @root.post("/api/users/enfermedad/{user_id}")
# def registrar_enfermedad(user_id: int, enfermedad: Enfermedad):
#     with engine.connect() as conn:
#         result = conn.execute(user.select().where(
#             user.c.id == user_id)).first()
#         if result != None:
#             nueva_enfermedad = dict(enfermedad)
#             nueva_enfermedad["id"] = result[0]
#             nueva_enfermedad["nombre_enfermedad"] = format_string(
#                 enfermedad.nombre_enfermedad)
#             conn.execute(enfermedades.insert().values(nueva_enfermedad))
#             return nueva_enfermedad
#         return {
#             "status": HTTP_404_NOT_FOUND,
#             "message": "Usuario no encontrado"
#         }

# @user.get("/")  # Esta ruta solo esta para verificar que el servidor este en linea
# def root():
#     return {"message": "Hola, estas usando la Celud-API!"}


# # Esta ruta muestra todos los usuarios
# @user.get("/api/users", response_model=List[UserSchema])
# def get_users():
#     with engine.connect() as conn:
#         result = conn.execute(users.select()).fetchall()
#         return result


# # Esta ruta muestra un usuario a traves de su ID
# @user.get("/api/users/{user_id}")
# def get_user(user_id: int):
#     with engine.connect() as conn:
#         result = conn.execute(users.select().where(
#             users.c.id == user_id)).first()
#         if result != None:
#             return result
#         return {
#             "status": HTTP_404_NOT_FOUND,
#             "message": "User doesn't exist"
#         }


# @user.post("/api/users")  # Esta ruta permite que se agreguen usuarios a la db
# def create_user(data_user: UserSchema):
#     with engine.connect() as conn:
#         result = conn.execute(users.select().where(
#             users.c.user_mail == data_user.user_mail)).first()
#         # Valida que realmente se le esta pasando un email correcto
#         if check_email(data_user.user_mail):
#             if result != None:  # Valida que el email no este en uso
#                 check_exist = data_user.user_mail == result[2]
#                 if check_exist:
#                     return {
#                         "status": "HTTP_200_OK",
#                         "message": "Email address already in use"
#                     }
#             else:  # Crea el usuario y encripta la contrase;a
#                 new_user = dict(data_user)
#                 new_user["user_password"] = generate_password_hash(
#                     data_user.user_password, "pbkdf2:sha256:30", 30)
#                 conn.execute(users.insert().values(new_user))
#                 # conn.commit()
#                 return new_user
#         return {
#             "status": 400,
#             "detail": "The email address is not valid"
#         }


# # Ruta para hacer inicio de sesion
# @user.post("/api/users/login", status_code=HTTP_202_ACCEPTED)
# def user_login(data_user: Login):
#     with engine.connect() as conn:
#         result = conn.execute(users.select().where(
#             users.c.user_mail == data_user.user_mail)).first()

#         if result != None:
#             check_password = check_password_hash(
#                 result[3], data_user.user_password)

#             if check_password:
#                 return {
#                     "status": HTTP_202_ACCEPTED,
#                     "message": "Access success!"
#                 }

#         return {
#             "status": HTTP_401_UNAUTHORIZED,
#             "message": "Access denied"
#         }


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
