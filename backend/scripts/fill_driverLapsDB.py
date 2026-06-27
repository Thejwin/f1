import time
import fastf1
import pandas as pd
from sqlalchemy.orm import Session
import os
import sys
from src.utils.db import LocalSession

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db import engine, Base
from src.models import DriverLaps, Schedule

os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

def fill_driver_laps(year):
    with LocalSession() as session:
        schedule = session.query(Schedule).filter_by(year=year).all()
        
        for event in schedule:
            if event.RoundNumber == 0:
                continue
            
            # Check if laps already exist to avoid duplicates
            existing_laps = session.query(DriverLaps).filter_by(year=year, round_number=event.RoundNumber).first()
            if existing_laps:
                print(f"Skipping {event.EventName} - Already in DB")
                continue

            try:
                print(f"Fetching {event.EventName} laps...")
                f1_session = fastf1.get_session(year, event.RoundNumber, "R")
                f1_session.load(telemetry=False, weather=False)
                laps_df = f1_session.laps
            except Exception as e:
                print(f"Error getting session for {event.EventName}: {e}")
                continue
                
            new_laps = []
            for lap in laps_df.itertuples():
                new_laps.append(DriverLaps(
                    year=year,
                    round_number=event.RoundNumber,
                    time=str(lap.Time) if pd.notna(lap.Time) else None,
                    driver=str(lap.Driver) if pd.notna(lap.Driver) else None,
                    driver_number=str(lap.DriverNumber) if pd.notna(lap.DriverNumber) else None,
                    lap_time=str(lap.LapTime) if pd.notna(lap.LapTime) else None,
                    lap_number=int(lap.LapNumber) if pd.notna(lap.LapNumber) else None,
                    stint=int(lap.Stint) if pd.notna(lap.Stint) else None,
                    pit_out_time=str(lap.PitOutTime) if pd.notna(lap.PitOutTime) else None,
                    pit_in_time=str(lap.PitInTime) if pd.notna(lap.PitInTime) else None,
                    sector1_time=str(lap.Sector1Time) if pd.notna(lap.Sector1Time) else None,
                    sector2_time=str(lap.Sector2Time) if pd.notna(lap.Sector2Time) else None,
                    sector3_time=str(lap.Sector3Time) if pd.notna(lap.Sector3Time) else None,
                    sector1_session_time=str(lap.Sector1SessionTime) if pd.notna(lap.Sector1SessionTime) else None,
                    sector2_session_time=str(lap.Sector2SessionTime) if pd.notna(lap.Sector2SessionTime) else None,
                    sector3_session_time=str(lap.Sector3SessionTime) if pd.notna(lap.Sector3SessionTime) else None,
                    speed_i1=str(lap.SpeedI1) if pd.notna(lap.SpeedI1) else None,
                    speed_i2=str(lap.SpeedI2) if pd.notna(lap.SpeedI2) else None,
                    speed_fl=str(lap.SpeedFL) if pd.notna(lap.SpeedFL) else None,
                    speed_st=str(lap.SpeedST) if pd.notna(lap.SpeedST) else None,
                    is_personal_best=bool(lap.IsPersonalBest) if pd.notna(lap.IsPersonalBest) else None,
                    compound=str(lap.Compound) if pd.notna(lap.Compound) else None,
                    tyre_life=int(lap.TyreLife) if pd.notna(lap.TyreLife) else None,
                    fresh_tyre=bool(lap.FreshTyre) if pd.notna(lap.FreshTyre) else None,
                    team=str(lap.Team) if pd.notna(lap.Team) else None,
                    lap_start_time=str(lap.LapStartTime) if pd.notna(lap.LapStartTime) else None,
                    lap_start_date=str(lap.LapStartDate) if pd.notna(lap.LapStartDate) else None,
                    track_status=str(lap.TrackStatus) if pd.notna(lap.TrackStatus) else None,
                    position=int(lap.Position) if pd.notna(lap.Position) else None,
                    deleted=bool(lap.Deleted) if pd.notna(lap.Deleted) else None,
                    deleted_reason=str(lap.DeletedReason) if pd.notna(lap.DeletedReason) else None,
                    fast_f1_generated=bool(lap.FastF1Generated) if pd.notna(lap.FastF1Generated) else None,
                    is_accurate=bool(lap.IsAccurate) if pd.notna(lap.IsAccurate) else None
                ))
                
            try:
                session.add_all(new_laps)
                session.commit()
                print(f"  Saved {len(new_laps)} laps.")
            except Exception as e:
                session.rollback()
                print(f"  Failed to save laps to DB: {e}")
                
            time.sleep(1) # respect API rate limits
        
if __name__ == "__main__":
    for yr in range(2019, 2027):
        fill_driver_laps(yr)
        time.sleep(30)