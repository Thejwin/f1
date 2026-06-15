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
    broadcast_name = Column(String, nullable=True)
    driver_abbreviation = Column(String, nullable=True) # e.g., 'VER'
    driver_id = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    full_name = Column(String, nullable=True)
    headshot_url = Column(String, nullable=True)
    country_code = Column(String, nullable=True)
    
    # Team Info
    team_name = Column(String, nullable=True)
    team_color = Column(String, nullable=True)
    team_id = Column(String, nullable=True)
    
    # Results
    position = Column(Integer, nullable=True)
    classified_position = Column(String, nullable=True)
    grid_position = Column(Integer, nullable=True)
    points = Column(Float, nullable=True)
    status = Column(String, nullable=True) # e.g., 'Finished', '+1 Lap', 'Accident'
    time = Column(String, nullable=True) # Final race time or difference
    laps = Column(Integer, nullable=True)
    
    # Qualifying times (nullable for race)
    q1_time = Column(String, nullable=True)
    q2_time = Column(String, nullable=True)
    q3_time = Column(String, nullable=True)
