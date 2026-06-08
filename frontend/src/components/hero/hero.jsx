import { useState } from 'react'
import Driver_standings from './driver_standings'
import Constructor_standings from './constructor_standings'

const Hero = ({ driver, constructor: constructorData }) => {
  const [activeTab, setActiveTab] = useState('drivers');

  return (
    <div className="hero-section">
      <div className="standings-header">
        <div className="standings-tabs">
          <button 
            className={`standings-tab ${activeTab === 'drivers' ? 'active' : ''}`}
            onClick={() => setActiveTab('drivers')}
          >
            Drivers
          </button>
          <button 
            className={`standings-tab ${activeTab === 'constructors' ? 'active' : ''}`}
            onClick={() => setActiveTab('constructors')}
          >
            Constructors
          </button>
        </div>
      </div>

      {activeTab === 'drivers' 
        ? <Driver_standings driver={driver} />
        : <Constructor_standings constructor={constructorData} />
      }
    </div>
  )
}

export default Hero