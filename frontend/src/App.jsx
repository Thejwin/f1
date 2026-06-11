import { useState, useEffect } from 'react'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home'
import SchedulePage from './pages/SchedulePage'
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
        </Routes>
      </BrowserRouter>


    </>
  )
}

export default App
