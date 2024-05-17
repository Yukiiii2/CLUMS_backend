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
    query = "SELECT Student_ID, Student_Name, Subject_ID, Section FROM students"
    db[0].execute(query)
    users = [{"student_id": user[0], "student_name": user[1], "Subject": user[2], "Section": user[3]} for user in db[0].fetchall()]
    return users
@UsersRouter.post("/student/login/", response_model=dict)
async def login_student(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists
    query_check_user = "SELECT password FROM students WHERE username = %s"
    db[0].execute(query_check_user, (username,))
    user = db[0].fetchone()

    if user:
        # Retrieve the stored password from the database
        stored_password = user[0]

        if password == stored_password:
            # If username and password are correct, print login successful
             return {"message": "Login successful"}
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")


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

@UsersRouter.get("/student/{student_id}", response_model=dict)
async def read_user(
    student_id: int, 
    db=Depends(get_db)
):
    query = "SELECT student_id, student_name FROM users_login WHERE student_id = %s"
    db[0].execute(query, (student_id,))
    user = db[0].fetchone()
    if user:
        return {"Student_id": user[0], "student_name": user[1]}
    raise HTTPException(status_code=404, detail="User not found")

@UsersRouter.post("/users/create", response_model=dict)
async def create_administrator(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO users_login (username, password) VALUES (%s, %s)"
    db[0].execute(query, (username, password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()
    
    return {"student_id": new_user_id, "username": username, "password": password, "message": "Account Created Successfully"}

@UsersRouter.put("/change_password/{user_id}", response_model=dict)
async def update_password(
    user_id: int,
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    db=Depends(get_db)
):
    # Check if user_id exists in the database
    check_query = "SELECT EXISTS(SELECT 1 FROM students WHERE Student_ID = %s)"
    db[0].execute(check_query, (user_id,))
    user_exists = db[0].fetchone()[0]

    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if new_password matches confirm_password
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="New password and confirm password do not match")

    # Update user password in the database
    update_query = "UPDATE students SET password = %s WHERE Student_ID = %s"
    db[0].execute(update_query, (new_password, user_id))
    db[1].commit()

    return {"message": "Password updated successfully"}

@UsersRouter.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    student_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT student_id FROM users_login WHERE student_id = %s"
        db[0].execute(query_check_user, (student_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM users_login WHERE student_id = %s"
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
