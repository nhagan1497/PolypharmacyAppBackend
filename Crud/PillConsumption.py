from sqlalchemy.orm import Session
from sqlalchemy import func
from Models.PillConsumption import PillConsumption as PillConsumptionDB
from Schema.PillConsumption import PillConsumptionCreate, PillConsumptionUpdate
from Models.Pill import Pill as PillDB
from Schema.Pill import Pill

def create_pill_consumption(db: Session, pill_consumption: PillConsumptionCreate, user_id: str = None):
    db_pill_consumption = PillConsumptionDB(**pill_consumption.dict(), user_id=user_id)
    db.add(db_pill_consumption)
    db.commit()
    db.refresh(db_pill_consumption)
    return db_pill_consumption


def get_pill_consumption(db: Session, pill_consumption_id: int, user_id: str = None):
    return db.query(PillConsumptionDB).filter(
        PillConsumptionDB.id == pill_consumption_id,
        PillConsumptionDB.user_id == user_id
    ).first()


def get_pill_consumptions(db: Session, skip: int = 0, limit: int = 10, user_id: str = None):
    query_result = db.query(PillConsumptionDB).filter(PillConsumptionDB.user_id == user_id)
    if skip and limit:
        query_result = query_result.order_by(PillConsumptionDB.id).offset(skip).limit(limit)
    return query_result.all()


def get_pill_consumption_details(db: Session, user_id: str):
    return (db.query(PillConsumptionDB, PillDB)
            .join(PillDB, PillConsumptionDB.pill_id == PillDB.id)  # Adjust the field names accordingly
            .filter(PillConsumptionDB.user_id == user_id)
            .order_by(PillConsumptionDB.id)
            .all())


def update_pill_consumption(db: Session, pill_consumption_id: int, pill_consumption_update: PillConsumptionUpdate, user_id: str = None):
    db_pill_consumption = db.query(PillConsumptionDB).filter(
        PillConsumptionDB.id == pill_consumption_id,
        PillConsumptionDB.user_id == user_id
    ).first()
    if not db_pill_consumption:
        return None
    for var, value in vars(pill_consumption_update).items():
        if value is not None:
            setattr(db_pill_consumption, var, value)
    db.commit()
    db.refresh(db_pill_consumption)
    return db_pill_consumption


def delete_pill_consumption(db: Session, pill_consumption_id: int, user_id: str = None):
    db_pill_consumption = db.query(PillConsumptionDB).filter(
        PillConsumptionDB.id == pill_consumption_id,
        PillConsumptionDB.user_id == user_id
    ).first()
    if not db_pill_consumption:
        return None
    db.delete(db_pill_consumption)
    db.commit()
    return db_pill_consumption


def get_remaining_pill_count(db: Session, pill_id: int, user_id: str):
    total_count = db.query(func.sum(PillConsumptionDB.quantity)).filter(
        PillConsumptionDB.user_id == user_id, PillConsumptionDB.pill_id == pill_id
    ).scalar()
    return total_count * -1
