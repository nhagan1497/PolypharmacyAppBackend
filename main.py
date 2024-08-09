import time
from cachetools import TTLCache, cached
from fastapi import Depends, FastAPI, Header, HTTPException, status
from firebase_admin import auth

import firebase_setup

app = FastAPI()

token_cache = TTLCache(maxsize=1000, ttl=3600)


@cached(cache=token_cache)
def verify_token_cached(id_token: str):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_token(auth_header: str = Header(None)):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header",
        )
    id_token = auth_header.split("Bearer ")[1]
    return verify_token_cached(id_token)


@app.get("/secure-data")
async def secure_data(user_data: dict = Depends(verify_token)):
    return {"message": "This is secured data", "user_id": user_data["uid"]}


@app.get("/")
async def root():
    return {"message": "Hello World"}


# User ID LOfI6oxL2pNmwAm9tJ1aFDgRw0w2
