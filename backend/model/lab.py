# model/lab.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db


LabRouter = APIRouter(tags=["Lab"])

# CRUD operations

@LabRouter.get("/labincharge/", response_model=list)
async def get_labincharge(
    db=Depends(get_db)
):
    query = "SELECT labincharge_id, first_name, last_name, password FROM labincharge"
    db[0].execute(query)
    users = [{"labincharge_id": user[0], "first_name": user[1], "last_name": user[2], "password": user[3]} for user in db[0].fetchall()]
    return users

@LabRouter.get("/labpc/", response_model=list)
async def get_labpc(
    db=Depends(get_db)
):
    query = "SELECT pc_id, lab_room FROM labpc"
    db[0].execute(query)
    users = [{"pc_id": user[0], "lab_room": user[1]} for user in db[0].fetchall()]
    return users
    