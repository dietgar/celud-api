from fastapi import APIRouter
from config.db import conn
from models.user import logins
from schemas.user import Login
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get('/users')
def get_users():
    return conn.execute(logins.select()).fetchall()


@user.post("/users")
def create_user(login: Login):
    new_user = {"user_name": login.user_name,
                "user_mail": login.user_mail}
    new_user["password"] = f.encrypt(login.password.encode("utf-8"))
    conn.execute(logins.insert().values(new_user))
    conn.commit()
    return new_user
