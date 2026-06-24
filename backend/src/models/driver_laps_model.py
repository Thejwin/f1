from sqlalchemy import Column, Integer, String, Boolean, Index
from src.utils.db import Base


class DriverLaps(Base):
    __tablename__ = "driver_laps"

    # Composite index speeds up queries filtered by race + driver
    __table_args__ = (
        Index('ix_driver_laps_year_round_driver', 'year', 'round_number', 'driver_number'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    year = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)

    time = Column(String, nullable=True)
    driver = Column(String, nullable=True)
    driver_number = Column(String, nullable=True)
    lap_time = Column(String, nullable=True)
    lap_number = Column(Integer, nullable=True)
    stint = Column(Integer, nullable=True)
    pit_out_time = Column(String, nullable=True)
    pit_in_time = Column(String, nullable=True)
    sector1_time = Column(String, nullable=True)
    sector2_time = Column(String, nullable=True)
    sector3_time = Column(String, nullable=True)
    sector1_session_time = Column(String, nullable=True)
    sector2_session_time = Column(String, nullable=True)
    sector3_session_time = Column(String, nullable=True)
    speed_i1 = Column(String, nullable=True)
    speed_i2 = Column(String, nullable=True)
    speed_fl = Column(String, nullable=True)
    speed_st = Column(String, nullable=True)
    is_personal_best = Column(Boolean, nullable=True)
    compound = Column(String, nullable=True)
    tyre_life = Column(Integer, nullable=True)
    fresh_tyre = Column(Boolean, nullable=True)
    team = Column(String, nullable=True)
    lap_start_time = Column(String, nullable=True)
    lap_start_date = Column(String, nullable=True)
    track_status = Column(String, nullable=True)
    position = Column(Integer, nullable=True)
    deleted = Column(Boolean, nullable=True)
    deleted_reason = Column(String, nullable=True)
    fast_f1_generated = Column(Boolean, nullable=True)
    is_accurate = Column(Boolean, nullable=True)