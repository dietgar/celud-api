from pydantic import BaseModel


class Register(BaseModel):
    id: int | None = None
    first_name: str
    middle_name: str
    last_name: str
    second_last_name: str
    username: str
    email: str
    password: str
