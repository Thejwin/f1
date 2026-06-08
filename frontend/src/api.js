const canada26racekey = 11291

export const fetchDriverStandings = () => {
  return fetch(
    `http://127.0.0.1:8000/driver-standings/`,
  )
    .then((response) => response.json())
    .then((jsonContent) => {
      console.log(jsonContent);
      return jsonContent;
    });
};

export const fetchConstructorStandings = () => {
  return fetch(
    `http://127.0.0.1:8000/constructor-standings/`,
  )
    .then((response) => response.json())
    .then((jsonContent) => {
      console.log(jsonContent);
      return jsonContent;
    });
};

