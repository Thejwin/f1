from sqlalchemy import Column, Integer, String, Boolean, Float, Date, ForeignKey, DateTime
from datetime import datetime
from src.utils.db import Base

class DriverStanding(Base):
    __tablename__ = "driver_standings"

    driver_id = Column("driver_id", String, primary_key=True)
    full_name = Column("full_name", String, nullable=False)
    team_name = Column("team_name", String, nullable=False)
    points_earned = Column("points_earned", Float, nullable=False)
    pos_1 = Column("pos_1", Integer, nullable=False, default=0)
    pos_2 = Column("pos_2", Integer, nullable=False, default=0)
    pos_3 = Column("pos_3", Integer, nullable=False, default=0)
    pos_4 = Column("pos_4", Integer, nullable=False, default=0)
    pos_5 = Column("pos_5", Integer, nullable=False, default=0)
    pos_6 = Column("pos_6", Integer, nullable=False, default=0)
    pos_7 = Column("pos_7", Integer, nullable=False, default=0)
    pos_8 = Column("pos_8", Integer, nullable=False, default=0)
    pos_9 = Column("pos_9", Integer, nullable=False, default=0)
    pos_10 = Column("pos_10", Integer, nullable=False, default=0)
    pos_11 = Column("pos_11", Integer, nullable=False, default=0)
    pos_12 = Column("pos_12", Integer, nullable=False, default=0)
    pos_13 = Column("pos_13", Integer, nullable=False, default=0)
    pos_14 = Column("pos_14", Integer, nullable=False, default=0)
    pos_15 = Column("pos_15", Integer, nullable=False, default=0)
    pos_16 = Column("pos_16", Integer, nullable=False, default=0)
    pos_17 = Column("pos_17", Integer, nullable=False, default=0)
    pos_18 = Column("pos_18", Integer, nullable=False, default=0)
    pos_19 = Column("pos_19", Integer, nullable=False, default=0)
    pos_20 = Column("pos_20", Integer, nullable=False, default=0)
    pos_21 = Column("pos_21", Integer, nullable=False, default=0)
    pos_22 = Column("pos_22", Integer, nullable=False, default=0)
    
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


class ConstructorStanding(Base):
    __tablename__ = "constructor_standings"

    team_name = Column("team_name", String, primary_key=True)
    points_earned = Column("points_earned", Float, nullable=False)
    pos_1 = Column("pos_1", Integer, nullable=False, default=0)
    pos_2 = Column("pos_2", Integer, nullable=False, default=0)
    pos_3 = Column("pos_3", Integer, nullable=False, default=0)
    pos_4 = Column("pos_4", Integer, nullable=False, default=0)
    pos_5 = Column("pos_5", Integer, nullable=False, default=0)
    pos_6 = Column("pos_6", Integer, nullable=False, default=0)
    pos_7 = Column("pos_7", Integer, nullable=False, default=0)
    pos_8 = Column("pos_8", Integer, nullable=False, default=0)
    pos_9 = Column("pos_9", Integer, nullable=False, default=0)
    pos_10 = Column("pos_10", Integer, nullable=False, default=0)
    pos_11 = Column("pos_11", Integer, nullable=False, default=0)
    pos_12 = Column("pos_12", Integer, nullable=False, default=0)
    pos_13 = Column("pos_13", Integer, nullable=False, default=0)
    pos_14 = Column("pos_14", Integer, nullable=False, default=0)
    pos_15 = Column("pos_15", Integer, nullable=False, default=0)
    pos_16 = Column("pos_16", Integer, nullable=False, default=0)
    pos_17 = Column("pos_17", Integer, nullable=False, default=0)
    pos_18 = Column("pos_18", Integer, nullable=False, default=0)
    pos_19 = Column("pos_19", Integer, nullable=False, default=0)
    pos_20 = Column("pos_20", Integer, nullable=False, default=0)
    pos_21 = Column("pos_21", Integer, nullable=False, default=0)
    pos_22 = Column("pos_22", Integer, nullable=False, default=0)

    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


#DriverId,FullName,TeamName,PointsEarned,pos_1,pos_2,pos_3,pos_4,pos_5,pos_6,pos_7,pos_8,pos_9,pos_10,pos_11,pos_12,pos_13,pos_14,pos_15,pos_16,pos_17,pos_18,pos_19,pos_20,pos_21,pos_22