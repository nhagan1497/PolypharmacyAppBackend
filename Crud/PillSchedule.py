from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

from sqlalchemy.orm import Session
from Models.PillSchedule import PillSchedule as PillScheduleDB
from Schema.PillSchedule import PillScheduleCreate, PillScheduleUpdate


def create_pill_schedule(db: Session, pill_schedule: PillScheduleCreate):
    db_pill_schedule = PillScheduleDB(**pill_schedule.dict())
    db.add(db_pill_schedule)
    db.commit()
    db.refresh(db_pill_schedule)
    return db_pill_schedule


def get_pill_schedule(db: Session, pill_schedule_id: int):
    return db.query(PillScheduleDB).filter(PillScheduleDB.id == pill_schedule_id).first()


def get_pill_schedules(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PillScheduleDB).order_by(PillScheduleDB.id).offset(skip).limit(limit).all()


def update_pill_schedule(db: Session, pill_schedule_id: int, pill_schedule_update: PillScheduleUpdate):
    db_pill_schedule = db.query(PillScheduleDB).filter(PillScheduleDB.id == pill_schedule_id).first()
    if not db_pill_schedule:
        return None
    for var, value in vars(pill_schedule_update).items():
        if value is not None:
            setattr(db_pill_schedule, var, value)
    db.commit()
    db.refresh(db_pill_schedule)
    return db_pill_schedule


def delete_pill_schedule(db: Session, pill_schedule_id: int):
    db_pill_schedule = db.query(PillScheduleDB).filter(PillScheduleDB.id == pill_schedule_id).first()
    if not db_pill_schedule:
        return None
    db.delete(db_pill_schedule)
    db.commit()
    return db_pill_schedule