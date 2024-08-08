from fastapi import FastAPI, Depends, HTTPException, status
from firebase_admin import auth

import firebase_setup

app = FastAPI()


def verify_token(auth_header: str):
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header",
        )
    id_token = auth_header.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


@app.get("/secure-data")
async def secure_data(user_data: dict = Depends(verify_token)):
    return {"message": "This is secured data", "user_id": user_data["uid"]}


@app.get("/")
async def root():
    return {"message": "Hello World"}
