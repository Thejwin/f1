from sqlalchemy import Column, Integer, String, DateTime, Boolean
from src.utils.db import Base

class Schedule(Base):
    __tablename__ = "schedules"


    year = Column("year", Integer, primary_key=True)
    RoundNumber = Column("RoundNumber", Integer, primary_key=True)
    Country = Column("Country", String, nullable=True)
    Location = Column("Location", String, nullable=True)
    OfficialEventName = Column("OfficialEventName", String, nullable=True)
    EventDate = Column("EventDate", DateTime, nullable=True)
    EventName = Column("EventName", String, nullable=True)
    EventFormat = Column("EventFormat", String, nullable=True)

    Session1 = Column("Session1", String, nullable=True)
    Session1Date = Column("Session1Date", DateTime, nullable=True)
    Session1DateUtc = Column("Session1DateUtc", DateTime, nullable=True)

    Session2 = Column("Session2", String, nullable=True)
    Session2Date = Column("Session2Date", DateTime, nullable=True)
    Session2DateUtc = Column("Session2DateUtc", DateTime, nullable=True)

    Session3 = Column("Session3", String, nullable=True)
    Session3Date = Column("Session3Date", DateTime, nullable=True)
    Session3DateUtc = Column("Session3DateUtc", DateTime, nullable=True)

    Session4 = Column("Session4", String, nullable=True)
    Session4Date = Column("Session4Date", DateTime, nullable=True)
    Session4DateUtc = Column("Session4DateUtc", DateTime, nullable=True)

    Session5 = Column("Session5", String, nullable=True)
    Session5Date = Column("Session5Date", DateTime, nullable=True)
    Session5DateUtc = Column("Session5DateUtc", DateTime, nullable=True)

    F1ApiSupport = Column("F1ApiSupport", Boolean)
    
