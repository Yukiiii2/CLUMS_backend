# model/admin.py
from fastapi import Depends, HTTPException, APIRouter, Form
from datetime import datetime
from .db import get_db

AdminRouter = APIRouter(tags=["Admin"])

# Define the new routes and functions
@AdminRouter.get("/Admin/", response_model=list)
async def get_students(db=Depends(get_db)):
    query = "SELECT student_id, student_name, PC_Number, Lab_Room, Subject_ID, Section FROM students"
    db[0].execute(query)
    users = [{"student_id": user[0], "student_name": user[1], "PC_Number": user[2], "Lab_Room": user[3], "Subject_ID": user[4], "Section": user[5]} for user in db[0].fetchall()]
    return users

@AdminRouter.get("/admin_login/", response_model=list)
async def get_admin_login(db=Depends(get_db)):
    query = "SELECT first_name, last_name FROM labincharge_login ORDER BY log_in DESC limit 1"
    db[0].execute(query)
    users = [{"first_name": user[0], "last_name": user[1]} for user in db[0].fetchall()]
    return users

def store_admin_login_data_in_db(db, admin_ID):
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Fetch first_name and last_name corresponding to admin_ID
    query_fetch_admin_data = "SELECT first_name, last_name FROM labincharge WHERE labincharge_id = %s"
    db[0].execute(query_fetch_admin_data, (admin_ID,))
    admin_data = db[0].fetchone()
    first_name, last_name = admin_data

    # Insert data into admin_login table
    query_insert_admin_login = "INSERT INTO labincharge_login (labincharge_id, first_name, last_name, log_in) VALUES (%s, %s, %s, %s)"
    db[0].execute(query_insert_admin_login, (admin_ID, first_name, last_name, current_datetime))
    db[1].commit()

@AdminRouter.post("/admin/login/", response_model=dict)
async def login_administrator(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists
    query_check_user = "SELECT labincharge_id, password, first_name, last_name FROM labincharge WHERE username = %s"
    db[0].execute(query_check_user, (username,))
    admin = db[0].fetchone()

    if admin:
        # Properly unpack the tuple
        admin_id, stored_password, first_name, last_name = admin

        # Verify the password
        if password == stored_password:
            # If username and password are correct, store login data and return login successful along with admin's name
            store_admin_login_data_in_db(db, admin_id)
            return {
                "message": "Login successful", 
                "admin_id": admin_id, 
                "first_name": first_name, 
                "last_name": last_name
            }
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@AdminRouter.post("/admin/create", response_model=dict)
async def Add_Student(
    student_name: str = Form(...), 
    pc_number: int = Form(...), 
    lab_room: int = Form(...),
    subject_id: str = Form(...),
    section: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):

    query_insert_student = "INSERT INTO students (student_name, pc_number, lab_room, subject_id, section, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    db[0].execute(query_insert_student, (student_name, pc_number, lab_room, subject_id, section, username, password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]


    db[1].commit()

    return {
            "student_id": new_user_id,
            "student_name": student_name,
            "pc_number": pc_number,
            "lab_room": lab_room,
            "subject_id": subject_id,
            "section": section,
            "username": username,
            "message": "Student Has been Added Successfully"
        }

        # Handle the case where the ID retrieval fails
    return {"message": "Failed to add student. Please try again."}
