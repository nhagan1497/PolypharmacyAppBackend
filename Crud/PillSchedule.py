from sqlalchemy.orm import Session
from Models.PillSchedule import PillSchedule as PillScheduleDB
from Schema.PillSchedule import PillScheduleCreate, PillScheduleUpdate

from Models.Pill import Pill as PillDB

def create_pill_schedule(db: Session, pill_schedule: PillScheduleCreate, user_id: str = None):
    db_pill_schedule = PillScheduleDB(**pill_schedule.dict(), user_id=user_id)
    db.add(db_pill_schedule)
    db.commit()
    db.refresh(db_pill_schedule)
    return db_pill_schedule


def get_pill_schedule(db: Session, pill_schedule_id: int, user_id: str = None):
    return db.query(PillScheduleDB).filter(
        PillScheduleDB.id == pill_schedule_id,
        PillScheduleDB.user_id == user_id
    ).first()


def get_pill_schedules(db: Session, skip: int = 0, limit: int = 10, user_id: str = None):
    query_result = db.query(PillScheduleDB).filter(PillScheduleDB.user_id == user_id)
    if skip and limit:
        query_result = query_result.order_by(PillScheduleDB.id).offset(skip).limit(limit)
    return query_result.all()


def get_pill_schedule_details(db: Session, user_id: str):
    return (db.query(PillScheduleDB, PillDB)
            .join(PillDB, PillScheduleDB.pill_id == PillDB.id)  # Adjust the field names accordingly
            .filter(PillScheduleDB.user_id == user_id)
            .order_by(PillScheduleDB.id)
            .all())

def update_pill_schedule(db: Session, pill_schedule_id: int, pill_schedule_update: PillScheduleUpdate, user_id: str = None):
    db_pill_schedule = db.query(PillScheduleDB).filter(
        PillScheduleDB.id == pill_schedule_id,
        PillScheduleDB.user_id == user_id
    ).first()
    if not db_pill_schedule:
        return None
    for var, value in vars(pill_schedule_update).items():
        if value is not None:
            setattr(db_pill_schedule, var, value)
    db.commit()
    db.refresh(db_pill_schedule)
    return db_pill_schedule


def delete_pill_schedule(db: Session, pill_schedule_id: int, user_id: str = None):
    db_pill_schedule = db.query(PillScheduleDB).filter(
        PillScheduleDB.id == pill_schedule_id,
        PillScheduleDB.user_id == user_id
    ).first()
    if not db_pill_schedule:
        return None
    db.delete(db_pill_schedule)
    db.commit()
    return db_pill_schedule
