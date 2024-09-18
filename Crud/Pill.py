from sqlalchemy.orm import Session
from Models.Pill import Pill as PillDB
from Schema.Pill import PillCreate, PillUpdate

from sqlalchemy import or_


def create_pill(db: Session, pill: PillCreate, user_id: str = None):
    db_pill = PillDB(**pill.dict(), user_id=user_id)
    db.add(db_pill)
    db.commit()
    db.refresh(db_pill)
    return db_pill


def get_pill(db: Session, pill_id: int, user_id: str = None):
    return db.query(PillDB).filter(
        PillDB.id == pill_id,
        (PillDB.user_id == user_id) | (PillDB.user_id == None)
    ).first()


def get_pill_by_name(db: Session, name: str, user_id: str = None):
    return db.query(PillDB).filter(
        PillDB.name == name,
        (PillDB.user_id == user_id) | (PillDB.user_id == None)
    ).first()


def get_pills(db: Session, skip: int = 0, limit: int = 10, user_id: str = None):
    return db.query(PillDB).filter(
        (PillDB.user_id == user_id) | (PillDB.user_id == None)
    ).order_by(PillDB.id).offset(skip).limit(limit).all()


def update_pill(db: Session, pill_id: int, pill_update: PillUpdate, user_id: str):
    db_pill = db.query(PillDB).filter(
        PillDB.id == pill_id,
        (PillDB.user_id == user_id)
    ).first()
    if not db_pill:
        return None
    for var, value in vars(pill_update).items():
        if value is not None:
            setattr(db_pill, var, value)
    db.commit()
    db.refresh(db_pill)
    return db_pill


def delete_pill(db: Session, pill_id: int, user_id: str):
    db_pill = db.query(PillDB).filter(
        PillDB.id == pill_id,
        (PillDB.user_id == user_id)
    ).first()
    if not db_pill:
        return None
    db.delete(db_pill)
    db.commit()
    return db_pill
