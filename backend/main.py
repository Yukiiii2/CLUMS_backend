# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model.users import UsersRouter
from model.lab import LabRouter
from model.report import ReportRouter
from model.admin import AdminRouter
from model.teacherLogin import TeacherLoginRouter 

app = FastAPI()

# Define allowed origins
origins = [
    "http://localhost:",
    "http://localhost:5173",  # Assuming your Vue.js server runs on port 8080
]

# Include CRUD routes from modules
app.include_router(UsersRouter, prefix="/api")
app.include_router(LabRouter, prefix="/api")
app.include_router(ReportRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(TeacherLoginRouter, prefix="/api")   

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
