from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

import Crud.Pill as PillCrud
import Schema.Pill as PillSchema
import Models.Pill as PillModel

pill_router = APIRouter()


@pill_router.post("/", response_model=PillSchema.Pill)
def create_pill(pill: PillSchema.PillCreate, db: Session = Depends(get_db)):
    db_pill = PillCrud.get_pill_by_name(db, name=pill.name)
    if db_pill:
        raise HTTPException(status_code=400, detail="Pill with this name already exists")
    return PillCrud.create_pill(db=db, pill=pill)


@pill_router.get("/{pill_id}", response_model=PillSchema.Pill)
def read_pill(pill_id: int, db: Session = Depends(get_db)):
    db_pill = PillCrud.get_pill(db=db, pill_id=pill_id)
    if db_pill is None:
        raise HTTPException(status_code=404, detail="Pill not found")
    return db_pill


@pill_router.get("/", response_model=list[PillSchema.Pill])
def read_pills(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pills = PillCrud.get_pills(db=db, skip=skip, limit=limit)
    return pills


@pill_router.put("/{pill_id}", response_model=PillSchema.Pill)
def update_pill(pill_id: int, pill_update: PillSchema.PillUpdate, db: Session = Depends(get_db)):
    db_pill = PillCrud.update_pill(db=db, pill_id=pill_id, pill_update=pill_update)
    if db_pill is None:
        raise HTTPException(status_code=404, detail="Pill not found")
    return db_pill


@pill_router.delete("/{pill_id}", response_model=PillSchema.Pill)
def delete_pill(pill_id: int, db: Session = Depends(get_db)):
    db_pill = PillCrud.delete_pill(db=db, pill_id=pill_id)
    if db_pill is None:
        raise HTTPException(status_code=404, detail="Pill not found")
    return db_pill
