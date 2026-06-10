from fastapi import APIRouter, HTTPException, Query
from src.controllers import schedule_controller
import datetime 

schedule_router = APIRouter(prefix="/scedule")

@scheddule_router.get("/", tags=[schedule])
def get_schedule(year: int = Query(default=datetime.datetime.now().year)):
    try:
        return shedule_controller.get_schedule(year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))