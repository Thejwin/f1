import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import Navbar from "../components/navbar/navbar";
import { fetchSessionResults } from "../api";
import PositionChart from "../components/position_change/PositionChart";
import "./SessionResultsPage.css";

const SessionResultsPage = () => {
    const { year, round, sessionId } = useParams();
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        fetchSessionResults(year, round, sessionId)
            .then((data) => {
                setResults(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("Error fetching results:", err);
                setLoading(false);
            });
    }, [year, round, sessionId]);

    return (
        <>
            <Navbar />
            <div className="results-container">
                <Link to={`/schedule/${year}/${round}`} className="back-link">
                    ← Back to Event
                </Link>

                <h1>{sessionId} Results</h1>
                <p className="results-subtitle">Round {round}, {year}</p>

                {loading ? (
                    <div style={{ marginTop: "40px" }}>Loading results…</div>
                ) : results.length === 0 ? (
                    <div style={{ marginTop: "40px" }}>No results available for this session.</div>
                ) : (
                    <div className="results-table-wrapper">
                        <table className="results-table">
                            <thead>
                                <tr>
                                    <th>Pos</th>
                                    <th>No</th>
                                    <th>Driver</th>
                                    <th>Team</th>
                                    <th>Grid</th>
                                    <th>Time</th>
                                    <th>Pts</th>
                                    <th>Status</th>
                                    <th>Laps</th>
                                </tr>
                            </thead>
                            <tbody>
                                {results.map((r, idx) => (
                                    <tr key={idx}>
                                        <td className="col-pos">{r.position === null ? idx + 1 : r.position}</td>
                                        <td>{r.driver_number}</td>
                                        <td className="col-driver">
                                            {r.full_name || r.broadcast_name || r.driver_abbreviation}
                                        </td>
                                        <td>{r.team_name}</td>
                                        <td>{r.grid_position}</td>
                                        <td className="col-time">{r.time || "—"}</td>
                                        <td>{r.points}</td>
                                        <td>{r.status}</td>
                                        <td>{r.laps}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {sessionId === 'R' && !loading && results.length > 0 && (
                    <PositionChart year={year} RoundNumber={round} />
                )}
            </div>
        </>
    );
};

export default SessionResultsPage;
