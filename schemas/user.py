from pydantic import BaseModel


class Login(BaseModel):
    user_name: str
    user_mail: str
    password: str
