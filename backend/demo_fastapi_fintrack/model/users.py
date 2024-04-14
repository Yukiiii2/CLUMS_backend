# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

UsersRouter = APIRouter(tags=["Users"])

# CRUD operations

@UsersRouter.get("/student/", response_model=list)
async def get_students(
    db=Depends(get_db)
):
    query = "SELECT student_id, last_name, password FROM users"
    db[0].execute(query)
    users = [{"student_id": user[0], "last_name": user[1], "password": user[2]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/labincharge/", response_model=list)
async def get_labincharge(
    db=Depends(get_db)
):
    query = "SELECT labincharge_id, first_name, last_name FROM labincharge"
    db[0].execute(query)
    users = [{"labincharge": user[0], "first_name": user[1], "last_name": user[2]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/teacher/", response_model=list)
async def get_teacher(
    db=Depends(get_db)
):
    query = "SELECT teacher_id, last_name FROM teacher"
    db[0].execute(query)
    users = [{"teacher_id": user[0], "first_name": user[1]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/enrollment/", response_model=list)
async def get_enrollment(
    db=Depends(get_db)
):
    query = "SELECT enrollment_id, enrollment_date FROM enrollment"
    db[0].execute(query)
    users = [{"enrollment_id": user[0], "enrollment_date": user[1]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/subject/", response_model=list)
async def get_subjects(
    db=Depends(get_db)
):
    query = "SELECT subject_id, subject_name FROM subject"
    db[0].execute(query)
    users = [{"subject_id": user[0], "subject_name": user[1]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/labpc/", response_model=list)
async def get_labpc(
    db=Depends(get_db)
):
    query = "SELECT pc_id, lab_room FROM labpc"
    db[0].execute(query)
    users = [{"pc_id": user[0], "lab_room": user[1]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/report/", response_model=list)
async def get_report(
    db=Depends(get_db)
):
    query = "SELECT report_id, student_id FROM report"
    db[0].execute(query)
    users = [{"report_id": user[0], "student_id": user[1]} for user in db[0].fetchall()]
    return users

@UsersRouter.get("/student/{student_id}", response_model=dict)
async def read_user(
    student_id: int, 
    db=Depends(get_db)
):
    query = "SELECT student_id, last_name FROM users WHERE student_id = %s"
    db[0].execute(query, (student_id,))
    user = db[0].fetchone()
    if user:
        return {"Student_id": user[0], "last_name": user[1]}
    raise HTTPException(status_code=404, detail="User not found")

@UsersRouter.post("/users/", response_model=dict)
async def create_user(
    student_id: int = Form(...),
    last_name: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)):

    query = "INSERT INTO users (student_id, last_name, username, password) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (student_id, last_name, username, password))
    db[1].commit()

    return {"student_id": student_id, "last_name":last_name, "username": username, "password":password,}

@UsersRouter.put("/users/{user_id}", response_model=dict)
async def update_user(
    student_id: int,
    last_name: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    # Update user information in the database 
    query = "UPDATE users SET last_name = %s, username = %s, password = %s WHERE student_id = %s"
    db[0].execute(query, (last_name, username , password, student_id))
    db[1].commit()
    return {"student_id": student_id, "last_name":last_name, "username": username, "password":password,}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@UsersRouter.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    student_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT student_id FROM users WHERE student_id = %s"
        db[0].execute(query_check_user, (student_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM users WHERE student_id = %s"
        db[0].execute(query_delete_user, (student_id,))
        db[1].commit()

        return {"message": "User deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

# Password hashing function using bcrypt
def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string for storage
