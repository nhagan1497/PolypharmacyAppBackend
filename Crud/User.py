from sqlalchemy.orm import Session
from Models.User import User as UserDB
from Schema.User import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate):
    db_user = UserDB(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(UserDB).filter(UserDB.uid == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(UserDB).order_by(UserDB.uid).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate):
    db_user = db.query(UserDB).filter(UserDB.uid == user_id).first()
    if not db_user:
        return None
    for var, value in vars(user_update).items():
        if value is not None:
            setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(UserDB).filter(UserDB.uid == user_id).first()
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user
