from fastapi import APIrouter
from src.controllers.standings_controller import update_driver_standings, update_constructor_standings

driver_standings_router = APIRouter(prefix="/driver-standings")
constructor_standings_router = APIRouter(prefix="/constructor-standings")

