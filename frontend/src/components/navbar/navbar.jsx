import React from 'react'
import './navbar.css'
import { useNavigate } from "react-router-dom";

// temp
const Navbar = () => {

  const navigate = useNavigate();

  return (
    <nav className='navbar'>
      <span className='nav-brand'>F1 STATS</span>
      <div className="nav-links">
        <button className="nav-btn" onClick={() => navigate("/")}>
          Home
        </button>
        <button className="nav-btn" onClick={() => navigate("/schedule")}>
          Schedule
        </button>
      </div>
    </nav>
  )
}

export default Navbar
