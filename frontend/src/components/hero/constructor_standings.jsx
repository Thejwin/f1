import React from 'react'
import Standing_entry from '../../cards/standing_entry'
import './standings.css'

const Constructor_standings = ({ constructor }) => {
  const standingsArray = constructor?.constructors || [];
  if (!constructor || standingsArray.length === 0) {
    return <div className='driver-standings'><p className='loading-text'>Loading standings data…</p></div>;
  }

  return (
    <div className="standings-container">
      <div className='standings-list'>
        {standingsArray.map((entry, i) => (
          <Standing_entry
            key={entry.constructorId}
            index={i + 1}
            id={entry.constructorName}
            team={entry.constructorNationality}
            points={entry.points_earned} />
        ))}
      </div>
    </div>
  )
}

export default Constructor_standings