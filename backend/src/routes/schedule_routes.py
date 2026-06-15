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

@schedule_router.get("/{year}/{round_number}", tags=["schedule"])
def get_event_sessions(year: int, round_number: int):
    try:
        return schedule_controller.get_event_sessions(year, round_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@schedule_router.get("/{year}/{round_number}/{session_id}/results", tags=["schedule"])
def get_session_results(year: int, round_number: int, session_id: str):
    try:
        return schedule_controller.get_session_results(year, round_number, session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))