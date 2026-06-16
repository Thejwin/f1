import datetime
import json
from typing import Optional, List, Dict

import pandas as pd
import fastf1
from fastf1.ergast import Ergast
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert as pg_insert

from src.utils.db import LocalSession
from src.models.standings_models import DriverStanding, ConstructorStanding
from src.models.schedules_model import Schedule

def _get_last_refresh(session) -> Optional[datetime.datetime]:
    res = session.query(func.max(DriverStanding.updated_at)).scalar()
    if res and res.tzinfo is None:
        res = res.replace(tzinfo=datetime.timezone.utc)
    return res

def _get_last_completed_race_datetime(year: int) -> Optional[datetime.datetime]:
    with LocalSession() as session:
        events = session.query(Schedule).filter_by(year=year).all()

    if not events:
        return None

    now = datetime.datetime.now(datetime.timezone.utc)
    last_dt = None

    date_attrs = [
        "Session1DateUtc", "Session2DateUtc", "Session3DateUtc",
        "Session4DateUtc", "Session5DateUtc", "EventDate",
    ]

    for event in events:
        for attr in date_attrs:
            dt = getattr(event, attr, None)
            if dt is None:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            if dt <= now and (last_dt is None or dt > last_dt):
                last_dt = dt

    return last_dt

def _standing_row_to_dict(row, kind: str) -> Dict:
    result = {
        'points_earned': float(row.points or 0),
        'updated_at': row.updated_at.isoformat() if row.updated_at else None,
        'wins': int(row.wins or 0)
    }
    if kind == 'driver':
        result['driver_id'] = getattr(row, 'driverId', None)
        
        # Safe: The string formatting handles fallback gracefully, so .title() is safe here
        result['full_name'] = f"{getattr(row, 'givenName', '')} {getattr(row, 'familyName', '')}".strip().title()
        
        names_list = getattr(row, 'constructorNames', None)
        if isinstance(names_list, str):
            try:
                names_list = json.loads(names_list)
            except Exception:
                names_list = None
        
        # Safe: Check that the index exists and is a string before running .title()
        team = names_list[-1] if (names_list and isinstance(names_list, list) and len(names_list) > 0) else None
        result['team_name'] = team.title() if isinstance(team, str) else None
        
        result['driver_code'] = getattr(row, 'driverCode', None)
        result['driver_number'] = getattr(row, 'driverNumber', None)

    elif kind == 'constructor':
        # Safe: Pull the name first and check that it isn't None
        c_name = getattr(row, 'constructorName', None)
        result['team_name'] = c_name.title() if isinstance(c_name, str) else None
    
    return result


def recompute_and_store(year: int) -> Dict[str, List[Dict]]:
    ergast = Ergast()
    driver_standings = ergast.get_driver_standings(season=year).content[0]
    constructor_standings = ergast.get_constructor_standings(season=year).content[0]

    now = datetime.datetime.now(datetime.UTC)
    driver_standings["updated_at"] = now
    constructor_standings["updated_at"] = now

    with LocalSession() as session:
        for _, r in driver_standings.iterrows():
            # pandas NaN values to None for nullable columns
            driver_num = int(r["driverNumber"]) if pd.notna(r["driverNumber"]) else None
            driver_code = str(r["driverCode"]) if pd.notna(r["driverCode"]) else None
            dob = str(r["dateOfBirth"]) if pd.notna(r["dateOfBirth"]) else None
            driver_nat = str(r["driverNationality"]) if pd.notna(r["driverNationality"]) else None

            # Handle JSON fields safely (serialize lists/dicts into text strings)
            c_ids = r["constructorIds"] if isinstance(r["constructorIds"], (str, bytes)) else json.dumps(r["constructorIds"])
            c_names = r["constructorNames"] if isinstance(r["constructorNames"], (str, bytes)) else json.dumps(r["constructorNames"])
            c_nats = r["constructorNationalities"] if isinstance(r["constructorNationalities"], (str, bytes)) else json.dumps(r["constructorNationalities"])

            driver_payload = {
                "driverId": str(r["driverId"]),
                "position": int(r["position"]),
                "positionText": str(r["positionText"]),
                "points": float(r["points"]),
                "wins": int(r["wins"]),
                "driverNumber": driver_num,
                "driverCode": driver_code,
                "givenName": str(r["givenName"]),
                "familyName": str(r["familyName"]),
                "dateOfBirth": dob,
                "driverNationality": driver_nat,
                "constructorIds": c_ids,
                "constructorNames": c_names,
                "constructorNationalities": c_nats,
                "updated_at": r["updated_at"]
            }

            # PostgreSQL Upsert: INSERT ... ON CONFLICT DO UPDATE
            stmt = pg_insert(DriverStanding).values(**driver_payload)
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=["driverId"],
                # Dynamically set all incoming values to overwrite existing rows on conflict
                set_={k: v for k, v in driver_payload.items() if k != "driverId"}
            )
            session.execute(upsert_stmt)

        for _, r in constructor_standings.iterrows():
            const_nat = str(r["constructorNationality"]) if pd.notna(r["constructorNationality"]) else None

            constructor_payload = {
                "constructorId": str(r["constructorId"]),
                "position": int(r["position"]),
                "positionText": str(r["positionText"]),
                "points": float(r["points"]),
                "wins": int(r["wins"]),
                "constructorName": str(r["constructorName"]),
                "constructorNationality": const_nat,
                "updated_at": r["updated_at"]
            }

            # PostgreSQL Upsert: INSERT ... ON CONFLICT DO UPDATE
            stmt = pg_insert(ConstructorStanding).values(**constructor_payload)
            upsert_stmt = stmt.on_conflict_do_update(
                index_elements=["constructorId"],
                set_={k: v for k, v in constructor_payload.items() if k != "constructorId"}
            )
            session.execute(upsert_stmt)

        session.commit()

        drivers = session.query(DriverStanding).all()
        constructors = session.query(ConstructorStanding).all()
        return {
            'drivers': [_standing_row_to_dict(d, 'driver') for d in drivers],
            'constructors': [_standing_row_to_dict(c, 'constructor') for c in constructors],
        }
        

def get_standings(kind: str = 'driver') -> Dict[str, List[Dict]]:
    year = datetime.datetime.now(datetime.UTC).year

    with LocalSession() as session:
        last_refresh = _get_last_refresh(session)
    
    try:
        last_race_dt = _get_last_completed_race_datetime(year)
    except Exception:
        last_race_dt = None
    
    if last_refresh and last_race_dt and last_refresh >= last_race_dt:
        with LocalSession() as session:
            if kind == 'driver':
                rows = session.query(DriverStanding).all()
                return {'drivers': [_standing_row_to_dict(r, 'driver') for r in rows]}
            rows = session.query(ConstructorStanding).all()
            return {'constructors': [_standing_row_to_dict(r, 'constructor') for r in rows]}
        
    result = recompute_and_store(year)
    if kind == 'driver':
        return {'drivers': result['drivers']}
    return {'constructors': result['constructors']}
    
