from fastapi import APIRouter, Response
from sqlalchemy import select
from config.db import conn
from models.user import logins
from schemas.user import Login
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND
from cryptography.fernet import Fernet
from typing import List

user = APIRouter()
key = Fernet.generate_key()
f = Fernet(key)


@user.get("/users", response_model=List[Login])
async def get_users():
    result = conn.execute(logins.select()).fetchall()
    return result


@user.post("/users")
async def create_user(login: Login):
    new_user = {"user_name": login.user_name,
                "user_mail": login.user_mail}
    new_user["password"] = f.encrypt(login.password.encode("utf-8"))
    conn.execute(logins.insert().values(new_user))
    conn.commit()
    return Response(status_code=HTTP_201_CREATED)


@user.get("/users/{id}")
async def get_user(id: int):
    query = select(logins).where(logins.c.id_login == id)
    result = conn.execute(query).fetchone()
    if result:
        user_data = dict(result._asdict())
        return user_data
    else:
        return Response(status_code=HTTP_404_NOT_FOUND)
