# SCADA Dashboard Simulator

This project simulates a SCADA (Supervisory Control and Data Acquisition) dashboard for monitoring wind turbine sites. It mimics real-time data updates for wind speed and power output using Python's Dash framework, intended for educational and prototyping purposes.

## Features

- Simulated real-time updates every 30 seconds
- Site drill-down via dropdown (Genesis, Foster, Whirl)
- Line graphs for Wind Speed (m/s) and Power Output (MW)
- Easily extendable to support more SCADA-style metrics

## Tech Stack

- Python 3.x
- Dash by Plotly
- Pandas & NumPy for fake data generation

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/scada-dashboard-sim.git
   cd scada-dashboard-sim
