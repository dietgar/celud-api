from fastapi import FastAPI
from routes.router import root
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "Salud Móvil API-Rest"
app.version = "0.0.5"

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root)
