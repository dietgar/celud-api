from pydantic import BaseModel


class Register(BaseModel):
    id: int | None = None
    first_name: str
    middle_name: str | None = None
    last_name: str
    second_last_name: str | None = None
    username: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str
