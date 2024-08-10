from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

import Crud.PillConsumption as PillConsumptionCrud
import Schema.PillConsumption as PillConsumptionSchema
import Models.PillConsumption as PillConsumptionModel

pill_consumption_router = APIRouter()


@pill_consumption_router.post("/", response_model=PillConsumptionSchema.PillConsumption)
def create_pill_consumption(pill_consumption: PillConsumptionSchema.PillConsumptionCreate, db: Session = Depends(get_db)):
    return PillConsumptionCrud.create_pill_consumption(db=db, pill_consumption=pill_consumption)


@pill_consumption_router.get("/{pill_consumption_id}", response_model=PillConsumptionSchema.PillConsumption)
def read_pill_consumption(pill_consumption_id: int, db: Session = Depends(get_db)):
    db_pill_consumption = PillConsumptionCrud.get_pill_consumption(db=db, pill_consumption_id=pill_consumption_id)
    if db_pill_consumption is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")
    return db_pill_consumption


@pill_consumption_router.get("/", response_model=list[PillConsumptionSchema.PillConsumption])
def read_pill_consumptions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pill_consumptions = PillConsumptionCrud.get_pill_consumptions(db=db, skip=skip, limit=limit)
    return pill_consumptions


@pill_consumption_router.put("/{pill_consumption_id}", response_model=PillConsumptionSchema.PillConsumption)
def update_pill_consumption(pill_consumption_id: int, pill_consumption_update: PillConsumptionSchema.PillConsumptionUpdate, db: Session = Depends(get_db)):
    db_pill_consumption = PillConsumptionCrud.update_pill_consumption(db=db, pill_consumption_id=pill_consumption_id, pill_consumption_update=pill_consumption_update)
    if db_pill_consumption is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")
    return db_pill_consumption


@pill_consumption_router.delete("/{pill_consumption_id}", response_model=PillConsumptionSchema.PillConsumption)
def delete_pill_consumption(pill_consumption_id: int, db: Session = Depends(get_db)):
    db_pill_consumption = PillConsumptionCrud.delete_pill_consumption(db=db, pill_consumption_id=pill_consumption_id)
    if db_pill_consumption is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")
    return db_pill_consumption