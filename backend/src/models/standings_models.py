from sqlalchemy import Column, Integer, String, Boolean, Float, Date, JSON, DateTime
from datetime import datetime
from src.utils.db import Base

class DriverStanding(Base):
    __tablename__ = "driver_standings"

    driverId = Column(String, primary_key=True)
    position = Column(Integer, nullable=False)
    positionText = Column(String, nullable=False)
    points = Column(Float, nullable=False)
    wins = Column(Integer, nullable=False)
    driverNumber = Column(Integer, nullable=True)
    driverCode = Column(String, nullable=True)
    givenName = Column(String, nullable=False)
    familyName = Column(String, nullable=False)
    dateOfBirth = Column(String, nullable=True)
    driverNationality = Column(String, nullable=True)
    constructorIds = Column(JSON, nullable=False)
    constructorNames = Column(JSON, nullable=False)
    constructorNationalities = Column(JSON, nullable=True)
    
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class ConstructorStanding(Base):
    __tablename__ = "constructor_standings"

    constructorId = Column(String, primary_key=True)
    position = Column(Integer, nullable=False)
    positionText = Column(String, nullable=False)
    points = Column(Float, nullable=False)
    wins = Column(Integer, nullable=False)
    constructorName = Column(String, nullable=False)
    constructorNationality = Column(String, nullable=True)


    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

