# ⚡ Smart EV Charging Management System

A real-time EV charging station management dashboard built with Python and Streamlit.

This project simulates a multi-charger EV charging station and provides live monitoring, load balancing, anomaly detection, estimated charging time, charging cost calculation, and historical data analysis.

---

## 🚀 Project Overview

This project was developed to simulate the basic operation of an intelligent EV charging station management system.

The system monitors 4 different EV chargers and simulates real-time values such as:

- Voltage
- Current
- Power consumption
- Battery level
- Charger temperature
- EV model
- Charging status
- Estimated charging time
- Estimated charging cost

The dashboard also includes a rule-based smart charging logic that recommends optimized charging power according to temperature, current, battery level, and grid capacity.

---

## 🎯 Key Features

### 🔌 Multi-Charger Simulation

The system simulates 4 EV charging units at the same time.

### 📊 Real-Time Dashboard

Live dashboard built with Streamlit and Plotly.

### ⚡ Power Calculation

Power is calculated using:

```text
Power (kW) = Voltage × Current / 1000