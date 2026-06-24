import React, { useState } from 'react'
import Standing_entry from '../../cards/standing_entry'
import './standings.css'

const Driver_standings = ({ driver }) => {
  const [expanded, setExpanded] = useState(false);

  const standingsArray = driver?.drivers || [];
  if (!driver || standingsArray.length === 0) {
    return <div className='driver-standings'><p className='loading-text'>Loading standings data…</p></div>;
  }

  const displayedStandings = expanded ? standingsArray : standingsArray.slice(0, 10);

  return (
    <div className="standings-container">
      <div className='standings-list'>
        {displayedStandings.map((entry, i) => (
          <Standing_entry
            key={entry.driver_id}
            index={i + 1}
            id={entry.full_name}
            team={entry.team_name}
            points={entry.points_earned} />
        ))}
      </div>
      {standingsArray.length > 10 && (
        <button className="expand-button" onClick={() => setExpanded(!expanded)}>
          {expanded ? 'Show Less' : 'Show More'}
        </button>
      )}
    </div>
  )
}

export default Driver_standings