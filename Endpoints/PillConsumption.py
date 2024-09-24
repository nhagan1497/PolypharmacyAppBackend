from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from base import get_db

import auth

import Crud.PillConsumption as PillConsumptionCrud
import Schema.PillConsumption as PillConsumptionSchema
import Models.PillConsumption as PillConsumptionModel

import Schema.Pill as PillSchema

pill_consumption_router = APIRouter()


@pill_consumption_router.post("/", response_model=PillConsumptionSchema.PillConsumption)
def create_pill_consumption(pill_consumption: PillConsumptionSchema.PillConsumptionCreate, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    return PillConsumptionCrud.create_pill_consumption(db=db, pill_consumption=pill_consumption, user_id=user_id)


@pill_consumption_router.get("/{pill_consumption_id}", response_model=PillConsumptionSchema.PillConsumption)
def read_pill_consumption(pill_consumption_id: int, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_consumption = PillConsumptionCrud.get_pill_consumption(db=db, pill_consumption_id=pill_consumption_id, user_id=user_id)
    if db_pill_consumption is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")
    return db_pill_consumption


@pill_consumption_router.get("/", response_model=list[PillConsumptionSchema.PillConsumption])
def read_pill_consumptions(skip: int = None, limit: int = None, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    pill_consumptions = PillConsumptionCrud.get_pill_consumptions(db=db, skip=skip, limit=limit, user_id=user_id)
    return pill_consumptions


@pill_consumption_router.put("/{pill_consumption_id}", response_model=PillConsumptionSchema.PillConsumption)
def update_pill_consumption(pill_consumption_id: int, pill_consumption_update: PillConsumptionSchema.PillConsumptionUpdate, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_consumption = PillConsumptionCrud.update_pill_consumption(db=db, pill_consumption_id=pill_consumption_id, pill_consumption_update=pill_consumption_update, user_id=user_id)
    if db_pill_consumption is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")
    return db_pill_consumption


@pill_consumption_router.delete("/{pill_consumption_id}", response_model=PillConsumptionSchema.PillConsumption)
def delete_pill_consumption(pill_consumption_id: int, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_consumption = PillConsumptionCrud.delete_pill_consumption(db=db, pill_consumption_id=pill_consumption_id, user_id=user_id)
    if db_pill_consumption is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")
    return db_pill_consumption


@pill_consumption_router.get("/pill_consumption_details/", response_model=list[tuple[PillConsumptionSchema.PillConsumption, PillSchema.Pill]])
def read_pill_consumption_details(db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill_consumption_details = PillConsumptionCrud.get_pill_consumption_details(db=db, user_id=user_id)
    if db_pill_consumption_details is None:
        raise HTTPException(status_code=404, detail="Pill consumption not found")

    return [(consumption, pill) for consumption, pill in db_pill_consumption_details]