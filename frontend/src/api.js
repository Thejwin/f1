export const fetchDriverStandings = () =>
  fetch(`http://127.0.0.1:8000/driver-standings/`).then((res) => res.json());

export const fetchConstructorStandings = () =>
  fetch(`http://127.0.0.1:8000/constructor-standings/`).then((res) => res.json());

export const fetchSchedule = (year) =>
  fetch(`http://127.0.0.1:8000/schedule?year=${year}`).then((res) => res.json());

export const fetchEventSessions = (year, round) =>
  fetch(`http://127.0.0.1:8000/schedule/${year}/${round}`).then((res) => res.json());

export const fetchSessionResults = (year, round, sessionId) =>
  fetch(`http://127.0.0.1:8000/schedule/${year}/${round}/${sessionId}/results`).then((res) => res.json());

export const fetchRaceLaps = (year, round) =>
  fetch(`http://127.0.0.1:8000/laps/${year}/${round}`).then((res) => res.json());
