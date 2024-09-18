from fastapi import FastAPI
from fastapi import Depends

import auth

from Endpoints import Pill
from Endpoints import PillConsumption
from Endpoints import PillSchedule
from Endpoints import User

app = FastAPI()
app.include_router(Pill.pill_router, prefix="/pills", tags=["pills"])
app.include_router(PillConsumption.pill_consumption_router, prefix="/pill_consumption", tags=["pill_consumption"])
app.include_router(PillSchedule.pill_schedule_router, prefix="/pill_schedule", tags=["pill_schedule"])
app.include_router(User.user_router, prefix="/users", tags=["users"])


@app.get('/example/')
def return_uid(user_id: str = Depends(auth.get_uid)):
    return {"uid": user_id}
