# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.users import UsersRouter


app = FastAPI()

# Include CRUD routes from modules
app.include_router(UsersRouter, prefix="/api")


# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)