import { fetchSchedule } from "../api";
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/navbar/navbar";
import "./SchedulePage.css";

const SchedulePage = () => {
    const currentYear = new Date().getFullYear();
    const years = Array.from({ length: currentYear - 1950 + 1 }, (_, i) => currentYear - i);

    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedYear, setSelectedYear] = useState(currentYear);

    function getDate(session1date, session5date, session3date) {
        const session1 = new Date(`${session1date}Z`);
        const session2 = session5date == null ? new Date(`${session3date}Z`) : new Date(`${session5date}Z`);
        const options = { month: 'short', day: 'numeric' }
        return `${session1.toLocaleDateString(undefined, options)} - ${session2.toLocaleDateString(undefined, options)}`;
    }

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
                            <Link to={`/schedule/${selectedYear}/${event.RoundNumber}`} key={i} className="schedule-item-link">
                                <li className="schedule-item">
                                    <div className="schedule-round">
                                        R{event.RoundNumber}
                                    </div>
                                    <div className="schedule-details">
                                        <div className="schedule-title">{event.EventName}</div>
                                        <div className="schedule-location">
                                            {event.Location}, {event.Country}
                                        </div>
                                    </div>
                                    <div className="schedule-time">{getDate(event.Session1DateUtc, event.Session5DateUtc, event.Session3DateUtc)}</div>
                                </li>
                            </Link>
                        ))}
                    </ul>
                )}
            </div>
        </>
    )
}

export default SchedulePage