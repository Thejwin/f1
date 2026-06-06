from src.services.standings_service import get_standings


def get_driver_standings():
    return get_standings(kind='driver')


def get_constructor_standings():
    return get_standings(kind='constructor')

