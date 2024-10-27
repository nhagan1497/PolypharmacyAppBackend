from fastapi import FastAPI, BackgroundTasks
from fastapi import Depends
# from apscheduler.schedulers.background import BackgroundScheduler

import auth

from Endpoints import Pill
from Endpoints import PillConsumption
from Endpoints import PillSchedule
from Endpoints import User

from base import initialize_database, db_heartbeat_task

app = FastAPI()

# scheduler = BackgroundScheduler()
# scheduler.add_job(db_heartbeat_task, 'interval', minutes=10)


@app.on_event("startup")
async def startup_event():
    initialize_database()
    # scheduler.start()


app.include_router(Pill.pill_router, prefix="/pills", tags=["pills"])
app.include_router(PillConsumption.pill_consumption_router, prefix="/pill_consumption", tags=["pill_consumption"])
app.include_router(PillSchedule.pill_schedule_router, prefix="/pill_schedule", tags=["pill_schedule"])
app.include_router(User.user_router, prefix="/users", tags=["users"])


@app.get('/example/')
def return_uid(user_id: str = Depends(auth.get_uid)):
    return {"uid": user_id}
