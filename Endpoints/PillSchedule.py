from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

import auth

import Crud.PillSchedule as PillScheduleCrud
import Schema.PillSchedule as PillScheduleSchema
import Models.PillSchedule as PillScheduleModel

import Schema.Pill as PillSchema

pill_schedule_router = APIRouter()


@pill_schedule_router.post("/", response_model=PillScheduleSchema.PillSchedule)
def create_pill_schedule(pill_schedule: PillScheduleSchema.PillScheduleCreate, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    return PillScheduleCrud.create_pill_schedule(db=db, pill_schedule=pill_schedule, user_id=user_id)


@pill_schedule_router.get("/{pill_schedule_id}", response_model=PillScheduleSchema.PillSchedule)
def read_pill_schedule(pill_schedule_id: int, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_schedule = PillScheduleCrud.get_pill_schedule(db=db, pill_schedule_id=pill_schedule_id, user_id=user_id)
    if db_pill_schedule is None:
        raise HTTPException(status_code=404, detail="Pill schedule not found")
    return db_pill_schedule


@pill_schedule_router.get("/", response_model=list[PillScheduleSchema.PillSchedule])
def read_pill_schedules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    pill_schedules = PillScheduleCrud.get_pill_schedules(db=db, skip=skip, limit=limit, user_id=user_id)
    return pill_schedules


@pill_schedule_router.put("/{pill_schedule_id}", response_model=PillScheduleSchema.PillSchedule)
def update_pill_schedule(pill_schedule_id: int, pill_schedule_update: PillScheduleSchema.PillScheduleUpdate, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_schedule = PillScheduleCrud.update_pill_schedule(db=db, pill_schedule_id=pill_schedule_id, pill_schedule_update=pill_schedule_update, user_id=user_id)
    if db_pill_schedule is None:
        raise HTTPException(status_code=404, detail="Pill schedule not found")
    return db_pill_schedule


@pill_schedule_router.delete("/{pill_schedule_id}", response_model=PillScheduleSchema.PillSchedule)
def delete_pill_schedule(pill_schedule_id: int, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_schedule = PillScheduleCrud.delete_pill_schedule(db=db, pill_schedule_id=pill_schedule_id, user_id=user_id)
    if db_pill_schedule is None:
        raise HTTPException(status_code=404, detail="Pill schedule not found")
    return db_pill_schedule


@pill_schedule_router.get("/pill_schedule_details/", response_model=list[tuple[PillScheduleSchema.PillSchedule, PillSchema.Pill]])
def read_pill_consumption_details(db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_consumption_details = PillScheduleCrud.get_pill_schedule_details(db=db, user_id=user_id)
    if db_pill_consumption_details is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")

    return [(consumption, pill) for consumption, pill in db_pill_consumption_details]