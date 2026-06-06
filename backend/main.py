from fastapi import FastAPI
from src.utils.db import Base, engine
from src.models.standings_models import DriverStanding, ConstructorStanding
from src.routes.standings_routes import driver_standings_router, constructor_standings_router

Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(driver_standings_router)
app.include_router(constructor_standings_router)