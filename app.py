from fastapi import FastAPI
from routes.router import user

app = FastAPI()

app.include_router(user)
