from fastapi import FastAPI
from routes.router import root

app = FastAPI()

app.include_router(root)
