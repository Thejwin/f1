import { fetchSchedule } from "../api";
import { useState, useEffect } from "react";
import Navbar from "../components/navbar/navbar";

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
        return <div>Loading schedule data…</div>;
    }
    else return (
        <div>
            <Navbar />
            <h1>Schedule</h1>
            <ul>
                {schedule.map((event, i) => (
                    <li key={i}>{event.RoundNumber}. {event.OfficialEventName.slice(10)}, {event.Country} - {event.Location}</li>
                ))}
            </ul>
        </div>
    )
}

export default SchedulePage