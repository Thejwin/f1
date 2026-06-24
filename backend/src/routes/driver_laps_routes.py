from fastapi import APIRouter, HTTPException
from src.controllers import driver_laps_controller

driver_laps_router = APIRouter(prefix="/laps")

@driver_laps_router.get("/{year}/{round_number}", tags=["laps"])
def get_race_laps(year: int, round_number: int):
    try:
        return driver_laps_controller.get_race_laps(year, round_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))