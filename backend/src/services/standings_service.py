import datetime
from typing import Optional, List, Dict

import pandas as pd
import fastf1
from sqlalchemy import func

from src.utils.db import LocalSession
from src.models.standings_models import DriverStanding, ConstructorStanding

# reuse existing build_standings function from backend/standings.py
try:
    import src.services.standings as local_standings
except Exception:
    local_standings = None


def _get_last_refresh(session) -> Optional[datetime.datetime]:
    res = session.query(func.max(DriverStanding.updated_at)).scalar()
    return res


def _normalize_datetime(dt: Optional[datetime.datetime]) -> Optional[datetime.datetime]:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    return dt


def _get_last_completed_race_datetime(year: int) -> Optional[datetime.datetime]:
    schedule = fastf1.get_event_schedule(year)
    date_cols = [c for c in schedule.columns if 'date' in c.lower()]
    if not date_cols:
        return None
    
    """ switch db for schedules. 
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    """

    now = pd.Timestamp.utcnow()
    last_dt = None
    for col in date_cols:
        try:
            col_dt = pd.to_datetime(schedule[col], utc=True)
        except Exception:
            continue
        past_events = col_dt[col_dt <= now]
        if past_events.empty:
            continue
        this_max = past_events.max()
        if pd.isna(this_max):
            continue
        this_max = this_max.to_pydatetime()
        if last_dt is None or this_max > last_dt:
            last_dt = this_max
    return _normalize_datetime(last_dt)


def _standing_row_to_dict(row, kind: str) -> Dict:
    result = {
        'team_name': getattr(row, 'team_name', None),
        'points_earned': float(row.points_earned or 0),
        'updated_at': row.updated_at.isoformat() if row.updated_at else None,
        **{f'pos_{i}': getattr(row, f'pos_{i}', 0) for i in range(1, 23)}
    }
    if kind == 'driver':
        result['driver_id'] = getattr(row, 'driver_id', None)
        result['full_name'] = getattr(row, 'full_name', None)
    return result


def recompute_and_store(year: int) -> Dict[str, List[Dict]]:
    """Recompute full standings and replace DB contents."""
    if local_standings is None:
        raise RuntimeError("standings module not available")
    schedule = fastf1.get_event_schedule(year) 

    """ schedules db!! """

    driver_df, constructor_df = local_standings.build_standings(schedule, year)

    with LocalSession() as session:
        # replace driver standings
        session.query(DriverStanding).delete()
        session.query(ConstructorStanding).delete()
        session.commit()

        now = datetime.datetime.utcnow()
        # insert drivers (skip those with null or empty DriverId)
        for _, r in driver_df.iterrows():
            driver_id = r['DriverId'] if not pd.isna(r['DriverId']) else None
            if not driver_id or str(driver_id).strip() == '':
                continue
            ds = DriverStanding(
                driver_id=str(driver_id),
                full_name=r['FullName'] if not pd.isna(r['FullName']) else '',
                team_name=r['TeamName'] if not pd.isna(r['TeamName']) else '',
                points_earned=float(r['PointsEarned'] or 0.0),
                updated_at=now,
            )
            # set pos_i fields dynamically
            for i in range(1, 23):
                col = f'pos_{i}'
                val = int(r[col]) if col in r and not pd.isna(r[col]) else 0
                setattr(ds, col, val)
            session.add(ds)

        # insert constructors
        for _, r in constructor_df.iterrows():
            cs = ConstructorStanding(
                team_name=r['TeamName'] if not pd.isna(r['TeamName']) else '',
                points_earned=float(r.get('PointsEarned') or 0.0),
                updated_at=now,
            )
            for i in range(1, 23):
                col = f'pos_{i}'
                val = int(r[col]) if col in r and not pd.isna(r[col]) else 0
                setattr(cs, col, val)
            session.add(cs)

        session.commit()

        # return fresh data
        drivers = session.query(DriverStanding).all()
        constructors = session.query(ConstructorStanding).all()
        return {
            'drivers': [_standing_row_to_dict(d, 'driver') for d in drivers],
            'constructors': [_standing_row_to_dict(c, 'constructor') for c in constructors],
        }


def get_standings(kind: str = 'driver') -> Dict[str, List[Dict]]:
    year = datetime.datetime.utcnow().year
    with LocalSession() as session:
        last_refresh = _get_last_refresh(session)

    # get last completed race datetime; best-effort
    try:
        last_race_dt = _get_last_completed_race_datetime(year)
    except Exception:
        last_race_dt = None

    last_refresh = _normalize_datetime(last_refresh)
    last_race_dt = _normalize_datetime(last_race_dt)

    if last_refresh and last_race_dt and last_refresh >= last_race_dt:
        with LocalSession() as session:
            if kind == 'driver':
                rows = session.query(DriverStanding).all()
                return {'drivers': [_standing_row_to_dict(r, 'driver') for r in rows]}
            rows = session.query(ConstructorStanding).all()
            return {'constructors': [_standing_row_to_dict(r, 'constructor') for r in rows]}

    if last_refresh and not last_race_dt:
        with LocalSession() as session:
            if kind == 'driver':
                rows = session.query(DriverStanding).all()
                if rows:
                    return {'drivers': [_standing_row_to_dict(r, 'driver') for r in rows]}
            else:
                rows = session.query(ConstructorStanding).all()
                if rows:
                    return {'constructors': [_standing_row_to_dict(r, 'constructor') for r in rows]}

    result = recompute_and_store(year)
    if kind == 'driver':
        return {'drivers': result['drivers']}
    return {'constructors': result['constructors']}
