from pydantic import BaseModel

# Modelo para la tabla users


class UserSchema(BaseModel):
    id: int | None = None
    user_name: str
    user_mail: str
    user_password: str

# Modelo para login


class Login(BaseModel):
    user_mail: str
    user_password: str
