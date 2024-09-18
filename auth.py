from cachetools import TTLCache, cached
from fastapi import HTTPException
from fastapi import Header, status
import firebase_admin
from firebase_admin import credentials, auth
import os
import json

token_cache = TTLCache(maxsize=1000, ttl=3600)

cred = credentials.Certificate(json.loads(os.environ['FIREBASE_SERVICE_CRED']))
firebase_admin.initialize_app(cred)


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


def get_uid(auth_header: str = Header(None)):
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication header",
        )
    id_token = auth_header.split("Bearer ")[1]
    return verify_token_cached(id_token).get('uid')
