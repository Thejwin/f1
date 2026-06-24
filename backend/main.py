from fastapi import FastAPI
from src.utils.db import Base, engine
from src.models import DriverStanding, ConstructorStanding, Schedule, SessionResult, DriverLaps
from src.routes import driver_standings_router, constructor_standings_router, schedule_router, driver_laps_router
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

app.include_router(driver_standings_router)
app.include_router(constructor_standings_router)
app.include_router(schedule_router)
app.include_router(driver_laps_router)
