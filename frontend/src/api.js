export const fetchDriverStandings = () =>
  fetch(`http://127.0.0.1:8000/driver-standings/`).then((res) => res.json());

export const fetchConstructorStandings = () =>
  fetch(`http://127.0.0.1:8000/constructor-standings/`).then((res) => res.json());


