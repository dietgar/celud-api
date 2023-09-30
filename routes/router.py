from fastapi import APIRouter, Response
from config.db import engine
from models.user import users
from schemas.user_schema import Login, UserSchema
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_202_ACCEPTED
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
import re
from validate_email import validate_email

user = APIRouter()

# Verificar que el correo representa una direccion valida


def check_email(email):
    pattern = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pattern, email):
        return True
    return False


@user.get("/")
def root():
    return {"message": "Hola, estas usando la Celud-API!"}

# Ruta que devuelve todos los usuarios de la db


@user.get("/api/users", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

# Ruta que devuelve un usuario por su ID


@user.get("/api/users/{user_id}")
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()
        if result != None:
            return result
        return {
            "status": 404,
            "message": "User doesn't exist"
        }


@user.post("/api/users")
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.user_mail == data_user.user_mail)).first()
        if validate_email(data_user.user_mail):
            if result != None:
                check_exist = data_user.user_mail == result[2]
                if check_exist:
                    return {
                        "status": "HTTP_200_OK",
                        "message": "Email address already in use"
                    }
            else:
                new_user = dict(data_user)
                new_user["user_password"] = generate_password_hash(
                    data_user.user_password, "pbkdf2:sha256:30", 30)
                conn.execute(users.insert().values(new_user))
                # conn.commit()
                return new_user
        return {
            "status": 400,
            "detail": "The email address is not valid"
        }
# Ruta que simula un inicio de sesion a traves de user_name y user_password


@user.post("/api/users/login", status_code=HTTP_202_ACCEPTED)
def user_login(data_user: Login):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.user_mail == data_user.user_mail)).first()

        if result != None:
            check_password = check_password_hash(
                result[3], data_user.user_password)

            if check_password:
                return {
                    "status": HTTP_202_ACCEPTED,
                    "message": "Access success!"
                }

        return {
            "status": HTTP_401_UNAUTHORIZED,
            "message": "Access denied"
        }

# Ruta que permite actualizar un usuario a traves de su ID


@user.put("/api/users/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: int):
    with engine.connect() as conn:
        encrypt_password = generate_password_hash(
            data_update.user_password, "pbkdf2:sha256:30", 30)
        conn.execute(users.update().values(user_name=data_update.user_name, user_mail=data_update.user_mail,
                                           user_password=encrypt_password).where(users.c.id == user_id))
        # conn.commit()
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()
    return result

# Ruta que permite eliminar usuarios por ID


@user.delete("/api/users/{user_id}", status_code=HTTP_200_OK)
def delete_user(user_id: int):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        # conn.commit()
    return Response(status_code=HTTP_200_OK)
