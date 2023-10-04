from fastapi import APIRouter
from config.db import engine
from models.user import user
from schemas.user_schema import Register, Login
from starlette.status import *
from werkzeug.security import generate_password_hash, check_password_hash
import re
from validations.user_data import *
# from typing import List

root = APIRouter()


@root.post("/api/users/register")
def register(data_user: Register):
    with engine.connect() as conn:
        try:

            if exist_username(data_user.username):
                return {
                    "detail": "Este nombre de usuario ya está en uso"
                }

            if exist_email(data_user.email):
                print("Entra aqui")
                return {
                    "detail": "Este correo electrónico ya pertenece a otra cuenta"
                }

            if validate_data_user(data_user):
                print("hello")
                new_user = dict(data_user)
                new_user["first_name"] = format_name(data_user.first_name)
                new_user["middle_name"] = format_name(data_user.middle_name)
                new_user["last_name"] = format_name(data_user.last_name)
                new_user["second_last_name"] = format_name(
                    data_user.second_last_name)
                new_user["password"] = generate_password_hash(
                    data_user.password, "pbkdf2:sha256:30", 30)
                print(new_user)
                conn.execute(user.insert().values(new_user))
                return new_user

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
