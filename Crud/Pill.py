from sqlalchemy.orm import Session
from Models.Pill import Pill as PillDB
from Schema.Pill import PillCreate, PillUpdate


def create_pill(db: Session, pill: PillCreate):
    db_pill = PillDB(**pill.dict())
    db.add(db_pill)
    db.commit()
    db.refresh(db_pill)
    return db_pill


def get_pill(db: Session, pill_id: int):
    return db.query(PillDB).filter(PillDB.id == pill_id).first()


def get_pill_by_name(db: Session, name: str):
    return db.query(PillDB).filter(PillDB.name == name).first()


def get_pills(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PillDB).order_by(PillDB.id).offset(skip).limit(limit).all()


def update_pill(db: Session, pill_id: int, pill_update: PillUpdate):
    db_pill = db.query(PillDB).filter(PillDB.id == pill_id).first()
    if not db_pill:
        return None
    for var, value in vars(pill_update).items():
        if value is not None:
            setattr(db_pill, var, value)
    db.commit()
    db.refresh(db_pill)
    return db_pill


def delete_pill(db: Session, pill_id: int):
    db_pill = db.query(PillDB).filter(PillDB.id == pill_id).first()
    if not db_pill:
        return None
    db.delete(db_pill)
    db.commit()
    return db_pill
