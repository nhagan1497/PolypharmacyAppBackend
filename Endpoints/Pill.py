from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from base import get_db
from PIL import Image
import io

import Crud.Pill as PillCrud
import Schema.Pill as PillSchema
import Models.Pill as PillModel

from MachineVision.ImagePredict import identify_pill

import auth

pill_router = APIRouter()


@pill_router.post("/", response_model=PillSchema.Pill)
async def create_pill(
                    image: UploadFile,
                    pill: PillSchema.PillCreate = Depends(),
                    db: Session = Depends(get_db),
                    user_id=Depends(auth.get_uid)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    image_data = await image.read()
    try:
        # Optional: You can validate the image content here (e.g., using PIL)
        img = Image.open(io.BytesIO(image_data))
        img.verify()  # Ensure it's a valid image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")
    db_pill = PillCrud.get_pill_by_name(db, name=pill.name, user_id=user_id)
    if db_pill:
        raise HTTPException(status_code=400, detail="Pill with this name already exists")
    return PillCrud.create_pill(db=db, pill=pill, user_id=user_id)


@pill_router.get("/{pill_id}", response_model=PillSchema.Pill)
def read_pill(pill_id: int, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill = PillCrud.get_pill(db=db, pill_id=pill_id, user_id=user_id)
    if db_pill is None:
        raise HTTPException(status_code=404, detail="Pill not found")
    return db_pill


@pill_router.get("/", response_model=list[PillSchema.Pill])
def read_pills(skip: int = None, limit: int = None, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    pills = PillCrud.get_pills(db=db, skip=skip, limit=limit, user_id=user_id)
    return pills


@pill_router.put("/{pill_id}", response_model=PillSchema.Pill)
def update_pill(pill_id: int, pill_update: PillSchema.PillUpdate, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill = PillCrud.update_pill(db=db, pill_id=pill_id, pill_update=pill_update, user_id=user_id)
    if db_pill is None:
        raise HTTPException(status_code=404, detail="Pill not found")
    return db_pill


@pill_router.delete("/{pill_id}", response_model=PillSchema.Pill)
def delete_pill(pill_id: int, db: Session = Depends(get_db), user_id=Depends(auth.get_uid)):
    db_pill = PillCrud.delete_pill(db=db, pill_id=pill_id, user_id=user_id)
    if db_pill is None:
        raise HTTPException(status_code=404, detail="Pill not found")
    return db_pill


@pill_router.post('/identify/', response_model=PillSchema.Pill)
async def identify_pill_image(image: UploadFile, db=Depends(get_db), user_id=Depends(auth.get_uid)):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")
    image_data = await image.read()
    try:
        # Optional: You can validate the image content here (e.g., using PIL)
        img = Image.open(io.BytesIO(image_data))
        img.verify()  # Ensure it's a valid image
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file")

    return identify_pill(db, user_id, img)
