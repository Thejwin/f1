from src.utils.db import LocalSession
from src.models.driver_laps_model import DriverLaps
from src.models.session_results_model import SessionResult

def get_laps(year: int, round_number: int):
    with LocalSession() as session:
        rows = (
            session.query(
                DriverLaps.lap_number,
                DriverLaps.position,
                DriverLaps.driver,
                DriverLaps.driver_number,
                DriverLaps.team,
                SessionResult.team_color,
                SessionResult.full_name,
            )
            .join(
                SessionResult,
                (DriverLaps.year == SessionResult.year) &
                (DriverLaps.round_number == SessionResult.round_number) &
                (DriverLaps.driver_number == SessionResult.driver_number) &
                (SessionResult.session_identifier == 'R')
            )
            .filter(
                DriverLaps.year == year,
                DriverLaps.round_number == round_number#,
                #DriverLaps.position.isnot(None),
                #DriverLaps.is_accurate == True
            )
            .order_by(DriverLaps.lap_number, DriverLaps.position)
            .all()
        )

        return [
            {
                "lap": r.lap_number,
                "pos": r.position,
                "driver": r.driver,
                "driver_number": r.driver_number,
                "team": r.team,
                "team_color": r.team_color,
                "full_name": r.full_name,
            }
            for r in rows
        ]
