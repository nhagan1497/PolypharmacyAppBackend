from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

import Crud.PillSchedule as PillScheduleCrud
import Schema.PillSchedule as PillScheduleSchema
import Models.PillSchedule as PillScheduleModel

pill_schedule_router = APIRouter()


@pill_schedule_router.post("/", response_model=PillScheduleSchema.PillSchedule)
def create_pill_schedule(pill_schedule: PillScheduleSchema.PillScheduleCreate, db: Session = Depends(get_db)):
    return PillScheduleCrud.create_pill_schedule(db=db, pill_schedule=pill_schedule)


@pill_schedule_router.get("/{pill_schedule_id}", response_model=PillScheduleSchema.PillSchedule)
def read_pill_schedule(pill_schedule_id: int, db: Session = Depends(get_db)):
    db_pill_schedule = PillScheduleCrud.get_pill_schedule(db=db, pill_schedule_id=pill_schedule_id)
    if db_pill_schedule is None:
        raise HTTPException(status_code=404, detail="Pill schedule not found")
    return db_pill_schedule


@pill_schedule_router.get("/", response_model=list[PillScheduleSchema.PillSchedule])
def read_pill_schedules(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pill_schedules = PillScheduleCrud.get_pill_schedules(db=db, skip=skip, limit=limit)
    return pill_schedules


@pill_schedule_router.put("/{pill_schedule_id}", response_model=PillScheduleSchema.PillSchedule)
def update_pill_schedule(pill_schedule_id: int, pill_schedule_update: PillScheduleSchema.PillScheduleUpdate, db: Session = Depends(get_db)):
    db_pill_schedule = PillScheduleCrud.update_pill_schedule(db=db, pill_schedule_id=pill_schedule_id, pill_schedule_update=pill_schedule_update)
    if db_pill_schedule is None:
        raise HTTPException(status_code=404, detail="Pill schedule not found")
    return db_pill_schedule


@pill_schedule_router.delete("/{pill_schedule_id}", response_model=PillScheduleSchema.PillSchedule)
def delete_pill_schedule(pill_schedule_id: int, db: Session = Depends(get_db)):
    db_pill_schedule = PillScheduleCrud.delete_pill_schedule(db=db, pill_schedule_id=pill_schedule_id)
    if db_pill_schedule is None:
        raise HTTPException(status_code=404, detail="Pill schedule not found")
    return db_pill_schedule