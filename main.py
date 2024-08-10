from cachetools import TTLCache, cached
from fastapi import Depends, FastAPI, Header, HTTPException, status
from firebase_admin import auth

import firebase_setup

from fastapi import APIRouter, Depends, HTTPException

from Endpoints import Pill
from Endpoints import PillConsumption
from Endpoints import PillSchedule
from Endpoints import User

app = FastAPI()
app.include_router(Pill.pill_router, prefix="/pills", tags=["pills"])
app.include_router(PillConsumption.pill_consumption_router, prefix="/pill_consumption", tags=["pill_consumption"])
app.include_router(PillSchedule.pill_schedule_router, prefix="/pill_schedule", tags=["pill_schedule"])
app.include_router(User.user_router, prefix="/users", tags=["users"])

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

