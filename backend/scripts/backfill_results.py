
import time
import fastf1
import pandas as pd
from sqlalchemy.orm import Session
import os
import sys

# Add the parent directory to sys.path so we can import src modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.db import engine, Base
from src.models import SessionResult, Schedule

# Enable FastF1 Cache (saves downloaded data locally to speed up future runs)
# Create a cache directory if it doesn't exist
os.makedirs("cache", exist_ok=True)
fastf1.Cache.enable_cache("cache")

def backfill_results(start_year: int, end_year: int):
    # Ensure tables exist
    Base.metadata.create_all(engine)
    
    with Session(engine) as session_db:
        for year in range(start_year, end_year + 1):
            print(f"Fetching schedule for {year}...")
            try:
                schedule = fastf1.get_event_schedule(year)
            except Exception as e:
                print(f"Error fetching schedule for {year}: {e}")
                continue
                
            for index, event in schedule.iterrows():
                round_number = event['RoundNumber']
                if round_number == 0:
                    continue # Pre-season testing
                    
                print(f"  Processing Round {round_number} - {event['EventName']}")
                
                event_format = event['EventFormat']
                session_identifiers = ['R']
                
                if event_format == 'conventional':
                    session_identifiers.extend(['FP1', 'FP2', 'FP3', 'Q'])
                elif event_format == 'sprint':
                    # modern sprint format
                    session_identifiers.extend(['FP1', 'Q', 'SQ', 'S'])
                elif event_format == 'sprint_shootout': # 2023
                    session_identifiers.extend(['FP1', 'Q', 'SS', 'S'])
                elif event_format == 'sprint_qualifying': # 2021-2022
                    session_identifiers.extend(['FP1', 'FP2', 'Q', 'SQ'])
                else:
                    # Default fallback
                    session_identifiers.extend(['FP1', 'Q'])

                for session_id in session_identifiers:
                    # Check if we already have it in DB
                    existing = session_db.query(SessionResult).filter_by(
                        year=year, 
                        round_number=round_number, 
                        session_identifier=session_id
                    ).first()
                    
                    if existing:
                        print(f"    Skipping {session_id} - Already in DB")
                        continue
                        
                    print(f"    Fetching {session_id}...")
                    try:
                        f1_session = fastf1.get_session(year, round_number, session_id)
                        f1_session.load(telemetry=False, weather=False, messages=False) # Load only results
                        results = f1_session.results
                        
                        if results is None or results.empty:
                            print(f"      No results data available for {session_id}")
                            continue
                            
                        new_records = []
                        for _, row in results.iterrows():
                            # Safely extract values, handling NaNs
                            pos = int(row['Position']) if pd.notna(row['Position']) else None
                            grid = int(row['GridPosition']) if pd.notna(row['GridPosition']) else None
                            pts = float(row['Points']) if pd.notna(row['Points']) else 0.0
                            
                            time_str = str(row['Time']).split()[-1] if pd.notna(row['Time']) else None
                            q1 = str(row['Q1']).split()[-1] if 'Q1' in row and pd.notna(row['Q1']) else None
                            q2 = str(row['Q2']).split()[-1] if 'Q2' in row and pd.notna(row['Q2']) else None
                            q3 = str(row['Q3']).split()[-1] if 'Q3' in row and pd.notna(row['Q3']) else None
                            
                            result_record = SessionResult(
                                year=year,
                                round_number=round_number,
                                session_identifier=session_id,
                                driver_number=str(row['DriverNumber']),
                                driver_abbreviation=str(row['Abbreviation']),
                                team_name=str(row['TeamName']),
                                position=pos,
                                grid_position=grid,
                                points=pts,
                                status=str(row['Status']),
                                time=time_str,
                                q1_time=q1,
                                q2_time=q2,
                                q3_time=q3
                            )
                            new_records.append(result_record)
                        
                        session_db.add_all(new_records)
                        session_db.commit()
                        print(f"      Saved {len(new_records)} driver results for {session_id}")
                        
                    except Exception as e:
                        print(f"      Failed to process {session_id}: {e}")
                        session_db.rollback()
                        
                    # Sleep to respect rate limits
                    time.sleep(2)
                    
if __name__ == "__main__":
    backfill_results(2018, 2026)
    print("Done!")
