import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home'
import SchedulePage from './pages/SchedulePage'
import EventPage from './pages/EventPage'
import SessionResultsPage from './pages/SessionResultsPage'
import './App.css'
import { fetchConstructorStandings, fetchDriverStandings } from './api'

function App() {

  const [driver_standings, setDriver_standings] = useState(null);
  const [constructor_standings, setConstructor_standings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [driverData, constructorData] = await Promise.all([
          fetchDriverStandings(),
          fetchConstructorStandings()
        ]);

        setDriver_standings(driverData);
        setConstructor_standings(constructorData);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <>

      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home driver={driver_standings} constructor={constructor_standings} />} />
          <Route path="/schedule" element={<SchedulePage />} />
          <Route path="/schedule/:year/:round" element={<EventPage />} />
          <Route path="/schedule/:year/:round/:sessionId" element={<SessionResultsPage />} />
        </Routes>
      </BrowserRouter>


    </>
  )
}

export default App
