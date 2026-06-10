# F1 Standings Tracker

A lightweight web application for tracking Formula 1 statistics.

## Repository Structure

- `/backend`: Python backend powered by FastAPI.
  - Fetches Formula 1 statistics via the `fastf1` API.
  - Computes driver and constructor standings using official F1 tiebreakers (total points, wins, 2nd place finishes, etc.).
  - Persists data to a database using SQLAlchemy.
- `/frontend`: Frontend dashboard built with React and Vite.
  - Features an F1-themed dark mode user interface.
  - Includes a responsive standings list with tab switching between Drivers and Constructors.

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv env
   env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the FastAPI development server:
   ```bash
   fastapi dev main.py --reload
   ```
   ```Command prompt
   env\Scripts\activate.bat
   ```
   ```Powershell
   .\env\Scripts\Activate.ps1
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the React development server:
   ```bash
   npm run dev
   ```
