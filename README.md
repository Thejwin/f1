# F1 Dashboard

A full-stack Formula 1 companion application built with **FastAPI**, **React**, and **PostgreSQL**.

The project aims to provide a fast, modern interface for exploring Formula 1 data, including championship standings, race schedules, session results, telemetry, and historical season information.

## Current Features

* Driver Championship Standings
* Constructor Championship Standings
* Race Weekend Schedule
* Database-backed caching to avoid unnecessary data processing
* REST API built with FastAPI
* Responsive React frontend

## Planned Features

* Session Results
* Race Detail Pages
* Driver & Team Profiles
* Telemetry Analysis
* Historical Seasons
* Interactive Data Visualizations

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* FastF1

### Frontend

* React
* Vite
* CSS

## Project Structure

```text
backend/
├── routes/         # API endpoints
├── controllers/    # Request handlers
├── services/       # Business logic
├── models/         # Database models
├── utils/          # Configuration and utilities
└── scripts/        # Data ingestion and update jobs

frontend/
├── components/
├── pages/
├── cards/
└── api.js
```

## Architecture

```text
FastF1
   │
   ▼
Data Collection
   │
   ▼
PostgreSQL
   │
   ▼
FastAPI
   │
   ▼
React Frontend
```

The backend periodically retrieves Formula 1 data using FastF1 and stores processed results in PostgreSQL. Frequently requested information such as championship standings is served directly from the database and refreshed only when the cached data becomes outdated, reducing response times and unnecessary recomputation.

## Running Locally

### Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt

fastapi dev main.py
```

### Frontend

```bash
cd frontend

npm install
npm run dev
```

## Roadmap

* [x] Championship Standings
* [x] Race Schedule
* [x] Session Results
* [x] Race Pages
* [ ] Driver Profiles
* [ ] Team Profiles
* [ ] Telemetry Dashboard
* [ ] Historical Seasons
* [ ] Advanced Analytics

## License

MIT License
