from sqlalchemy import Column, Integer, String, Float, ForeignKey
from src.utils.db import Base

class SessionResult(Base):
    __tablename__ = "session_results"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Link back to the Schedule model
    year = Column(Integer, nullable=False)
    round_number = Column(Integer, nullable=False)
    
    # E.g., 'R', 'FP1', 'Q', 'S', 'SQ'
    session_identifier = Column(String, nullable=False) 
    
    # Driver Info
    driver_number = Column(String, nullable=True) # e.g., '1' for Verstappen
    driver_abbreviation = Column(String, nullable=True) # e.g., 'VER'
    team_name = Column(String, nullable=True)
    
    # Results
    position = Column(Integer, nullable=True)
    grid_position = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    status = Column(String, nullable=True) # e.g., 'Finished', '+1 Lap', 'Accident'
    time = Column(String, nullable=True) # Final race time or difference
    
    # Qualifying times (nullable for race)
    q1_time = Column(String, nullable=True)
    q2_time = Column(String, nullable=True)
    q3_time = Column(String, nullable=True)
