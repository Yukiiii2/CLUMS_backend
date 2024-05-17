# model/teacherLogin.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
from datetime import datetime

TeacherLoginRouter = APIRouter(tags=["TeacherLogin"])

@TeacherLoginRouter.get("/teacher/", response_model=list)
async def get_teacher(
    db=Depends(get_db)
):
    query = "SELECT teacher_id, first_name, last_name FROM teacher"
    db[0].execute(query)
    users = [{"teacher_id": user[0], "first_name": user[1], "last_name": user[2]} for user in db[0].fetchall()]
    return users

@TeacherLoginRouter.get("/teacher_login/", response_model=list)
async def get_teacher_login(
    db=Depends(get_db)
):
    # Query to get teacher login data ordered by login time in descending order
    query = "SELECT first_name, last_name FROM teacher_login ORDER BY log_in DESC limit 1"
    db[0].execute(query)
    teacher_logins = [{ "first_name": login[0], "last_name": login[1]} for login in db[0].fetchall()]
    return teacher_logins

def store_teacher_login_data_in_db(db, teacher_ID):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Fetch first_name and last_name corresponding to teacher_ID
    query_fetch_teacher_data = "SELECT first_name, last_name FROM teacher WHERE teacher_id = %s"
    db[0].execute(query_fetch_teacher_data, (teacher_ID,))
    teacher_data = db[0].fetchone()
    first_name, last_name = teacher_data

    # Insert data into teacher_login table
    query_insert_teacher_login = "INSERT INTO teacher_login (teacher_id, first_name, last_name, log_in) VALUES (%s, %s, %s, %s)"
    db[0].execute(query_insert_teacher_login, (teacher_ID, first_name, last_name, current_datetime))
    db[1].commit()

@TeacherLoginRouter.post("/teacher/login/", response_model=dict)
async def login_administrator(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists and get additional details
    query_check_user = "SELECT teacher_ID, password, first_name, last_name FROM teacher WHERE username = %s "
    db[0].execute(query_check_user, (username,))
    user = db[0].fetchone()

    if user:
        # Properly unpack the tuple
        teacher_ID, stored_password, first_name, last_name = user

        # Verify the plain text password
        if password == stored_password:
            store_teacher_login_data_in_db(db, teacher_ID)
            return {
                "message": "Login successful",
                "teacher_id": teacher_ID,
                "first_name": first_name,
                "last_name": last_name
            }
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")