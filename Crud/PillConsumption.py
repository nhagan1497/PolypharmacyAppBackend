from sqlalchemy.orm import Session
from Models.PillConsumption import PillConsumption as PillConsumptionDB
from Schema.PillConsumption import PillConsumptionCreate, PillConsumptionUpdate


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
    return (db.query(PillConsumptionDB).filter(PillConsumptionDB.user_id == user_id).
            order_by(PillConsumptionDB.id).offset(skip).limit(limit).all())


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
