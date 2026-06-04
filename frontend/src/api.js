const canada26racekey = 11291

export const fetchCarData = () => {
  return fetch(
    "https://api.openf1.org/v1/car_data?driver_number=55&session_key=11291&speed>=315",
  )
    .then((response) => response.json())
    .then((jsonContent) => console.log(jsonContent));
};

export const fetchChampionshipDrivers = () => {
  return fetch(
    `https://api.openf1.org/v1/championship_drivers?session_key=${canada26racekey}&driver_number=81&driver_number=3`,
  )
    .then((response) => response.json())
    .then((jsonContent) => console.log(jsonContent));
};

export const fetchSessions = () => {
  return fetch(
    `https://api.openf1.org/v1/sessions?country_name=Canada&session_name=Race&year=2026`,
  )
    .then((response) => response.json())
    .then((jsonContent) => console.log(jsonContent));
};

