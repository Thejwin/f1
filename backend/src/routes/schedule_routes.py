from fastapi import APIRouter, HTTPException, Query
from src.controllers import schedule_controller
import datetime 

schedule_router = APIRouter(prefix="/schedule")

@schedule_router.get("/", tags=["schedule"])
def get_schedule(year: int = Query(default=datetime.datetime.now().year, description="test")):
    try:
        return schedule_controller.get_schedules(year)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))