from fastapi import APIRouter
from config.db import engine
from models.user import user
from schemas.user_schema import Register
from starlette.status import *
from werkzeug.security import generate_password_hash, check_password_hash
# from typing import List
import re

root = APIRouter()


def format_name(name):
    try:
        delete_white_spaces = name.replace(" ", "")
        name_to_minus = delete_white_spaces.casefold()
        name_to_capitalize = name_to_minus.capitalize()
        return name_to_capitalize
    except:
        return False


def validate_names(name):
    try:
        if len(name) > 0 and len(name) < 50:
            number = False
            digit = False
            if re.search(r'\d', name):
                number = True
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', name):
                digit = True
            if not digit and number:
                return False
            return True
    except:
        return False


def exist_username(username):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.username == username)).first()
        if result == None:
            return True
        return False


def validate_username(username):
    if len(username) > 3 and len(username) < 15:
        if re.match(r'^[a-zA-Z0-9_-]+$', username):
            return True
    return {
        "detail": "The username is already in use"
    }


def exist_email(email):
    with engine.connect() as conn:
        result = conn.execute(user.select().where(
            user.c.email == email)).first()
        if result == None:
            return True
        return {
            "detail": "The email addres is already in use"
        }


def validate_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    result = re.match(pattern, email)
    if result:
        return True
    return False


def validate_secure_password(password):
    mayus = False
    minus = False
    number = False
    digit = False
    if len(password) >= 8 and len(password) < 50:
        if re.search(r'[A-Z]', password):
            mayus = True
        if re.search(r'[a-z]', password):
            minus = True
        if re.search(r'\d', password):
            number = True
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            digit = True
        if mayus and minus and number and digit:
            return True
    return False


def validate_data_user(data_user: Register):
    try:
        counter = 0
        if validate_names(data_user.first_name):
            counter += 1
            print("primer nombre", counter)

        if validate_names(data_user.middle_name):
            counter += 1
            print("segundo nombre", counter)

        if validate_names(data_user.last_name):
            counter += 1
            print("apellido", counter)

        if validate_names(data_user.second_last_name):
            counter += 1
            print("segundo apellido", counter)

        if validate_email(data_user.email):
            counter += 1
            print("email", counter)

        if validate_secure_password(data_user.password):
            counter += 1
            print("contra", counter)

        print(counter)

        if counter == 6:
            return True
        return False

    except:
        return {
            "status": HTTP_400_BAD_REQUEST,
            "message": "Unexpected error"
        }


@root.post("/api/users/register")
def register(data_user: Register):
    with engine.connect() as conn:
        try:
            if validate_data_user(data_user):
                if exist_username:
                    if exist_email:
                        new_user = dict(data_user)
                        new_user["first_name"] = format_name(
                            data_user.first_name)
                        new_user["middle_name"] = format_name(
                            data_user.middle_name)
                        new_user["last_name"] = format_name(
                            data_user.last_name)
                        new_user["second_last_name"] = format_name(
                            data_user.second_last_name)
                        new_user["password"] = generate_password_hash(
                            data_user.password, "pbkdf2:sha256:30", 30)
                        print(new_user)
                        conn.execute(user.insert().values(new_user))
                        return new_user
                    return {
                        "status": HTTP_422_UNPROCESSABLE_ENTITY,
                        "message": "The request isn't valid"
                    }
        except:
            return {
                "status": "",
                "message": "Unknown error"
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
