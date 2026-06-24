import './PositionChart.css'
import { useState, useEffect } from 'react'
import { fetchRaceLaps } from '../../api';
import Chart from 'react-apexcharts';

const PositionChart = ({ year, RoundNumber }) => {
    const [raceLaps, setRaceLaps] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchRaceLaps(year, RoundNumber)
            .then((data) => {
                setRaceLaps(data);
                setLoading(false);
            })
            .catch((err) => {
                console.log("error loading data", err);
                setLoading(false);
            })
    }, [year, RoundNumber])

    if (loading) {
        return <div className="chart-loading">Loading telemetry data...</div>;
    }

    if (!raceLaps || raceLaps.length === 0) {
        return <div className="chart-error">No lap data available for this race.</div>;
    }

    const driversMap = {};
    raceLaps.forEach(row => {
        if (!driversMap[row.driver]) {
            driversMap[row.driver] = {
                name: row.driver,
                // Automatically fix missing hashtags or enforce a default fallback color
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

    const colors = series.map(s => s.color);

    // 7. Configure Chart Look & Feel
    const options = {
        chart: {
            type: 'line',
            background: '#15151e',
            foreColor: '#fff',
            zoom: { enabled: false },
            toolbar: { show: false }
        },
        colors: colors,
        stroke: { curve: 'straight', width: 2.5 },
        grid: { borderColor: '#2b2b3c' },
        xaxis: {
            type: 'numeric',
            title: { text: 'Lap', style: { color: '#fff' } }
        },
        yaxis: {
            reversed: true, // P1 at top, P20 at bottom
            min: 1,
            max: 20,
            tickAmount: 19,
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
            <Chart
                options={options}
                series={series}
                type="line"
                height={450}
            />
        </div>
    );
};


export default PositionChart