import src.services.race_laps_services as laps_services

def get_race_laps(year: int, round_number: int):
    return laps_services.get_laps(year, round_number)