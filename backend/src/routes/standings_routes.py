from fastapi import APIRouter, HTTPException, Request
from src.controllers import standings_controller
from src.utils.rate_limiter import limiter

driver_standings_router = APIRouter(prefix="/driver-standings")
constructor_standings_router = APIRouter(prefix="/constructor-standings")

@driver_standings_router.get("/", tags=["standings"])
@limiter.limit("60/minute")
def get_driver_standings(request: Request):
    try:
        return standings_controller.get_driver_standings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@constructor_standings_router.get("/", tags=["standings"])
@limiter.limit("60/minute")
def get_constructor_standings(request: Request):
    try:
        return standings_controller.get_constructor_standings()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))