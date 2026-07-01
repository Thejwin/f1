from datetime import datetime
import datetime as dt
from src.utils.db import LocalSession
from src.models.schedules_model import Schedule
from src.models.session_results_model import SessionResult
from scripts.backfill_results import backfill_results
from src.services.standings_service import _get_last_completed_race_datetime

def get_schedule(year):
    with LocalSession() as session:
        schedule = session.query(Schedule).filter_by(year=year).all() 
        return schedule    

def get_event_sessions(year, round_number):
    with LocalSession() as session:
        event = session.query(Schedule).filter_by(year=year, RoundNumber=round_number).first()
        return event

def get_session_results(year, round_number, session_id):
    with LocalSession() as session:
        results = session.query(SessionResult).filter_by(
            year=year, 
            round_number=round_number, 
            session_identifier=session_id
        ).order_by(SessionResult.position).all()
        last_race_dt = _get_last_completed_race_datetime(datetime.now().year)
        if not results and year == datetime.now().year and last_race_dt is not None and last_race_dt < dt.datetime.now(dt.UTC):
            backfill_results(year, year)
            results = session.query(SessionResult).filter_by(
                year=year, 
                round_number=round_number, 
                session_identifier=session_id
            ).order_by(SessionResult.position).all()
        return results