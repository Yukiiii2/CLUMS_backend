# model/report.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


ReportRouter = APIRouter(tags=["report"])

@ReportRouter.get("/report/", response_model=list)
async def get_report(
    db=Depends(get_db)
):
    query = "SELECT report_id, issue, unit_number FROM report"
    db[0].execute(query)
    users = [{"report_id": user[0], "issue":user[1], "unit_number": user[2]} for user in db[0].fetchall()]
    return users

@ReportRouter.delete("/report/{report_id}", response_model=dict)
async def delete_report(
    report_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT report_id FROM report WHERE report_id = %s"
        db[0].execute(query_check_user, (report_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM report WHERE report_id = %s"
        db[0].execute(query_delete_user, (report_id,))
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

@ReportRouter.post("/report/create", response_model=dict)
async def create_report(
    issue: str = Form(...), 
    unit_number: int = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO report (issue, unit_number) VALUES (%s, %s)"
    db[0].execute(query, (issue, unit_number))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_report_id = db[0].fetchone()[0]
    db[1].commit()
    
    return {"report_id": new_report_id, "unit_number": unit_number, "issue": issue, "message": "Report Created Successfully"}

@ReportRouter.put("/change_report/{user_id}", response_model=dict)
async def update_report_issue(
    report_id: int = Form(...),  # assuming report_id is an integer
    issue: str = Form(...),
    db=Depends(get_db)
):
    # Update report issue in the database 
    query = "UPDATE report SET issue = %s WHERE report_id = %s"
    db[0].execute(query, (issue, report_id))
    db[1].commit()
    return {"issue": issue}
    
    # If no rows were affected, report not found
    raise HTTPException(status_code=404, detail="Report not found")

@ReportRouter.get("/report/{report_id}", response_model=dict)
async def read_report(
    report_id: int, 
    db=Depends(get_db)
):
    query = "SELECT report_id, issue FROM report WHERE report_id = %s"
    db[0].execute(query, (report_id,))
    user = db[0].fetchone()
    if user:
        return {"report_id": user[0], "issue": user[1]}
    raise HTTPException(status_code=404, detail="User not found")





