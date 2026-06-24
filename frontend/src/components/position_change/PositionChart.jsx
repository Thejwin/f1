import './PositionChart.css';
import { useState, useEffect } from 'react';
import { fetchRaceLaps } from '../../api';
import Chart from 'react-apexcharts';

const PositionChart = ({ year, RoundNumber }) => {
    const [raceLaps, setRaceLaps] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        setLoading(true);
        fetchRaceLaps(year, RoundNumber)
            .then((data) => {
                setRaceLaps(data);
                setLoading(false);
            })
            .catch((err) => {
                console.error("error loading data", err);
                setLoading(false);
            });
    }, [year, RoundNumber]);

    if (loading) return <div className="chart-loading">Loading telemetry data...</div>;
    if (!raceLaps || raceLaps.length === 0) return <div className="chart-error">No lap data available.</div>;

    // grp by driver as before
    const driversMap = {};
    raceLaps.forEach(row => {
        if (!driversMap[row.driver]) {
            driversMap[row.driver] = {
                name: row.driver,
                team: row.team || 'Unknown',
                color: row.team_color ? `#${row.team_color.replace('#', '')}` : '#FFFFFF',
                data: []
            };
        }
        driversMap[row.driver].data.push({ x: row.lap, y: row.pos });
    });

    const series = Object.values(driversMap).map(drv => {
        drv.data.sort((a, b) => a.x - b.x);
        return drv;
    });

    const teamCounts = {};
    const widthsArray = [];
    const dashArray = [];
    const colors = []

    series.forEach((driverSeries) => {
        const teamName = driverSeries.team;
        colors.push(driverSeries.color);

        // first/second driver 
        if (!teamCounts[teamName]) {
            teamCounts[teamName] = 1;
            // First driver: solid line
            widthsArray.push(1.2);
            dashArray.push(0);  // 0 means solid line
        } else {
            teamCounts[teamName] += 1;
            // Second driver: dotted line
            widthsArray.push(1.2);
            dashArray.push(4);    // 4px dash spacing creates a clean dotted/dashed look
        }
    });

    const options = {
        chart: {
            type: 'line',
            background: '#15151e',
            foreColor: '#fff',
            zoom: { enabled: false },
            toolbar: { show: false }
        },
        colors: colors,
        // DYNAMIC STYLING 
        stroke: {
            curve: 'straight',
            width: widthsArray,    // Array of widths per line
            dashArray: dashArray   // Array of dash styles per line
        },
        grid: { borderColor: '#2b2b3c' },
        xaxis: {
            type: 'numeric',
            title: { text: 'Lap', style: { color: '#fff' }, },
            tickAmount: 4
        },
        yaxis: {
            reversed: true,
            min: 1,
            max: year >= 2026 ? 22 : 20,
            tickAmount: year >= 2026 ? 21 : 19,
            title: { text: 'Position', style: { color: '#fff' } }
        },
        tooltip: {
            theme: 'dark',
            y: { formatter: (val) => `P${val}` }
        },
        legend: {
            position: 'right',
            labels: { colors: '#fff' }
        }
    };

    return (
        <div className="position-chart-container">
            <div className="heading">
                <h2>Position Changes During Race</h2>
            </div>
            <Chart options={options} series={series} type="line" height={450} />
        </div>
    );
};

export default PositionChart;