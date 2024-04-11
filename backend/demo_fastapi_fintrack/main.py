# main.py
from fastapi import FastAPI
from model.users import UsersRouter


app = FastAPI()

# Include CRUD routes from modules
app.include_router(UsersRouter, prefix="/api")
