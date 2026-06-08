
import './standing_entry.css'
// For both drivers and consrtructers
const Standing_entry = ({ index, id, team, points }) => {
  return (
    <div className='standing-entry'>
      <div className='position'>{index}</div>
      <div className='driver-id'>{id}</div>
      <div className='team'>{team}</div>
      <div className='points'>
        {points}
        <span className='points-label'> PTS</span>
      </div>
    </div>
  )
}

export default Standing_entry