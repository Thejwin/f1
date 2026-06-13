import { fetchSchedule } from "../api";
import { useState, useEffect } from "react";
import Navbar from "../components/navbar/navbar";
import "./SchedulePage.css";

const SchedulePage = () => {

    const [schedule, setSchedule] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchSchedule(2026)
            .then((data) => {
                setSchedule(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Error fetching data:", err);
                setLoading(false);
            });
    }, [])

    if (loading) {
        return (
            <>
                <Navbar />
                <div className="schedule-container">
                    <div style={{ marginTop: "40px" }}>Loading schedule data…</div>
                </div>
            </>
        );
    }
    
    return (
        <>
            <Navbar />
            <div className="schedule-container">
                <h1>Schedule</h1>
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
        </div>
        </>
    )
}

export default SchedulePage