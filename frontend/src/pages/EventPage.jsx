import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../components/navbar/navbar";
import { fetchEventSessions } from "../api";
import "./EventPage.css";

const SESSION_MAP = {
    conventional: [
        { id: "FP1", name: "Practice 1" },
        { id: "FP2", name: "Practice 2" },
        { id: "FP3", name: "Practice 3" },
        { id: "Q", name: "Qualifying" },
        { id: "R", name: "Race" },
    ],
    sprint: [
        { id: "FP1", name: "Practice 1" },
        { id: "Q", name: "Qualifying" },
        { id: "FP2", name: "Practice 2" },
        { id: "S", name: "Sprint" },
        { id: "R", name: "Race" },
    ],
    sprint_shootout: [
        { id: "FP1", name: "Practice 1" },
        { id: "Q", name: "Qualifying" },
        { id: "SS", name: "Sprint Shootout" },
        { id: "S", name: "Sprint" },
        { id: "R", name: "Race" },
    ],
    sprint_qualifying: [
        { id: "FP1", name: "Practice 1" },
        { id: "SQ", name: "Sprint Qualifying" },
        { id: "S", name: "Sprint" },
        { id: "Q", name: "Qualifying" },
        { id: "R", name: "Race" },
    ],
    default: [
        { id: "FP1", name: "Practice 1" },
        { id: "Q", name: "Qualifying" },
        { id: "R", name: "Race" },
    ],
};

const EventPage = () => {
    const { year, round } = useParams();
    const [event, setEvent] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        fetchEventSessions(year, round)
            .then((data) => {
                setEvent(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Error fetching event:", err);
                setLoading(false);
            });
    }, [year, round]);

    const sessions = event
        ? SESSION_MAP[event.EventFormat] || SESSION_MAP.default
        : [];

    return (
        <>
            <Navbar />
            <div className="event-container">
                <Link to="/schedule" className="back-link">← Back to Schedule</Link>

                {loading ? (
                    <div style={{ marginTop: "40px" }}>Loading event data…</div>
                ) : !event ? (
                    <div style={{ marginTop: "40px" }}>Event not found.</div>
                ) : (
                    <>
                        <h1>{event.EventName}</h1>
                        <p className="event-subtitle">
                            {event.Location}, {event.Country}
                        </p>

                        <h2>Sessions</h2>
                        <ul className="sessions-list">
                            {sessions.map((s) => (
                                <Link
                                    to={`/schedule/${year}/${round}/${s.id}`}
                                    key={s.id}
                                    className="session-item-link"
                                >
                                    <li className="session-item">
                                        <span className="session-badge">{s.id}</span>
                                        <span className="session-name">{s.name}</span>
                                        <span className="session-arrow">→</span>
                                    </li>
                                </Link>
                            ))}
                        </ul>
                    </>
                )}
            </div>
        </>
    );
};

export default EventPage;
