from fastapi import APIRouter, Response
from config.db import engine
from models.user import users
from schemas.user_schema import Login, UserSchema
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED, HTTP_202_ACCEPTED
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

user = APIRouter()

# Ruta que devuelve todos los usuarios de la db


@user.get("/users", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

# Ruta que devuelve un usuario por su ID


@user.get("/users/{user_id}")
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first
    if result:
        return dict(result._asdict())
    return {
        "status": HTTP_404_NOT_FOUND,
        "message": "User doesn't exist"
    }

# Ruta que permite crear usuarios


@user.post("/users", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.user_name == data_user.user_name)).first()
        if result != None:
            check_exist = data_user.user_name == result[1]
            if check_exist:
                return {
                    "status": "HTTP_200_OK",
                    "message": "User already exist"
                }
        else:
            new_user = dict(data_user)
            new_user["user_password"] = generate_password_hash(
                data_user.user_password, "pbkdf2:sha256:30", 30)
            conn.execute(users.insert().values(new_user))
            conn.commit()
            return Response(status_code=HTTP_201_CREATED)

# Ruta que simula un inicio de sesion a traves de user_name y user_password


@user.post("/users/login", status_code=HTTP_202_ACCEPTED)
def user_login(data_user: Login):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.user_name == data_user.user_name)).first()

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


@user.put("/users/{user_id}", response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: int):
    with engine.connect() as conn:
        encrypt_password = generate_password_hash(
            data_update.user_password, "pbkdf2:sha256:30", 30)
        conn.execute(users.update().values(user_name=data_update.user_name, user_mail=data_update.user_mail,
                                           user_password=encrypt_password).where(users.c.id == user_id))
        conn.commit()
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()
    return result

# Ruta que permite eliminar usuarios por ID


@user.delete("/users/{user_id}", status_code=HTTP_200_OK)
def delete_user(user_id: int):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))
        conn.commit()
    return Response(status_code=HTTP_200_OK)
