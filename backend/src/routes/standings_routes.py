from fastapi import APIRouter, HTTPException
from src.controllers import standings_controller

driver_standings_router = APIRouter(prefix="/driver-standings")
constructor_standings_router = APIRouter(prefix="/constructor-standings")

@driver_standings_router.get("/", tags=["standings"])
def get_driver_standings():
    try:
        return standings_controller.get_driver_standings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@constructor_standings_router.get("/", tags=["standings"])
def get_constructor_standings():
    try:
        return standings_controller.get_constructor_standings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))