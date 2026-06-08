import { useState, useEffect } from 'react'
import Home from './pages/Home'
import './App.css'
import { fetchConstructorStandings, fetchDriverStandings } from './api'

function App() {

  const [driver_standings, setDriver_standings] = useState(null);
  const [constructor_standings, setConstructor_standings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const driverData = await fetchDriverStandings();
        const constructorData = await fetchConstructorStandings();
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

      <Home driver={driver_standings} constructor={constructor_standings} />

    </>
  )
}

export default App
