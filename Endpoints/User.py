from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

import Crud.User as UserCrud
import Schema.User as UserSchema
import Models.User as UserModel

user_router = APIRouter()


@user_router.post("/", response_model=UserSchema.User)
def create_user(user: UserSchema.UserCreate, db: Session = Depends(get_db)):
    return UserCrud.create_user(db=db, user=user)


@user_router.get("/{user_id}", response_model=UserSchema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserCrud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.get("/", response_model=list[UserSchema.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = UserCrud.get_users(db=db, skip=skip, limit=limit)
    return users


@user_router.put("/{user_id}", response_model=UserSchema.User)
def update_user(user_id: int, user_update: UserSchema.UserUpdate, db: Session = Depends(get_db)):
    db_user = UserCrud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.delete("/{user_id}", response_model=UserSchema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserCrud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user