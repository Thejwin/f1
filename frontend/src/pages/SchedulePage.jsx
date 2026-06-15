import { fetchSchedule } from "../api";
import { useState, useEffect } from "react";
import Navbar from "../components/navbar/navbar";
import "./SchedulePage.css";

const SchedulePage = () => {
    const currentYear = new Date().getFullYear();
    const years = Array.from({ length: currentYear - 1950 + 1 }, (_, i) => currentYear - i);

    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState(currentYear);

    useEffect(() => {
        setLoading(true);
        fetchSchedule(selectedYear)
            .then((data) => {
                setSchedule(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Error fetching data:", err);
                setLoading(false);
            });
    }, [selectedYear])
    
    return (
        <>
            <Navbar />
            <div className="schedule-container">
                <div className="schedule-header-wrapper">
                    <h1>Schedule</h1>
                    <select 
                        className="year-selector" 
                        value={selectedYear} 
                        onChange={(e) => setSelectedYear(parseInt(e.target.value))}
                    >
                        {years.map(year => (
                            <option key={year} value={year}>{year}</option>
                        ))}
                    </select>
                </div>
                
                {loading ? (
                    <div style={{ marginTop: "40px" }}>Loading schedule data…</div>
                ) : (
                    <ul className="schedule-list">
                        {schedule.map((event, i) => (
                            <li className="schedule-item" key={i}>
                                <div className="schedule-round">
                                    R{event.RoundNumber}
                                </div>
                                <div className="schedule-details">
                                    <div className="schedule-title">{event.EventName}</div>
                                    <div className="schedule-location">
                                        {event.Location}, {event.Country}
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </>
    )
}

export default SchedulePage