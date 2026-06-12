/* JavaScript Logic for Deep Space Mission OS Dashboard */

// Global State variables for Playback Animation
let animationInterval = null;
let animationStep = 0;
let animationMaxSteps = 0;
let isPlaying = false;
let spacecraftPositionHistory = [];
let targetPositionHistory = [];
let earthPositionHistory = [];
let timeArray = [];
let destinationName = "Mars";

// Utilities
function getElementValue(id) {
    const el = document.getElementById(id);
    return el ? el.value : null;
}

function setElementText(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
}

function jdToCalendarDate(jd) {
    // Basic JD to calendar date approximation for display
    let z = Math.floor(jd + 0.5);
    let f = (jd + 0.5) - z;
    let a = z;
    if (z >= 2299161) {
        let alpha = Math.floor((z - 1867216.25) / 36524.25);
        a = z + 1 + alpha - Math.floor(alpha / 4);
    }
    let b = a + 1524;
    let c = Math.floor((b - 122.1) / 365.25);
    let d = Math.floor(365.25 * c);
    let e = Math.floor((b - d) / 30.6001);
    
    let day = b - d - Math.floor(30.6001 * e) + f;
    let month = e < 14 ? e - 1 : e - 13;
    let year = month > 2 ? c - 4716 : c - 4715;
    
    return `${year}-${String(month).padStart(2, '0')}-${String(Math.floor(day)).padStart(2, '0')}`;
}

// 1. Run Trajectory Simulation
async function runSimulation() {
    const dest = getElementValue("destination");
    const launchDate = getElementValue("launch_date");
    const flightDays = parseFloat(getElementValue("flight_days"));
    
    setElementText("btn-run-simulation", "Processing...");
    document.getElementById("btn-run-simulation").disabled = true;
    
    try {
        const response = await fetch("/api/v1/simulations/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                destination: dest,
                launch_date: launchDate,
                flight_days: flightDays
            })
        });
        
        if (!response.ok) throw new Error("Simulation execution failed");
        
        const data = await response.json();
        
        // Cache data for playback controls
        spacecraftPositionHistory = data.sc_position;
        timeArray = data.t;
        destinationName = dest.charAt(0).toUpperCase() + dest.slice(1);
        
        // Detect target position arrays in response
        if (data.mars_position) {
            targetPositionHistory = data.mars_position;
        } else if (data.moon_position) {
            targetPositionHistory = data.moon_position;
        } else if (data.asteroid_position) {
            targetPositionHistory = data.asteroid_position;
        } else {
            targetPositionHistory = [];
        }
        
        // Detect earth orbit values
        if (data.earth_position) {
            earthPositionHistory = data.earth_position;
        } else {
            earthPositionHistory = Array(spacecraftPositionHistory.length).fill([0.0, 0.0, 0.0]);
        }
        
        // Plot 3D Orbit Trajectories
        plot3DOrbit(data, dest);
        
        // Configure playback animation panel
        setupPlayback(spacecraftPositionHistory.length);
        
    } catch (err) {
        console.error(err);
        alert("Error executing N-body numerical simulation. Check server logs.");
    } finally {
        setElementText("btn-run-simulation", "Run Simulation");
        document.getElementById("btn-run-simulation").disabled = false;
    }
}

// Render Plotly 3D WebGL Chart
function plot3DOrbit(data, dest) {
    const sc = data.sc_position;
    const t = data.t;
    
    // Parse coordinates
    const scX = sc.map(p => p[0]);
    const scY = sc.map(p => p[1]);
    const scZ = sc.map(p => p[2]);
    
    const traces = [];
    
    // Spacecraft Trajectory
    traces.push({
        type: 'scatter3d',
        mode: 'lines',
        name: 'Spacecraft Trajectory',
        x: scX,
        y: scY,
        z: scZ,
        line: { color: '#3b82f6', width: 4 },
        hoverinfo: 'name+text',
        text: t.map((val, idx) => `Time: ${(val/86400).toFixed(1)} days`)
    });
    
    // Animated Spacecraft Point
    traces.push({
        type: 'scatter3d',
        mode: 'markers',
        name: 'Spacecraft Active Position',
        x: [scX[0]],
        y: [scY[0]],
        z: [scZ[0]],
        marker: { color: '#ffffff', size: 8, symbol: 'circle', line: { color: '#2563eb', width: 2 } }
    });
    
    if (dest.toLowerCase() === 'moon') {
        // Geocentric Simulation
        // Earth (Center)
        traces.push({
            type: 'scatter3d',
            mode: 'markers',
            name: 'Earth (Origin)',
            x: [0], y: [0], z: [0],
            marker: { color: '#1d4ed8', size: 14, line: { color: '#60a5fa', width: 1 } }
        });
        
        // Moon Orbits
        if (data.moon_position) {
            const m = data.moon_position;
            traces.push({
                type: 'scatter3d',
                mode: 'lines+markers',
                name: 'Moon Path',
                x: m.map(p => p[0]),
                y: m.map(p => p[1]),
                z: m.map(p => p[2]),
                line: { color: '#6b7280', width: 2, dash: 'dot' },
                marker: { color: '#9ca3af', size: 4 }
            });
        }
    } else {
        // Heliocentric Simulation
        // Sun (Origin)
        traces.push({
            type: 'scatter3d',
            mode: 'markers',
            name: 'Sun (Origin)',
            x: [0], y: [0], z: [0],
            marker: { color: '#eab308', size: 16, line: { color: '#f97316', width: 1 } }
        });
        
        // Earth position
        if (data.earth_position) {
            const e = data.earth_position;
            traces.push({
                type: 'scatter3d',
                mode: 'lines',
                name: 'Earth Path',
                x: e.map(p => p[0]),
                y: e.map(p => p[1]),
                z: e.map(p => p[2]),
                line: { color: '#10b981', width: 2, dash: 'dash' }
            });
        }
        
        // Destination target (Mars, Asteroid)
        const targetPos = data.mars_position || data.asteroid_position;
        if (targetPos) {
            const label = dest.charAt(0).toUpperCase() + dest.slice(1);
            traces.push({
                type: 'scatter3d',
                mode: 'lines+markers',
                name: `${label} Path`,
                x: targetPos.map(p => p[0]),
                y: targetPos.map(p => p[1]),
                z: targetPos.map(p => p[2]),
                line: { color: '#ef4444', width: 2, dash: 'dot' },
                marker: { color: '#f87171', size: 3 }
            });
        }
    }
    
    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 0, r: 0, t: 0, b: 0 },
        scene: {
            xaxis: { title: 'X (km)', gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)', color: '#9ca3af' },
            yaxis: { title: 'Y (km)', gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)', color: '#9ca3af' },
            zaxis: { title: 'Z (km)', gridcolor: 'rgba(255,255,255,0.05)', zerolinecolor: 'rgba(255,255,255,0.1)', color: '#9ca3af' },
            camera: { eye: { x: 1.5, y: 1.5, z: 1.2 } }
        },
        legend: { font: { color: '#e2e8f0' }, x: 0.1, y: 0.9 }
    };
    
    Plotly.newPlot('plot-3d', traces, layout, { responsive: true });
}

// 2. Playback Simulation Controls
function setupPlayback(maxSteps) {
    isPlaying = false;
    if (animationInterval) clearInterval(animationInterval);
    
    animationStep = 0;
    animationMaxSteps = maxSteps;
    
    document.getElementById("playback-panel").style.display = "flex";
    document.getElementById("btn-play-pause").innerText = "▶";
    
    const slider = document.getElementById("time-slider");
    slider.max = maxSteps - 1;
    slider.value = 0;
    
    updatePlaybackDisplay();
}

function updatePlaybackDisplay() {
    document.getElementById("time-slider").value = animationStep;
    const timeDays = (timeArray[animationStep] / 86400).toFixed(1);
    setElementText("playback-time", `T+ ${timeDays} Days (Step ${animationStep + 1}/${animationMaxSteps})`);
    
    // Update active spacecraft point coordinates on Plotly
    const plotEl = document.getElementById('plot-3d');
    if (plotEl && plotEl.data && plotEl.data[1]) {
        const scPos = spacecraftPositionHistory[animationStep];
        
        Plotly.restyle('plot-3d', {
            x: [[scPos[0]]],
            y: [[scPos[1]]],
            z: [[scPos[2]]]
        }, [1]);
    }
}

function togglePlayback() {
    if (isPlaying) {
        clearInterval(animationInterval);
        document.getElementById("btn-play-pause").innerText = "▶";
        isPlaying = false;
    } else {
        document.getElementById("btn-play-pause").innerText = "⏸";
        isPlaying = true;
        
        animationInterval = setInterval(() => {
            animationStep++;
            if (animationStep >= animationMaxSteps) {
                animationStep = 0; // Loop
            }
            updatePlaybackDisplay();
        }, 120);
    }
}

function setPlaybackStep(val) {
    animationStep = parseInt(val);
    updatePlaybackDisplay();
}

// 3. Plan Mission Details & Costs
async function planMission() {
    const dest = getElementValue("destination");
    const launchDate = getElementValue("launch_date");
    const m0 = parseFloat(getElementValue("spacecraft_mass"));
    const payload = parseFloat(getElementValue("payload_mass"));
    const propType = getElementValue("propulsion_type");
    
    setElementText("btn-plan-mission", "Planning...");
    
    try {
        const response = await fetch("/api/v1/mission/plan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                origin: "Earth",
                destination: dest.charAt(0).toUpperCase() + dest.slice(1),
                spacecraft_mass: m0,
                propulsion_type: propType,
                payload_mass: payload,
                launch_date: launchDate
            })
        });
        
        if (!response.ok) throw new Error("Mission planning failed");
        
        const data = await response.json();
        
        // Update Metrics Cards
        setFeasibilityCard(data.feasibility);
        setMetricValue("metric-deltav", `${data.delta_v_budget.total_delta_v_km_s.toFixed(2)} km/s`);
        setMetricValue("metric-propellant", `${(data.delta_v_budget.propellant_fraction * 100).toFixed(1)}%`);
        setMetricValue("metric-risk", `${data.risk_score.toFixed(1)} / 100`);
        
        // Update Timeline Tables
        renderTimelineTable(data.delta_v_budget.segments);
        
        // Automatically size staging and render plot
        runStagingSizing(payload, data.delta_v_budget.total_delta_v_m_s, propType);
        
    } catch (err) {
        console.error(err);
        alert("Failed to compile mission plan metrics.");
    } finally {
        setElementText("btn-plan-mission", "Plan Mission & Costs");
    }
}

function setFeasibilityCard(feasibility) {
    const card = document.getElementById("metric-feasibility");
    const valEl = card.querySelector(".metric-value");
    
    if (feasibility.feasible) {
        valEl.innerText = "PASS";
        valEl.style.color = "var(--accent-color)";
        card.classList.add("nominal-glow");
    } else {
        valEl.innerText = "FAIL";
        valEl.style.color = "var(--danger-color)";
        card.classList.remove("nominal-glow");
    }
}

function setMetricValue(id, value) {
    const card = document.getElementById(id);
    if (card) {
        card.querySelector(".metric-value").innerText = value;
    }
}

function renderTimelineTable(segments) {
    const tableBody = document.getElementById("timeline-body");
    tableBody.innerHTML = "";
    document.getElementById("timeline-card").style.display = "block";
    
    segments.forEach(seg => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td><strong>${seg.name}</strong></td>
            <td>${seg.delta_v_m_s.toFixed(1)}</td>
            <td>${seg.mass_start_kg ? seg.mass_start_kg.toFixed(0) : "0"}</td>
            <td>${seg.mass_end_kg ? seg.mass_end_kg.toFixed(0) : "0"}</td>
            <td>${seg.propellant_consumed_kg ? seg.propellant_consumed_kg.toFixed(1) : "0.0"}</td>
        `;
        tableBody.appendChild(tr);
    });
}

// Staging Sizing API Call & Bar Chart Rendering
async function runStagingSizing(payload, totalDv, propulsionType) {
    // Stage configurations base
    let Isp_stages = [320.0, 340.0];
    let structural_fractions = [0.1, 0.08];
    
    if (propulsionType === "Electric") {
        Isp_stages = [2000.0, 2200.0];
        structural_fractions = [0.18, 0.15];
    } else if (propulsionType === "Nuclear") {
        Isp_stages = [900.0, 950.0];
        structural_fractions = [0.15, 0.12];
    }
    
    try {
        const response = await fetch("/api/v1/staging/size", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                payload_mass: payload,
                total_dv: totalDv / 1000.0, // m/s to km/s or matching staging API expect
                Isp_stages: Isp_stages,
                structural_fractions: structural_fractions
            })
        });
        
        if (!response.ok) return;
        
        const data = await response.json();
        
        plotStagingBar(data);
        
    } catch (err) {
        console.error("Staging optimization failed:", err);
    }
}

function plotStagingBar(data) {
    const stages = data.stages;
    
    const xLabels = stages.map(s => `Stage ${s.stage}`);
    const propMasses = stages.map(s => s.propellant_mass_kg);
    const structMasses = stages.map(s => s.structural_mass_kg);
    
    const propTrace = {
        x: xLabels,
        y: propMasses,
        name: 'Propellant Mass (kg)',
        type: 'bar',
        marker: { color: 'rgba(59, 130, 246, 0.7)' }
    };
    
    const structTrace = {
        x: xLabels,
        y: structMasses,
        name: 'Structural Dry Mass (kg)',
        type: 'bar',
        marker: { color: 'rgba(168, 85, 247, 0.7)' }
    };
    
    const layout = {
        barmode: 'stack',
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 40, r: 20, t: 40, b: 40 },
        title: { text: 'Vehicle Stage Mass Sizing', font: { color: '#cbd5e1', size: 14 } },
        xaxis: { color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis: { title: 'Mass (kg)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        legend: { font: { color: '#e2e8f0' } }
    };
    
    Plotly.newPlot('plot-secondary', [propTrace, structTrace], layout, { responsive: true });
}

// 4. Generate Porkchop Launch Opportunity Grid
async function generatePorkchop() {
    const dest = getElementValue("destination");
    const depStart = getElementValue("porkchop_start_dep");
    const depEnd = getElementValue("porkchop_end_dep");
    const arrStart = getElementValue("porkchop_start_arr");
    const arrEnd = getElementValue("porkchop_end_arr");
    const steps = parseInt(getElementValue("porkchop_steps"));
    
    setElementText("btn-generate-porkchop", "Calculating Grid...");
    document.getElementById("btn-generate-porkchop").disabled = true;
    
    try {
        const response = await fetch("/api/v1/porkchop/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                destination: dest,
                start_departure_date: depStart,
                end_departure_date: depEnd,
                start_arrival_date: arrStart,
                end_arrival_date: arrEnd,
                steps: steps
            })
        });
        
        if (!response.ok) throw new Error("Porkchop grid calculation failed");
        
        const data = await response.json();
        
        plotPorkchopContour(data);
        
    } catch (err) {
        console.error(err);
        alert("Failed to compute Porkchop launch energy contour map.");
    } finally {
        setElementText("btn-generate-porkchop", "Generate Porkchop Grid");
        document.getElementById("btn-generate-porkchop").disabled = false;
    }
}

function plotPorkchopContour(data) {
    const depDates = data.departure_jds.map(jd => jdToCalendarDate(jd));
    const arrDates = data.arrival_jds.map(jd => jdToCalendarDate(jd));
    
    // Replace null elements in c3 matrix with NaN for Plotly's rendering engine
    const zData = data.c3.map(row => row.map(val => val === null ? NaN : val));
    
    const plotData = [{
        z: zData,
        x: depDates,
        y: arrDates,
        type: 'contour',
        colorscale: 'Viridis',
        colorbar: {
            title: 'C3 Energy (km²/s²)',
            titlefont: { color: '#cbd5e1' },
            tickfont: { color: '#cbd5e1' }
        },
        contours: {
            coloring: 'heatmap',
            showlabels: true,
            labelfont: { size: 10, color: '#ffffff' }
        }
    }];
    
    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 60, r: 20, t: 40, b: 60 },
        xaxis: { title: 'Departure Launch Date', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis: { title: 'Arrival Target Date', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' }
    };
    
    Plotly.newPlot('plot-porkchop', plotData, layout, { responsive: true });
}

// 5. Run Genetic Algorithm Optimization
async function runOptimization() {
    const dest = getElementValue("destination");
    const launchDate = getElementValue("launch_date");
    
    // Approximate a search window based on launch date
    const dateObj = new Date(launchDate);
    const minDep = launchDate;
    
    const maxDate = new Date(dateObj);
    maxDate.setDate(maxDate.getDate() + 30);
    const maxDep = maxDate.toISOString().split('T')[0];
    
    setElementText("btn-optimize", "GA Optimizing...");
    
    try {
        const response = await fetch("/api/v1/optimization/optimize", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                destination: dest,
                algorithm: "ga",
                min_departure_date: minDep,
                max_departure_date: maxDep,
                min_duration_days: 150.0,
                max_duration_days: 350.0,
                population_size: 20,
                generations: 20
            })
        });
        
        if (!response.ok) throw new Error("GA Optimization failed");
        
        const data = await response.json();
        
        // Plot GA convergence history
        plotGAConvergence(data.history);
        
        // Sync launch date & flight duration values with inputs
        document.getElementById("launch_date").value = data.best_departure_calendar;
        document.getElementById("flight_days").value = Math.round(data.best_duration_days);
        
        alert(`GA Optimal Window Found!\nDeparture: ${data.best_departure_calendar}\nTransit: ${Math.round(data.best_duration_days)} days\nMinimum Delta-V: ${data.min_delta_v_km_s.toFixed(2)} km/s`);
        
    } catch (err) {
        console.error(err);
        alert("Failed to execute Genetic Algorithm trajectory optimizer.");
    } finally {
        setElementText("btn-optimize", "Run Genetic Algorithm");
    }
}

function plotGAConvergence(history) {
    const generations = history.map((_, idx) => idx + 1);
    
    const trace = {
        x: generations,
        y: history,
        mode: 'lines+markers',
        name: 'Best Delta-V Cost',
        line: { color: '#10b981', width: 3 },
        marker: { color: '#059669', size: 6 }
    };
    
    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 40, r: 20, t: 40, b: 40 },
        title: { text: 'Genetic Algorithm Solver Convergence', font: { color: '#cbd5e1', size: 14 } },
        xaxis: { title: 'Generation Iteration', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis: { title: 'Fitness Delta-V (km/s)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' }
    };
    
    Plotly.newPlot('plot-secondary', [trace], layout, { responsive: true });
}

// --- Orbit Tweaker Sliders & HUD logic ---

const BODY_RADII = {
    "earth": 6378.137,
    "moon": 1737.4,
    "mars": 3389.5,
    "sun": 696340.0
};

const BODY_MU = {
    "earth": 3.986004418e5,
    "moon": 4.9048695e3,
    "mars": 4.282837e4,
    "sun": 1.32712440018e11
};

const BODY_J2 = {
    "earth": 1.08262668e-3,
    "moon": 2.0302e-4,
    "mars": 1.96045e-3,
    "sun": 2.2e-7
};

let visVivaDebounceTimer = null;
let tweakedOrbitData = null;

function estimateJ2Rates(a, e, i, body) {
    const mu = BODY_MU[body] || BODY_MU["earth"];
    const R = BODY_RADII[body] || BODY_RADII["earth"];
    const J2 = BODY_J2[body] || BODY_J2["earth"];
    
    const p = a * (1.0 - e * e);
    if (p <= 0 || a <= 0) return { dOmega_dt: 0, dwomega_dt: 0, period: 0 };
    
    const n = Math.sqrt(mu / (a * a * a));
    const iRad = (i * Math.PI) / 180.0;
    
    // Nodal precession and Apsidal drift rates (rad/s)
    const dOmega_dt = -1.5 * J2 * Math.pow(R / p, 2) * n * Math.cos(iRad);
    const dwomega_dt = 0.75 * J2 * Math.pow(R / p, 2) * n * (5.0 * Math.pow(Math.cos(iRad), 2) - 1.0);
    const period = 2.0 * Math.PI * Math.sqrt(Math.pow(a, 3) / mu);
    
    return { dOmega_dt, dwomega_dt, period };
}

function onTweakerParamsChange() {
    clearPostBurnOrbit();
    clearTransferOrbits();
    clearMonteCarlo();
    const a = parseFloat(document.getElementById("tweaker_a").value);
    const e = parseFloat(document.getElementById("tweaker_e").value);
    const i = parseFloat(document.getElementById("tweaker_i").value);
    const raan = parseFloat(document.getElementById("tweaker_raan").value);
    const body = document.getElementById("tweaker_body").value;
    const j2Enabled = document.getElementById("tweaker_j2").checked;
    const nbodyEnabled = document.getElementById("tweaker_nbody").checked;

    // Enable/disable Sun-Sync buttons depending on central body
    const solveBtn = document.getElementById("btn-solve-sunsync");
    if (solveBtn) {
        solveBtn.disabled = (body === "sun");
    }
    const optimizeBtn = document.getElementById("btn-optimize-sunsync-raan");
    if (optimizeBtn) {
        optimizeBtn.disabled = (body === "sun");
    }

    // Update parameter displays in label
    document.getElementById("val_tweaker_a").innerText = a;
    document.getElementById("val_tweaker_e").innerText = e.toFixed(2);
    document.getElementById("val_tweaker_i").innerText = i.toFixed(1);
    document.getElementById("val_tweaker_raan").innerText = raan.toFixed(1);

    const xPoints = [];
    const yPoints = [];
    const zPoints = [];
    const iRad = (i * Math.PI) / 180.0;

    if (nbodyEnabled) {
        const duration = parseFloat(document.getElementById("tweaker_duration").value);
        document.getElementById("val_tweaker_duration").innerText = duration;
        
        // Instant visual feedback during slider drags: Draw standard Keplerian ellipse
        const thetaSteps = 120;
        const omega = (raan * Math.PI) / 180.0;
        const cosO = Math.cos(omega);
        const sinO = Math.sin(omega);
        const cosi = Math.cos(iRad);
        const sini = Math.sin(iRad);

        for (let k = 0; k <= thetaSteps; k++) {
            const theta = (k * 2.0 * Math.PI) / thetaSteps;
            const denom = 1.0 + e * Math.cos(theta);
            const r = (a * (1.0 - e * e)) / denom;

            const xPerifocal = r * Math.cos(theta);
            const yPerifocal = r * Math.sin(theta);

            const xRot = xPerifocal * cosO - yPerifocal * sinO * cosi;
            const yRot = xPerifocal * sinO + yPerifocal * cosO * cosi;
            const zRot = yPerifocal * sini;

            xPoints.push(xRot);
            yPoints.push(yRot);
            zPoints.push(zRot);
        }
    } else if (j2Enabled) {
        // Retrieve J2 rates
        const rates = estimateJ2Rates(a, e, i, body);
        
        // Visual amplification factor so precession is obvious in the 3D viewer
        const visualScale = 200.0;
        const dOmega_dt = rates.dOmega_dt * visualScale;
        const dwomega_dt = rates.dwomega_dt * visualScale;
        const period = rates.period;

        // Draw multiple revolutions to show the precessing rosette trajectory
        const numRevolutions = 8;
        const stepsPerRev = 100;
        const totalSteps = numRevolutions * stepsPerRev;

        for (let k = 0; k <= totalSteps; k++) {
            const theta = (k * 2.0 * Math.PI) / stepsPerRev;
            const denom = 1.0 + e * Math.cos(theta);
            const r = (a * (1.0 - e * e)) / denom;

            const t = (theta / (2.0 * Math.PI)) * period;
            const omega = ((raan * Math.PI) / 180.0) + dOmega_dt * t;
            const womega = dwomega_dt * t;

            // Perifocal coordinates
            const xP = r * Math.cos(theta);
            const yP = r * Math.sin(theta);

            // 3D rotation using omega (ascending node), inclination, and womega (argument of periapsis)
            const cosO = Math.cos(omega);
            const sinO = Math.sin(omega);
            const cosw = Math.cos(womega);
            const sinw = Math.sin(womega);
            const cosi = Math.cos(iRad);
            const sini = Math.sin(iRad);

            const xRot = xP * (cosO * cosw - sinO * sinw * cosi) - yP * (cosO * sinw + sinO * cosw * cosi);
            const yRot = xP * (sinO * cosw + cosO * sinw * cosi) - yP * (sinO * sinw - cosO * cosw * cosi);
            const zRot = xP * (sinw * sini) + yP * (cosw * sini);

            xPoints.push(xRot);
            yPoints.push(yRot);
            zPoints.push(zRot);
        }
    } else {
        // Generate standard 3D ellipse points with initial RAAN (Ω)
        const thetaSteps = 120;
        const omega = (raan * Math.PI) / 180.0;
        const cosO = Math.cos(omega);
        const sinO = Math.sin(omega);
        const cosi = Math.cos(iRad);
        const sini = Math.sin(iRad);

        for (let k = 0; k <= thetaSteps; k++) {
            const theta = (k * 2 * Math.PI) / thetaSteps;
            const denom = 1.0 + e * Math.cos(theta);
            const r = (a * (1.0 - e * e)) / denom;

            const xPerifocal = r * Math.cos(theta);
            const yPerifocal = r * Math.sin(theta);

            const xRot = xPerifocal * cosO - yPerifocal * sinO * cosi;
            const yRot = xPerifocal * sinO + yPerifocal * cosO * cosi;
            const zRot = yPerifocal * sini;

            xPoints.push(xRot);
            yPoints.push(yRot);
            zPoints.push(zRot);
        }
    }

    tweakedOrbitData = { x: xPoints, y: yPoints, z: zPoints, body: body };

    // Redraw or overlay onto the 3D WebGL Chart
    update3DPlotWithTweakedOrbit();

    // Debounce vis-viva API query (120ms delay)
    if (visVivaDebounceTimer) clearTimeout(visVivaDebounceTimer);
    visVivaDebounceTimer = setTimeout(() => {
        queryVisViva(a, e, body, i, j2Enabled || nbodyEnabled);
        if (nbodyEnabled) {
            const duration = parseFloat(document.getElementById("tweaker_duration").value);
            queryPerturbedPropagation(a, e, i, raan, body, j2Enabled, nbodyEnabled, duration);
        }
    }, 120);
}

function update3DPlotWithTweakedOrbit() {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl) return;

    const tweakedTrace = {
        type: 'scatter3d',
        mode: 'lines',
        name: 'Tweaked Orbit',
        x: tweakedOrbitData.x,
        y: tweakedOrbitData.y,
        z: tweakedOrbitData.z,
        line: { color: '#a855f7', width: 4 }
    };

    const isPlaceholder = plotEl.querySelector('.chart-placeholder') !== null;
    if (isPlaceholder || !plotEl.data) {
        // Create initial clean plot with tweaked orbit
        const traces = [
            {
                type: 'scatter3d',
                mode: 'markers',
                name: tweakedOrbitData.body.charAt(0).toUpperCase() + tweakedOrbitData.body.slice(1) + ' (Origin)',
                x: [0], y: [0], z: [0],
                marker: { color: getBodyColor(tweakedOrbitData.body), size: 14 }
            },
            tweakedTrace
        ];

        const layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            margin: { l: 0, r: 0, t: 0, b: 0 },
            scene: {
                xaxis: { title: 'X (km)', gridcolor: 'rgba(255,255,255,0.05)', color: '#9ca3af' },
                yaxis: { title: 'Y (km)', gridcolor: 'rgba(255,255,255,0.05)', color: '#9ca3af' },
                zaxis: { title: 'Z (km)', gridcolor: 'rgba(255,255,255,0.05)', color: '#9ca3af' },
                camera: { eye: { x: 1.5, y: 1.5, z: 1.2 } }
            },
            legend: { font: { color: '#e2e8f0' }, x: 0.1, y: 0.9 }
        };

        Plotly.newPlot('plot-3d', traces, layout, { responsive: true });
    } else {
        // Find existing tweaked trace
        let tweakedTraceIdx = -1;
        for (let idx = 0; idx < plotEl.data.length; idx++) {
            if (plotEl.data[idx].name === 'Tweaked Orbit') {
                tweakedTraceIdx = idx;
                break;
            }
        }

        if (tweakedTraceIdx !== -1) {
            Plotly.restyle('plot-3d', {
                x: [tweakedOrbitData.x],
                y: [tweakedOrbitData.y],
                z: [tweakedOrbitData.z]
            }, [tweakedTraceIdx]);
        } else {
            Plotly.addTraces('plot-3d', tweakedTrace);
        }
    }
}

function getBodyColor(body) {
    const colorMap = {
        "earth": "#3b82f6",
        "moon": "#9ca3af",
        "mars": "#ef4444",
        "sun": "#eab308"
    };
    return colorMap[body] || "#ffffff";
}

async function queryVisViva(a, e, body, i, j2Enabled) {
    try {
        const response = await fetch("/api/v1/astrodynamics/vis-viva", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                a: a,
                e: e,
                mu_type: body,
                r: null,
                i: i
            })
        });

        if (!response.ok) return;

        const data = await response.json();

        // Calculate surface altitudes
        const radius = BODY_RADII[body] || 0.0;
        const altPeri = Math.max(0.0, data.rp_km - radius);
        const altApo = Math.max(0.0, data.ra_km - radius);

        const periodHrs = data.period_s / 3600.0;
        let periodText = "";
        if (periodHrs > 48.0) {
            periodText = `${(periodHrs / 24.0).toFixed(2)} days`;
        } else {
            periodText = `${periodHrs.toFixed(2)} hrs`;
        }

        // Display on HUD card
        document.getElementById("hud-v-peri").innerText = `${data.v_periapsis_km_s.toFixed(3)} km/s`;
        document.getElementById("hud-v-apo").innerText = `${data.v_apoapsis_km_s.toFixed(3)} km/s`;
        document.getElementById("hud-alt-peri").innerText = `${Math.round(altPeri).toLocaleString()} km`;
        document.getElementById("hud-alt-apo").innerText = `${Math.round(altApo).toLocaleString()} km`;
        document.getElementById("hud-period").innerText = periodText;

        // J2 elements display
        const j2Metrics = document.querySelectorAll(".j2-only");
        if (j2Enabled) {
            j2Metrics.forEach(m => m.style.display = "flex");
            document.getElementById("hud-j2-node").innerText = `${data.nodal_precession_deg_day.toFixed(4)}°/d`;
            document.getElementById("hud-j2-apsidal").innerText = `${data.apsidal_rotation_deg_day.toFixed(4)}°/d`;
        } else {
            j2Metrics.forEach(m => m.style.display = "none");
        }

        // Atmospheric entry warning HUD styling shifts
        const hud = document.getElementById("orbit-hud");
        const bodyColor = getBodyColor(body);
        if (data.entry_warning) {
            hud.style.borderColor = "var(--danger-color)";
            hud.style.boxShadow = "0 0 15px rgba(239, 68, 68, 0.45)";
            document.getElementById("hud-alt-peri").style.color = "var(--danger-color)";
            document.getElementById("hud-alt-peri").innerText += " ⚠️ DECAY";
        } else {
            hud.style.borderColor = "rgba(255, 255, 255, 0.05)";
            hud.style.boxShadow = "none";
            document.getElementById("hud-alt-peri").style.color = bodyColor;
        }

        // Color glow adjustment based on reference body selection
        const hudValues = document.querySelectorAll(".hud-value");
        hudValues.forEach(val => {
            if (val.id === "hud-alt-peri" && data.entry_warning) return;
            val.style.color = bodyColor;
            val.style.textShadow = `0 0 10px ${bodyColor}66`;
        });

    } catch (err) {
        console.error("Orbit HUD update failed:", err);
    }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("tweaker_a")) {
        onTweakerParamsChange();
    }
    if (document.getElementById("mc_runs")) {
        onMonteCarloParamsChange();
    }
});

async function queryPerturbedPropagation(a, e, i, raan, body, j2Enabled, nbodyEnabled, duration) {
    try {
        const response = await fetch("/api/v1/astrodynamics/propagate-perturbed", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                a: a,
                e: e,
                i: i,
                omega: 0.0,
                raan: raan,
                mu_type: body,
                duration_days: duration,
                j2_enabled: j2Enabled,
                nbody_enabled: nbodyEnabled
            })
        });

        if (!response.ok) return;
        const data = await response.json();

        // Extract coordinate points
        const xPoints = data.sc_position.map(p => p[0]);
        const yPoints = data.sc_position.map(p => p[1]);
        const zPoints = data.sc_position.map(p => p[2]);

        tweakedOrbitData = { x: xPoints, y: yPoints, z: zPoints, body: body };
        update3DPlotWithTweakedOrbit();

        // Atmospheric entry warnings styles in propagation
        const hud = document.getElementById("orbit-hud");
        const bodyColor = getBodyColor(body);
        if (data.entry_warning) {
            hud.style.borderColor = "var(--danger-color)";
            hud.style.boxShadow = "0 0 20px rgba(239, 68, 68, 0.45)";
            document.getElementById("hud-alt-peri").style.color = "var(--danger-color)";
            document.getElementById("hud-alt-peri").innerText = `${Math.round(data.min_altitude_km).toLocaleString()} km ⚠️ CRITICAL DECAY`;
        }

    } catch (err) {
        console.error("Perturbed propagation failed:", err);
    }
}

function toggleNBodyControls() {
    const nbodyEnabled = document.getElementById("tweaker_nbody").checked;
    const durationGroup = document.getElementById("nbody_duration_group");
    if (nbodyEnabled) {
        durationGroup.style.display = "flex";
    } else {
        durationGroup.style.display = "none";
    }
    onTweakerParamsChange();
}

async function solveSunSyncInclination() {
    const a = parseFloat(document.getElementById("tweaker_a").value);
    const e = parseFloat(document.getElementById("tweaker_e").value);
    const body = document.getElementById("tweaker_body").value;

    if (body === "sun") {
        alert("Sun-Synchronous orbits are not defined with the Sun as the central body.");
        return;
    }

    try {
        const response = await fetch("/api/v1/astrodynamics/sun-synchronous", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                a: a,
                e: e,
                mu_type: body
            })
        });

        if (!response.ok) throw new Error("Sun-synchronous solver failed");
        const data = await response.json();

        if (data.possible) {
            const incVal = data.inclination_deg;
            document.getElementById("tweaker_i").value = incVal.toFixed(1);
            document.getElementById("val_tweaker_i").innerText = incVal.toFixed(1);
            onTweakerParamsChange();
            alert(`Sun-Synchronous inclination solved successfully!\nRequired Inclination: ${incVal.toFixed(2)}°\nPrecession Target: ${data.target_rate_deg_day.toFixed(4)}°/day`);
        } else {
            alert(`Sun-Synchronous orbit is NOT possible at this altitude (${a} km) and eccentricity (${e.toFixed(2)}).\nJ2 precession at any inclination cannot match the target rate of ${data.target_rate_deg_day.toFixed(4)}°/day.`);
        }
    } catch (err) {
        console.error(err);
        alert("Error running Sun-Synchronous inclination solver.");
    }
}

async function optimizeSunSyncRAAN() {
    const launchDate = document.getElementById("tweaker_launch_date").value;
    const ltan = parseFloat(document.getElementById("tweaker_ltan").value);
    const body = document.getElementById("tweaker_body").value;

    if (body === "sun") {
        alert("Sun-Synchronous planes are not defined with the Sun as the central body.");
        return;
    }

    try {
        const response = await fetch("/api/v1/astrodynamics/sunsync-raan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                launch_date: launchDate,
                ltan_hours: ltan
            })
        });

        if (!response.ok) throw new Error("RAAN solver failed");
        const data = await response.json();

        const raanVal = data.raan_deg;
        document.getElementById("tweaker_raan").value = raanVal.toFixed(1);
        document.getElementById("val_tweaker_raan").innerText = raanVal.toFixed(1);

        onTweakerParamsChange();
        alert(`Sun-Synchronous plane optimized successfully!\nTarget RAAN (Ω): ${raanVal.toFixed(2)}°\nLaunch Date: ${launchDate}\nSun Right Ascension: ${data.sun_ra_deg.toFixed(2)}°`);

    } catch (err) {
        console.error(err);
        alert("Error running Sun-Synchronous RAAN optimizer.");
    }
}

function onStationKeepingChange() {
    const dv = parseFloat(document.getElementById("tweaker_dv_burn").value);
    document.getElementById("val_tweaker_dv_burn").innerText = dv;
    clearPostBurnOrbit();
}

function clearPostBurnOrbit() {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl || !plotEl.data) return;
    let idx = plotEl.data.findIndex(t => t.name === 'Post-Burn Orbit');
    if (idx !== -1) {
        Plotly.deleteTraces('plot-3d', idx);
    }
    const panel = document.getElementById("sk-results-panel");
    if (panel) panel.style.display = "none";
}

async function executeStationKeepingBurn() {
    const a = parseFloat(document.getElementById("tweaker_a").value);
    const e = parseFloat(document.getElementById("tweaker_e").value);
    const i = parseFloat(document.getElementById("tweaker_i").value);
    const raan = parseFloat(document.getElementById("tweaker_raan").value);
    const body = document.getElementById("tweaker_body").value;
    const dv = parseFloat(document.getElementById("tweaker_dv_burn").value);
    
    // Mission parameters defaults
    const wetMassEl = document.getElementById("spacecraft_mass");
    const payloadEl = document.getElementById("payload_mass");
    const ispEl = document.getElementById("isp");
    
    const m0 = wetMassEl ? parseFloat(wetMassEl.value) || 2500.0 : 2500.0;
    const m_payload = payloadEl ? parseFloat(payloadEl.value) || 800.0 : 800.0;
    const isp = ispEl ? parseFloat(ispEl.value) || 320.0 : 320.0;
    
    try {
        const response = await fetch("/api/v1/astrodynamics/station-keeping", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                a: a,
                e: e,
                mu_type: body,
                dv_burn_m_s: dv,
                m0_wet_kg: m0,
                m_payload_kg: m_payload,
                isp_s: isp
            })
        });
        
        if (!response.ok) throw new Error("Station keeping burn computation failed");
        
        const data = await response.json();
        
        // Show results panel
        const panel = document.getElementById("sk-results-panel");
        if (panel) {
            panel.style.display = "flex";
        }
        
        const newAltVal = document.getElementById("sk-new-alt");
        if (newAltVal) {
            newAltVal.innerText = `${Math.round(data.new_rp_alt_km).toLocaleString()} km`;
        }
        
        const fuelMassVal = document.getElementById("sk-fuel-mass");
        if (fuelMassVal) {
            fuelMassVal.innerText = `${data.fuel_consumed_kg.toFixed(1)} kg / ${data.available_propellant_kg.toFixed(1)} kg`;
        }
        
        const fuelWarningDiv = document.getElementById("sk-fuel-warning");
        if (fuelWarningDiv) {
            fuelWarningDiv.style.display = data.fuel_warning ? "block" : "none";
        }
        
        // Plot post-burn orbit
        plotPostBurnOrbit(data.new_a_km, data.new_e, i, raan, body);
        
    } catch (err) {
        console.error(err);
        alert("Error executing active station keeping burn simulation.");
    }
}

function plotPostBurnOrbit(newA, newE, i, raan, body) {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl) return;
    
    const xPoints = [];
    const yPoints = [];
    const zPoints = [];
    const iRad = (i * Math.PI) / 180.0;
    const omega = (raan * Math.PI) / 180.0;
    const cosO = Math.cos(omega);
    const sinO = Math.sin(omega);
    const cosi = Math.cos(iRad);
    const sini = Math.sin(iRad);
    
    const thetaSteps = 120;
    for (let k = 0; k <= thetaSteps; k++) {
        const theta = (k * 2.0 * Math.PI) / thetaSteps;
        const denom = 1.0 + newE * Math.cos(theta);
        const r = (newA * (1.0 - newE * newE)) / denom;
        
        const xPerifocal = r * Math.cos(theta);
        const yPerifocal = r * Math.sin(theta);
        
        const xRot = xPerifocal * cosO - yPerifocal * sinO * cosi;
        const yRot = xPerifocal * sinO + yPerifocal * cosO * cosi;
        const zRot = yPerifocal * sini;
        
        xPoints.push(xRot);
        yPoints.push(yRot);
        zPoints.push(zRot);
    }
    
    const postBurnTrace = {
        type: 'scatter3d',
        mode: 'lines',
        name: 'Post-Burn Orbit',
        x: xPoints,
        y: yPoints,
        z: zPoints,
        line: { color: '#06b6d4', width: 3, dash: 'dash' }
    };
    
    if (plotEl.data) {
        let postBurnTraceIdx = plotEl.data.findIndex(t => t.name === 'Post-Burn Orbit');
        if (postBurnTraceIdx !== -1) {
            Plotly.restyle('plot-3d', {
                x: [xPoints],
                y: [yPoints],
                z: [zPoints]
            }, [postBurnTraceIdx]);
        } else {
            Plotly.addTraces('plot-3d', postBurnTrace);
        }
    }
}

function toggleTransferControls() {
    const type = document.getElementById("transfer_type").value;
    const boostGroup = document.getElementById("transfer_boost_r_group");
    if (boostGroup) {
        boostGroup.style.display = type === "bielliptic" ? "block" : "none";
    }
    const thrustGroup = document.getElementById("transfer_thrust_group");
    if (thrustGroup) {
        thrustGroup.style.display = type === "lowthrust" ? "block" : "none";
    }
    clearTransferOrbits();
}

function onTransferParamsChange() {
    const targetR = parseFloat(document.getElementById("transfer_target_r").value);
    document.getElementById("val_transfer_target_r").innerText = targetR;
    
    const boostR = document.getElementById("transfer_boost_r");
    if (boostR) {
        document.getElementById("val_transfer_boost_r").innerText = boostR.value;
    }
    
    const thrustSlider = document.getElementById("transfer_thrust");
    if (thrustSlider) {
        document.getElementById("val_transfer_thrust").innerText = parseFloat(thrustSlider.value).toFixed(2);
    }
    clearTransferOrbits();
}

function clearTransferOrbits() {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl || !plotEl.data) return;
    const names = ['Target Orbit', 'Transfer Phase 1', 'Transfer Phase 2'];
    let indices = [];
    for (let name of names) {
        let idx = plotEl.data.findIndex(t => t.name === name);
        if (idx !== -1) {
            indices.push(idx);
        }
    }
    indices.sort((a, b) => b - a);
    for (let idx of indices) {
        Plotly.deleteTraces('plot-3d', idx);
    }
    const panel = document.getElementById("transfer-results-panel");
    if (panel) panel.style.display = "none";
}

async function executeTransferSolver() {
    const a = parseFloat(document.getElementById("tweaker_a").value);
    const i = parseFloat(document.getElementById("tweaker_i").value);
    const raan = parseFloat(document.getElementById("tweaker_raan").value);
    const body = document.getElementById("tweaker_body").value;
    const type = document.getElementById("transfer_type").value;
    const targetR = parseFloat(document.getElementById("transfer_target_r").value);
    
    // Retrieve mission form defaults
    const wetMassEl = document.getElementById("spacecraft_mass");
    const payloadEl = document.getElementById("payload_mass");
    const ispEl = document.getElementById("isp");
    
    const m0 = wetMassEl ? parseFloat(wetMassEl.value) || 2500.0 : 2500.0;
    const m_payload = payloadEl ? parseFloat(payloadEl.value) || 800.0 : 800.0;
    const isp = ispEl ? parseFloat(ispEl.value) || 320.0 : 320.0;

    let url = "/api/v1/astrodynamics/hohmann";
    let bodyData = {
        r1: a,
        r2: targetR,
        mu_type: body
    };
    
    if (type === "bielliptic") {
        url = "/api/v1/astrodynamics/bielliptic";
        const boostR = parseFloat(document.getElementById("transfer_boost_r").value);
        if (boostR < a || boostR < targetR) {
            alert("Boost apoapsis radius rb must be greater than or equal to both r1 and r2.");
            return;
        }
        bodyData.rb = boostR;
    } else if (type === "lowthrust") {
        url = "/api/v1/astrodynamics/low-thrust-spiral";
        const thrustVal = parseFloat(document.getElementById("transfer_thrust").value);
        bodyData = {
            r1: a,
            r2: targetR,
            thrust_N: thrustVal,
            isp_s: isp,
            m0_kg: m0,
            mu_type: body
        };
    }
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(bodyData)
        });
        
        if (!response.ok) throw new Error("Transfer calculation failed");
        
        const data = await response.json();
        
        // Show results
        const panel = document.getElementById("transfer-results-panel");
        if (panel) panel.style.display = "flex";
        
        const impulsiveDetails = document.getElementById("transfer-impulsive-details");
        const lowthrustDetails = document.getElementById("transfer-lowthrust-details");

        if (type === "lowthrust") {
            if (impulsiveDetails) impulsiveDetails.style.display = "none";
            if (lowthrustDetails) {
                lowthrustDetails.style.display = "block";
                document.getElementById("tr-prop-mass").innerText = `${data.propellant_kg.toFixed(1)} kg`;
                document.getElementById("tr-final-mass").innerText = `${data.final_mass_kg.toFixed(1)} kg`;
            }
            document.getElementById("tr-total-dv").innerText = `${data.delta_v_km_s.toFixed(3)} km/s`;
            document.getElementById("tr-tof").innerText = `${data.burn_time_days.toFixed(2)} days`;
        } else {
            if (impulsiveDetails) impulsiveDetails.style.display = "block";
            if (lowthrustDetails) lowthrustDetails.style.display = "none";
            
            document.getElementById("tr-dv1").innerText = `${data.dv1_km_s.toFixed(3)} km/s`;
            document.getElementById("tr-dv2").innerText = `${data.dv2_km_s.toFixed(3)} km/s`;
            
            const dv3Row = document.getElementById("tr-dv3-row");
            const dv2RowLabel = document.getElementById("tr-dv2-row");
            
            if (type === "bielliptic") {
                dv2RowLabel.innerHTML = `Apoapsis Burn ΔV₂: <strong id="tr-dv2" style="color: var(--primary-color);">${data.dv2_km_s.toFixed(3)} km/s</strong>`;
                if (dv3Row) {
                    dv3Row.style.display = "block";
                    document.getElementById("tr-dv3").innerText = `${data.dv3_km_s.toFixed(3)} km/s`;
                }
            } else {
                dv2RowLabel.innerHTML = `Arrival Burn ΔV₂: <strong id="tr-dv2" style="color: var(--primary-color);">${data.dv2_km_s.toFixed(3)} km/s</strong>`;
                if (dv3Row) dv3Row.style.display = "none";
            }
            
            document.getElementById("tr-total-dv").innerText = `${data.total_dv_km_s.toFixed(3)} km/s`;
            document.getElementById("tr-tof").innerText = `${data.tof_days.toFixed(2)} days`;
        }
        
        // Plot traces
        plotTransferOrbits(data, type, i, raan, body);
        
    } catch (err) {
        console.error(err);
        alert("Error solving circular orbital transfer.");
    }
}

function plotTransferOrbits(data, type, i, raan, body) {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl) return;

    const iRad = (i * Math.PI) / 180.0;
    const omega = (raan * Math.PI) / 180.0;
    const cosO = Math.cos(omega);
    const sinO = Math.sin(omega);
    const cosi = Math.cos(iRad);
    const sini = Math.sin(iRad);

    const thetaSteps = 120;
    const traces = [];

    // 1. Target Orbit (circular radius r2)
    const targetX = [];
    const targetY = [];
    const targetZ = [];
    const r2 = data.r2;

    for (let k = 0; k <= thetaSteps; k++) {
        const theta = (k * 2.0 * Math.PI) / thetaSteps;
        const xP = r2 * Math.cos(theta);
        const yP = r2 * Math.sin(theta);
        
        const xRot = xP * cosO - yP * sinO * cosi;
        const yRot = xP * sinO + yP * cosO * cosi;
        const zRot = yP * sini;
        
        targetX.push(xRot);
        targetY.push(yRot);
        targetZ.push(zRot);
    }

    traces.push({
        type: 'scatter3d',
        mode: 'lines',
        name: 'Target Orbit',
        x: targetX,
        y: targetY,
        z: targetZ,
        line: { color: '#f97316', width: 3, dash: 'dot' }
    });

    if (type === 'hohmann') {
        // 2. Hohmann Transfer Ellipse (half-ellipse from r1 to r2)
        const transX = [];
        const transY = [];
        const transZ = [];
        const a = data.a_trans_km;
        const e = data.e_trans;

        const startTheta = data.r1 < data.r2 ? 0.0 : Math.PI;
        const endTheta = data.r1 < data.r2 ? Math.PI : 2.0 * Math.PI;

        for (let k = 0; k <= thetaSteps; k++) {
            const theta = startTheta + (k * (endTheta - startTheta)) / thetaSteps;
            const denom = 1.0 + e * Math.cos(theta);
            const r = (a * (1.0 - e * e)) / denom;

            const xP = r * Math.cos(theta);
            const yP = r * Math.sin(theta);

            const xRot = xP * cosO - yP * sinO * cosi;
            const yRot = xP * sinO + yP * cosO * cosi;
            const zRot = yP * sini;

            transX.push(xRot);
            transY.push(yRot);
            transZ.push(zRot);
        }

        traces.push({
            type: 'scatter3d',
            mode: 'lines',
            name: 'Transfer Phase 1',
            x: transX,
            y: transY,
            z: transZ,
            line: { color: '#ec4899', width: 3, dash: 'dash' }
        });

    } else if (type === 'bielliptic') {
        // 3. Bi-elliptic: Ellipse 1 (r1 -> rb) goes from periapsis (theta=0) to apoapsis (theta=pi)
        const trans1X = [];
        const trans1Y = [];
        const trans1Z = [];
        const a1 = data.a1_km;
        const e1 = data.e1;

        for (let k = 0; k <= thetaSteps; k++) {
            const theta = (k * Math.PI) / thetaSteps;
            const denom = 1.0 + e1 * Math.cos(theta);
            const r = (a1 * (1.0 - e1 * e1)) / denom;

            const xP = r * Math.cos(theta);
            const yP = r * Math.sin(theta);

            const xRot = xP * cosO - yP * sinO * cosi;
            const yRot = xP * sinO + yP * cosO * cosi;
            const zRot = yP * sini;

            trans1X.push(xRot);
            trans1Y.push(yRot);
            trans1Z.push(zRot);
        }

        traces.push({
            type: 'scatter3d',
            mode: 'lines',
            name: 'Transfer Phase 1',
            x: trans1X,
            y: trans1Y,
            z: trans1Z,
            line: { color: '#ec4899', width: 3, dash: 'dash' }
        });

        // 4. Bi-elliptic: Ellipse 2 (rb -> r2) goes from apoapsis (theta=pi) to periapsis (theta=2*pi)
        const trans2X = [];
        const trans2Y = [];
        const trans2Z = [];
        const a2 = data.a2_km;
        const e2 = data.e2;

        for (let k = 0; k <= thetaSteps; k++) {
            const theta = Math.PI + (k * Math.PI) / thetaSteps;
            const denom = 1.0 + e2 * Math.cos(theta);
            const r = (a2 * (1.0 - e2 * e2)) / denom;

            const xP = r * Math.cos(theta);
            const yP = r * Math.sin(theta);

            const xRot = xP * cosO - yP * sinO * cosi;
            const yRot = xP * sinO + yP * cosO * cosi;
            const zRot = yP * sini;

            trans2X.push(xRot);
            trans2Y.push(yRot);
            trans2Z.push(zRot);
        }

        traces.push({
            type: 'scatter3d',
            mode: 'lines',
            name: 'Transfer Phase 2',
            x: trans2X,
            y: trans2Y,
            z: trans2Z,
            line: { color: '#06b6d4', width: 3, dash: 'dash' }
        });
    } else if (type === 'lowthrust') {
        // 5. Low-Thrust Spiral (multi-revolution spiral from r1 to r2)
        const transX = [];
        const transY = [];
        const transZ = [];
        const r1 = data.r1;
        const r2 = data.r2;

        const numRevs = 8;
        const totalSteps = numRevs * 120;

        for (let k = 0; k <= totalSteps; k++) {
            const theta = (k * 2.0 * Math.PI) / 120.0;
            const r = r1 + (r2 - r1) * (k / totalSteps);

            const xP = r * Math.cos(theta);
            const yP = r * Math.sin(theta);

            const xRot = xP * cosO - yP * sinO * cosi;
            const yRot = xP * sinO + yP * cosO * cosi;
            const zRot = yP * sini;

            transX.push(xRot);
            transY.push(yRot);
            transZ.push(zRot);
        }

        traces.push({
            type: 'scatter3d',
            mode: 'lines',
            name: 'Transfer Phase 1',
            x: transX,
            y: transY,
            z: transZ,
            line: { color: '#ec4899', width: 3, dash: 'dash' }
        });
    }

    if (plotEl.data) {
        const names = ['Target Orbit', 'Transfer Phase 1', 'Transfer Phase 2'];
        let indices = [];
        for (let name of names) {
            let idx = plotEl.data.findIndex(t => t.name === name);
            if (idx !== -1) {
                indices.push(idx);
            }
        }
        indices.sort((a, b) => b - a);
        for (let idx of indices) {
            Plotly.deleteTraces('plot-3d', idx);
        }
        
        Plotly.addTraces('plot-3d', traces);
    }
}

function toggleMonteCarloControls() {
    // Monte Carlo controls are always visible in the sidebar, so this is a placeholder.
}

function onMonteCarloParamsChange() {
    const runs = document.getElementById("mc_runs").value;
    const posStd = document.getElementById("mc_pos_std").value;
    const velStd = document.getElementById("mc_vel_std").value;
    const duration = document.getElementById("mc_duration").value;

    setElementText("val_mc_runs", runs);
    setElementText("val_mc_pos_std", posStd);
    setElementText("val_mc_vel_std", velStd);
    setElementText("val_mc_duration", duration);

    clearMonteCarlo();
}

function clearMonteCarlo() {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl || !plotEl.data) return;
    let indices = [];
    for (let idx = 0; idx < plotEl.data.length; idx++) {
        const name = plotEl.data[idx].name || '';
        if (name === 'MC Nominal' || name.startsWith('MC Perturbed Run')) {
            indices.push(idx);
        }
    }
    indices.sort((a, b) => b - a);
    for (let idx of indices) {
        Plotly.deleteTraces('plot-3d', idx);
    }
}

async function executeMonteCarlo() {
    const a = parseFloat(document.getElementById("tweaker_a").value);
    const e = parseFloat(document.getElementById("tweaker_e").value);
    const i = parseFloat(document.getElementById("tweaker_i").value);
    const raan = parseFloat(document.getElementById("tweaker_raan").value);
    const body = document.getElementById("tweaker_body").value;

    const runs = parseInt(document.getElementById("mc_runs").value);
    const posStd = parseFloat(document.getElementById("mc_pos_std").value);
    const velStd = parseFloat(document.getElementById("mc_vel_std").value);
    const duration = parseFloat(document.getElementById("mc_duration").value);

    const btn = document.getElementById("btn-run-mc");
    const oldText = btn.innerText;
    btn.innerText = "Running MC...";
    btn.disabled = true;

    try {
        const response = await fetch("/api/v1/astrodynamics/monte-carlo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                a: a,
                e: e,
                i: i,
                omega: 0.0,
                raan: raan,
                mu_type: body,
                duration_days: duration,
                runs: runs,
                pos_std_km: posStd,
                vel_std_m_s: velStd
            })
        });

        if (!response.ok) throw new Error("Monte Carlo simulation failed");

        const data = await response.json();

        plotMonteCarloTraces(data);
        plotMonteCarloChart(data);

    } catch (err) {
        console.error(err);
        alert("Error executing Monte Carlo dispersion simulation.");
    } finally {
        btn.innerText = oldText;
        btn.disabled = false;
    }
}

function plotMonteCarloTraces(data) {
    const plotEl = document.getElementById('plot-3d');
    if (!plotEl) return;

    const traces = [];

    // Nominal Path
    const nomX = data.nominal_path.map(p => p[0]);
    const nomY = data.nominal_path.map(p => p[1]);
    const nomZ = data.nominal_path.map(p => p[2]);

    traces.push({
        type: 'scatter3d',
        mode: 'lines',
        name: 'MC Nominal',
        x: nomX,
        y: nomY,
        z: nomZ,
        line: { color: '#10b981', width: 3 } // green
    });

    // Perturbed Paths
    data.perturbed_paths.forEach((path, idx) => {
        const pertX = path.map(p => p[0]);
        const pertY = path.map(p => p[1]);
        const pertZ = path.map(p => p[2]);

        traces.push({
            type: 'scatter3d',
            mode: 'lines',
            name: `MC Perturbed Run ${idx + 1}`,
            x: pertX,
            y: pertY,
            z: pertZ,
            line: { color: '#f43f5e', width: 2 }, // rose color
            opacity: 0.3
        });
    });

    if (plotEl.data) {
        // Clear existing MC traces first
        clearMonteCarlo();
        Plotly.addTraces('plot-3d', traces);
    }
}

function plotMonteCarloChart(data) {
    const trace = {
        x: data.t_days,
        y: data.envelope_3sigma_km,
        mode: 'lines',
        name: '3σ Dispersion',
        line: { color: '#f43f5e', width: 3 }
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        margin: { l: 50, r: 20, t: 40, b: 40 },
        title: { text: '3σ Trajectory Uncertainty Growth', font: { color: '#cbd5e1', size: 14 } },
        xaxis: { title: 'Time (days)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis: { title: 'Dispersion Magnitude (km)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' }
    };

    Plotly.newPlot('plot-secondary', [trace], layout, { responsive: true });
}



// ═══════════════════════════════════════════════════════════════════════════════
//  DIAGNOSTIC TAB SWITCHER
// ═══════════════════════════════════════════════════════════════════════════════

/**
 * Switches the active diagnostic tab.
 * @param {string} name - Tab key: 'ekf' | 'ccsds' | 'anomaly' | 'vacuum' | 'erosion'
 */
function switchDiagTab(name) {
    const tabs    = ['ekf', 'ccsds', 'anomaly', 'vacuum', 'erosion'];
    const buttons = document.querySelectorAll('.diag-tab');
    
    tabs.forEach((t) => {
        const content = document.getElementById(`diag-${t}`);
        const btn     = document.getElementById(`tab-${t}`);
        if (content) content.style.display = (t === name) ? '' : 'none';
        if (btn)     btn.classList.toggle('active', t === name);
    });
}


// ═══════════════════════════════════════════════════════════════════════════════
//  HELPER: SET DIAGNOSTIC STATUS BADGE
// ═══════════════════════════════════════════════════════════════════════════════

function setDiagStatus(id, message, isError = false) {
    const el = document.getElementById(id);
    if (!el) return;
    el.style.display  = 'block';
    el.className      = `diag-status ${isError ? 'err' : 'ok'}`;
    el.textContent    = message;
}

function clearDiagStatus(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
}


// ═══════════════════════════════════════════════════════════════════════════════
//  1.  EKF FILTER SIMULATION
// ═══════════════════════════════════════════════════════════════════════════════

async function runEKFSimulation() {
    const btn = document.getElementById('btn-run-ekf');
    btn.disabled    = true;
    btn.textContent = '⏳ Running…';
    clearDiagStatus('ekf-status');

    const payload = {
        orbit_radius_km:     parseFloat(document.getElementById('ekf_orbit_radius').value),
        steps:               parseInt(document.getElementById('ekf_steps').value, 10),
        dt_s:                parseFloat(document.getElementById('ekf_dt').value),
        measurement_noise_km: parseFloat(document.getElementById('ekf_meas_noise').value),
        fault_step:          parseInt(document.getElementById('ekf_fault_step').value, 10),
        fault_magnitude_km:  parseFloat(document.getElementById('ekf_fault_mag').value)
    };

    try {
        const res  = await fetch('/api/v1/digital-twin/ekf-simulate', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(`Server: ${res.status}`);
        const data = await res.json();
        plotEKFResults(data);
        setDiagStatus('ekf-status', `✔ EKF completed — ${data.true_pos.length} steps simulated.`);
    } catch (err) {
        setDiagStatus('ekf-status', `✖ ${err.message}`, true);
    } finally {
        btn.disabled    = false;
        btn.textContent = '⚡ Run EKF Filter';
    }
}

function plotEKFResults(data) {
    const t = data.t;
    const traceTrue = {
        x: t, y: data.true_pos, mode: 'lines', name: 'True Position (X)',
        line: { color: '#10b981', width: 2 }
    };
    const traceEst = {
        x: t, y: data.estimated_pos, mode: 'lines', name: 'EKF Estimate',
        line: { color: '#3b82f6', width: 2, dash: 'dash' }
    };
    const traceMeas = {
        x: t, y: data.measured_pos, mode: 'markers', name: 'Noisy Measurement',
        marker: { color: 'rgba(249,115,22,0.55)', size: 3 }
    };
    const traceCov = {
        x: t, y: data.covariance_trace, mode: 'lines', name: 'Cov Trace',
        line: { color: '#a855f7', width: 1.5, dash: 'dot' },
        yaxis: 'y2'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor:  'rgba(0,0,0,0)',
        margin: { l: 54, r: 54, t: 36, b: 40 },
        title:  { text: 'EKF State Estimation vs True Orbit', font: { color: '#cbd5e1', size: 13 } },
        legend: { font: { color: '#9ca3af', size: 10 }, bgcolor: 'rgba(0,0,0,0)' },
        xaxis:  { title: 'Time (s)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis:  { title: 'Position X (km)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis2: { title: 'Cov Trace', overlaying: 'y', side: 'right', color: '#a855f7', showgrid: false }
    };

    Plotly.newPlot('plot-ekf', [traceTrue, traceEst, traceMeas, traceCov], layout, { responsive: true });
}


// ═══════════════════════════════════════════════════════════════════════════════
//  2.  CCSDS PACKET PARSER
// ═══════════════════════════════════════════════════════════════════════════════

async function parseCCSDSPacket() {
    const btn = document.getElementById('btn-parse-ccsds');
    btn.disabled    = true;
    btn.textContent = '⏳ Parsing…';
    clearDiagStatus('ccsds-status');

    const hex = document.getElementById('ccsds_hex').value.trim().replace(/\s+/g, '');

    try {
        const res  = await fetch('/api/v1/digital-twin/ccsds-parse', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ hex_packet: hex })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        renderCCSDSResults(data);
        setDiagStatus('ccsds-status', '✔ Packet decoded successfully.');
    } catch (err) {
        setDiagStatus('ccsds-status', `✖ ${err.message}`, true);
    } finally {
        btn.disabled    = false;
        btn.textContent = '📡 Parse Packet';
    }
}

function renderCCSDSResults(data) {
    const container = document.getElementById('ccsds-results');
    
    const rows = Object.entries(data).map(([k, v]) => {
        const displayVal = (typeof v === 'object') ? JSON.stringify(v) : String(v);
        return `<tr><td>${k}</td><td>${displayVal}</td></tr>`;
    }).join('');

    container.innerHTML = `
        <table class="diag-results-table">
            <thead><tr><th>Field</th><th>Value</th></tr></thead>
            <tbody>${rows}</tbody>
        </table>`;
}


// ═══════════════════════════════════════════════════════════════════════════════
//  3.  AI ANOMALY FORECASTING
// ═══════════════════════════════════════════════════════════════════════════════

async function runAnomalyForecast() {
    const btn = document.getElementById('btn-anomaly-forecast');
    btn.disabled    = true;
    btn.textContent = '⏳ Forecasting…';
    clearDiagStatus('anomaly-status');

    const historyRaw = document.getElementById('anomaly_history').value;
    const history    = historyRaw.split(',').map(s => parseFloat(s.trim())).filter(n => !isNaN(n));

    const payload = {
        param_name:  document.getElementById('anomaly_param').value.trim(),
        history:     history,
        steps_future: parseInt(document.getElementById('anomaly_steps').value, 10),
        safety_min:  parseFloat(document.getElementById('anomaly_min').value),
        safety_max:  parseFloat(document.getElementById('anomaly_max').value)
    };

    try {
        const res  = await fetch('/api/v1/digital-twin/anomaly-predict', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        plotAnomalyResults(data, history, payload);
        const anomalyTxt = data.is_anomaly ? '⚠️ ANOMALY DETECTED' : '✔ No anomaly detected';
        setDiagStatus('anomaly-status', `${anomalyTxt} — Forecast[+1]: ${data.forecast_value?.toFixed(2) ?? 'N/A'}`, data.is_anomaly);
    } catch (err) {
        setDiagStatus('anomaly-status', `✖ ${err.message}`, true);
    } finally {
        btn.disabled    = false;
        btn.textContent = '🔮 Run Forecast';
    }
}

function plotAnomalyResults(data, history, payload) {
    const histLen  = history.length;
    const tHist    = Array.from({ length: histLen }, (_, i) => i);
    const tForecast= Array.from({ length: data.forecast_sequence.length }, (_, i) => histLen + i);

    const traceHist = {
        x: tHist, y: history, mode: 'lines+markers', name: 'Telemetry History',
        line: { color: '#3b82f6', width: 2 }, marker: { size: 4 }
    };
    const traceFore = {
        x: tForecast, y: data.forecast_sequence, mode: 'lines+markers', name: 'AI Forecast',
        line: { color: data.is_anomaly ? '#ef4444' : '#10b981', width: 2, dash: 'dash' },
        marker: { size: 5, symbol: 'diamond' }
    };

    const safeZone = {
        type: 'rect', xref: 'paper', yref: 'y',
        x0: 0, x1: 1, y0: payload.safety_min, y1: payload.safety_max,
        fillcolor: 'rgba(16,185,129,0.06)', line: { color: 'rgba(16,185,129,0.2)', width: 1 },
        layer: 'below'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor:  'rgba(0,0,0,0)',
        margin: { l: 54, r: 20, t: 36, b: 40 },
        title:  { text: `Anomaly Forecast — ${payload.param_name}`, font: { color: '#cbd5e1', size: 13 } },
        legend: { font: { color: '#9ca3af', size: 10 }, bgcolor: 'rgba(0,0,0,0)' },
        shapes: [safeZone],
        xaxis:  { title: 'Step Index', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis:  { title: payload.param_name, color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' }
    };

    Plotly.newPlot('plot-anomaly', [traceHist, traceFore], layout, { responsive: true });
}


// ═══════════════════════════════════════════════════════════════════════════════
//  4.  VACUUM CHAMBER SIMULATION
// ═══════════════════════════════════════════════════════════════════════════════

async function runVacuumSim() {
    const btn = document.getElementById('btn-run-vacuum');
    btn.disabled    = true;
    btn.textContent = '⏳ Simulating…';
    clearDiagStatus('vacuum-status');

    const payload = {
        p_init_torr:        parseFloat(document.getElementById('vac_p_init').value),
        leak_rate_torr_l_s: parseFloat(document.getElementById('vac_leak').value),
        pump_speed_l_s:     parseFloat(document.getElementById('vac_pump').value),
        volume_l:           parseFloat(document.getElementById('vac_volume').value),
        duration_s:         parseFloat(document.getElementById('vac_duration').value)
    };

    try {
        const res  = await fetch('/api/v1/propulsion/vacuum-simulate', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        plotVacuumResults(data, payload);
        const finalP = data.p[data.p.length - 1];
        setDiagStatus('vacuum-status', `✔ Final pressure: ${finalP.toExponential(3)} Torr`);
    } catch (err) {
        setDiagStatus('vacuum-status', `✖ ${err.message}`, true);
    } finally {
        btn.disabled    = false;
        btn.textContent = '🔬 Run Vacuum Sim';
    }
}

function plotVacuumResults(data, payload) {
    const trace = {
        x: data.t, y: data.p, mode: 'lines', name: 'Chamber Pressure',
        line: { color: '#06b6d4', width: 2.5 },
        fill: 'tozeroy', fillcolor: 'rgba(6,182,212,0.08)'
    };

    const layout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor:  'rgba(0,0,0,0)',
        margin: { l: 64, r: 20, t: 36, b: 40 },
        title:  { text: 'Vacuum Chamber Pressure Decay', font: { color: '#cbd5e1', size: 13 } },
        legend: { font: { color: '#9ca3af' }, bgcolor: 'rgba(0,0,0,0)' },
        xaxis:  { title: 'Time (s)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)' },
        yaxis:  { title: 'Pressure (Torr)', color: '#9ca3af', gridcolor: 'rgba(255,255,255,0.05)', type: 'log' }
    };

    Plotly.newPlot('plot-vacuum', [trace], layout, { responsive: true });
}


// ═══════════════════════════════════════════════════════════════════════════════
//  5.  ION THRUSTER GRID EROSION RATE
// ═══════════════════════════════════════════════════════════════════════════════

async function calcErosionRate() {
    const btn = document.getElementById('btn-calc-erosion');
    btn.disabled    = true;
    btn.textContent = '⏳ Calculating…';
    clearDiagStatus('erosion-status');

    const payload = {
        material_name:        document.getElementById('erosion_material').value,
        ion_energy_eV:        parseFloat(document.getElementById('erosion_energy').value),
        current_density_a_m2: parseFloat(document.getElementById('erosion_current').value)
    };

    try {
        const res  = await fetch('/api/v1/propulsion/erosion-rate', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify(payload)
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || `HTTP ${res.status}`);
        }
        const data = await res.json();
        renderErosionResults(data, payload);
        setDiagStatus('erosion-status', `✔ Erosion rate: ${data.erosion_rate_um_hr?.toFixed(4) ?? 'N/A'} µm/hr`);
    } catch (err) {
        setDiagStatus('erosion-status', `✖ ${err.message}`, true);
    } finally {
        btn.disabled    = false;
        btn.textContent = '⚗️ Calculate Erosion Rate';
    }
}

function renderErosionResults(data, payload) {
    const container = document.getElementById('erosion-results');
    const rate      = data.erosion_rate_um_hr;
    const matInfo   = data.material_info || {};

    const matRows = Object.entries(matInfo).map(([k, v]) =>
        `<tr><td>${k}</td><td>${typeof v === 'object' ? JSON.stringify(v) : v}</td></tr>`
    ).join('');

    container.innerHTML = `
        <div class="erosion-metric">
            <span class="rate-value">${rate != null ? rate.toFixed(3) : 'N/A'}</span>
            <span class="rate-unit">µm / hour  ·  ${payload.material_name.toUpperCase()}</span>
        </div>
        <table class="diag-results-table" style="margin-top:16px;">
            <thead><tr><th>Material Property</th><th>Value</th></tr></thead>
            <tbody>${matRows}</tbody>
        </table>`;
}

