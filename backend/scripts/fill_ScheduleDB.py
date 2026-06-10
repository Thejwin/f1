from src.utils.db import LocalSession
from src.models.schedules_model import Schedule
import fastf1
import datetime
import pandas as pd

startyr = 1950
endyr = datetime.datetime.now().year

def clean_row_data(row_dict):
    """Replaces NaT and NaN values with None for database compatibility"""
    cleaned = {}
    for key, val in row_dict.items():
        # Check if the value is NaT or NaN
        if pd.isna(val) or val is pd.NaT:
            cleaned[key] = None
        else:
            cleaned[key] = val
    return cleaned

def fill_schedule_db():
    for yr in range(startyr, endyr + 1):
        schedule = fastf1.get_event_schedule(yr)
        with LocalSession() as session:
            #fill schedule db with events
            for _, r in schedule.iterrows():
                row = clean_row_data(r.to_dict())

                exists = session.query(Schedule).filter_by(
                    year=yr, 
                    RoundNumber=row["RoundNumber"]
                ).first()
                
                if exists:
                    # Skip to the next race if this one is already in the database
                    continue

                s = Schedule(
                    year = yr,
                    RoundNumber = row["RoundNumber"],
                    Country = row["Country"],
                    Location = row["Location"],
                    OfficialEventName = row["OfficialEventName"],
                    EventDate = row["EventDate"],
                    EventName = row["EventName"],
                    EventFormat = row["EventFormat"],

                    Session1 = row["Session1"],
                    Session1Date = row["Session1Date"],
                    Session1DateUtc = row["Session1DateUtc"],

                    Session2 = row["Session2"],
                    Session2Date = row["Session2Date"],
                    Session2DateUtc = row["Session2DateUtc"],

                    Session3 = row["Session3"],
                    Session3Date = row["Session3Date"],
                    Session3DateUtc = row["Session3DateUtc"],

                    Session4 = row["Session4"],
                    Session4Date = row["Session4Date"],
                    Session4DateUtc = row["Session4DateUtc"],
                    Session5 = row["Session5"],
                    Session5Date = row["Session5Date"],
                    Session5DateUtc = row["Session5DateUtc"],

                    F1ApiSupport = row["F1ApiSupport"]

                )
                session.add(s)
                session.commit()


if __name__ == "__main__":
    fill_schedule_db()
    