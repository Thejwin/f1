from src.utils.db import LocalSession
from src.models.schedules_model import Schedule

def get_schedule(year):
    with LocalSession() as session:
        schedule = session.query(Schedule).filter_by(year=year).all() 
        return schedule    