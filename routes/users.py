from fastapi import APIRouter
from config.db import conn
from models.user import users
from schemas.user import User
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
    print(new_user)
    return "Hello World"
