import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../components/navbar/navbar";
import { fetchEventSessions } from "../api";
import "./EventPage.css";

const SESSION_MAP = {
    conventional: [
        { id: "FP1", name: "Practice 1", session: "Session1DateUtc" },
        { id: "FP2", name: "Practice 2", session: "Session2DateUtc" },
        { id: "FP3", name: "Practice 3", session: "Session3DateUtc" },
        { id: "Q", name: "Qualifying", session: "Session4DateUtc" },
        { id: "R", name: "Race", session: "Session5DateUtc" },
    ],
    sprint: [
        { id: "FP1", name: "Practice 1", session: "Session1DateUtc" },
        { id: "Q", name: "Qualifying", session: "Session2DateUtc" },
        { id: "FP2", name: "Practice 2", session: "Session3DateUtc" },
        { id: "S", name: "Sprint", session: "Session4DateUtc" },
        { id: "R", name: "Race", session: "Session5DateUtc" },
    ],
    sprint_shootout: [
        { id: "FP1", name: "Practice 1", session: "Session1DateUtc" },
        { id: "Q", name: "Qualifying", session: "Session2DateUtc" },
        { id: "SS", name: "Sprint Shootout", session: "Session3DateUtc" },
        { id: "S", name: "Sprint", session: "Session4DateUtc" },
        { id: "R", name: "Race", session: "Session5DateUtc" },
    ],
    sprint_qualifying: [
        { id: "FP1", name: "Practice 1", session: "Session1DateUtc" },
        { id: "SQ", name: "Sprint Qualifying", session: "Session2DateUtc" },
        { id: "S", name: "Sprint", session: "Session3DateUtc" },
        { id: "Q", name: "Qualifying", session: "Session4DateUtc" },
        { id: "R", name: "Race", session: "Session5DateUtc" },
    ],
    default: [
        { id: "FP1", name: "Practice 1", session: "Session1DateUtc" },
        { id: "Q", name: "Qualifying", session: "Session2DateUtc" },
        { id: "R", name: "Race", session: "Session3DateUtc" },
    ],
};

function getDateandTime(sessionDate) {
    if (sessionDate === null) {
        return "Unavailable" //2020 emola for some reason
    }
    const session = new Date(`${sessionDate}Z`);
    const options = { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', hour12: true };
    return session.toLocaleTimeString(undefined, options);
}

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
                                        <span className="session-date">{getDateandTime(event[s.session])}</span>
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
