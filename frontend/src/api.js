const ip = "http://127.0.0.1:8000"

export const fetchDriverStandings = () =>
  fetch(`${ip}/driver-standings/`).then((res) => res.json());

export const fetchConstructorStandings = () =>
  fetch(`${ip}/constructor-standings/`).then((res) => res.json());

export const fetchSchedule = (year) =>
  fetch(`${ip}/schedule?year=${year}`).then((res) => res.json());

export const fetchEventSessions = (year, round) =>
  fetch(`${ip}/schedule/${year}/${round}`).then((res) => res.json());

export const fetchSessionResults = (year, round, sessionId) =>
  fetch(`${ip}/schedule/${year}/${round}/${sessionId}/results`).then((res) => res.json());

export const fetchRaceLaps = (year, round) =>
  fetch(`${ip}/laps/${year}/${round}`).then((res) => res.json());
