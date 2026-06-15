import src.services.schedule_services as schedule_services

def get_schedules(year):
    return schedule_services.get_schedule(year)

def get_event_sessions(year, round_number):
    return schedule_services.get_event_sessions(year, round_number)

def get_session_results(year, round_number, session_id):
    return schedule_services.get_session_results(year, round_number, session_id)