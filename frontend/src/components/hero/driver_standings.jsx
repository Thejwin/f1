import Standing_entry from '../../cards/standing_entry'

const Driver_standings = ({ driver }) => {

  const standingsArray = driver?.drivers || [];
  if (!driver || standingsArray.length === 0) {
    return <div className='driver-standings'><p className='loading-text'>Loading standings data…</p></div>;
  }
  return (
    <div className='standings-list'>
      {standingsArray.map((entry, i) => (
          <Standing_entry 
              key={entry.driver_id}
              index={i + 1}
              id={entry.full_name} 
              team={entry.team_name} 
              points={entry.points_earned} />
      ))}
    </div>
  )
}

export default Driver_standings