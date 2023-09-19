from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int | None = None
    user_name: str
    user_mail: str
    user_password: str


class Login(BaseModel):
    user_name: str
    user_password: str
