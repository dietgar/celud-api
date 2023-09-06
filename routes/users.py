from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User, Login
from cryptography.fernet import Fernet

key = Fernet.generate_key()
f = Fernet(key)

user = APIRouter()


@user.get('/users')
def get_users():
    return conn.execute(users.select()).fetchall()


@user.post("/users")
def create_user(user: User):
    new_user = {"first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "height": user.height,
                "weight": user.weight}
    result = conn.execute(users.insert().values(new_user))
    print(result)
    return "Hello World"


@user.post("/login")
def sign_in(login: Login):
    signin = {"username": login.user_name,
              "email": login.user_mail}
    signin["password"] = f.encrypt(login.password.encode("utf-8"))
    print(signin)
    return "Registro exitoso"
