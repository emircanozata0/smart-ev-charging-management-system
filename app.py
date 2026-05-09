import streamlit as st
import plotly.express as px
import pandas as pd
import os
from simulator import generate_charger_data, save_charging_data
import time


st.set_page_config(
    page_title="Smart EV Charging Management System",
    page_icon="⚡",
    layout="wide"
)


st.sidebar.title("⚙️ Control Panel")

grid_capacity = st.sidebar.slider(
    "Grid Capacity Limit (kW)",
    min_value=60,
    max_value=200,
    value=120,
    step=10
)

refresh_interval = st.sidebar.slider(
    "Refresh Interval (seconds)",
    min_value=1,
    max_value=10,
    value=3,
    step=1
)

data_logging_enabled = st.sidebar.checkbox(
    "Enable Data Logging",
    value=True
)

cost_per_kwh = st.sidebar.number_input(
    "Electricity Price (TL/kWh)",
    min_value=1.0,
    max_value=20.0,
    value=7.5,
    step=0.5
)

st.sidebar.info(
    "This panel allows the operator to adjust station capacity, refresh rate, electricity price and data logging."
)


st.title("⚡ Smart EV Charging Management System")

st.markdown("""
### 🔋 AI-Based Charging Optimization
Real-time monitoring, anomaly detection, load balancing, grid load analysis, estimated charging cost and historical energy data tracking system for EV charging stations.
""")


placeholder = st.empty()


while True:
    df = generate_charger_data(total_power_limit=grid_capacity)

    df["estimated_cost_tl"] = round(
        df["energy_needed_kwh"] * cost_per_kwh,
        2
    )

    if data_logging_enabled:
        save_charging_data(df)

    total_power = round(df["power_kw"].sum(), 2)
    optimized_power = round(df["recommended_power_kw"].sum(), 2)
    avg_temp = round(df["temperature"].mean(), 2)
    active_chargers = len(df)

    normal_chargers = len(df[df["status"] == "Charging"])
    warning_chargers = active_chargers - normal_chargers

    if total_power > 0:
        station_efficiency = round((optimized_power / total_power) * 100, 2)
    else:
        station_efficiency = 0

    grid_load = round((optimized_power / grid_capacity) * 100, 2)

    with placeholder.container():

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Power", f"{total_power} kW")
        col2.metric("Optimized Power", f"{optimized_power} kW")
        col3.metric("Average Temperature", f"{avg_temp} °C")
        col4.metric("Active Chargers", active_chargers)

        st.divider()

        status_col1, status_col2 = st.columns(2)

        status_col1.metric("Normal Chargers", normal_chargers)
        status_col2.metric("Warning Chargers", warning_chargers)

        if warning_chargers == 0:
            st.success("Station health is normal. No active warnings.")
        else:
            st.warning(f"{warning_chargers} charger(s) require attention.")

        st.divider()

        st.write(f"### ⚡ System Efficiency: {station_efficiency}%")
        st.progress(min(station_efficiency / 100, 1.0))

        st.divider()

        st.subheader("⚡ Grid Load Status")

        if grid_load < 50:
            st.success(f"Grid Load Stable: {grid_load}%")
        elif grid_load < 80:
            st.warning(f"Grid Load Medium: {grid_load}%")
        else:
            st.error(f"Critical Grid Load: {grid_load}%")

        st.progress(min(grid_load / 100, 1.0))

        st.caption(f"Current grid capacity limit: {grid_capacity} kW")

        st.divider()

        st.subheader("🔌 Charger Status Cards")

        card_cols = st.columns(4)

        for index, row in df.iterrows():
            with card_cols[index]:
                if row["status"] == "Charging":
                    st.success(f"✅ {row['charger_id']}")
                else:
                    st.warning(f"⚠️ {row['charger_id']}")

                st.write(f"**EV Model:** {row['ev_model']}")
                st.write(f"**Battery Capacity:** {row['battery_capacity_kwh']} kWh")
                st.write(f"**Battery:** {row['battery_level']}%")
                st.write(f"**Energy Needed:** {row['energy_needed_kwh']} kWh")
                st.write(f"**Estimated Time:** {row['estimated_time_hour']} h")
                st.write(f"**Estimated Cost:** {row['estimated_cost_tl']} TL")
                st.write(f"**Temperature:** {row['temperature']} °C")
                st.write(f"**Voltage:** {row['voltage']} V")
                st.write(f"**Current:** {row['current']} A")
                st.write(f"**Power:** {row['power_kw']} kW")
                st.write(f"**Recommended:** {row['recommended_power_kw']} kW")
                st.write(f"**Status:** {row['status']}")

        st.divider()

        st.subheader("📊 Charger Data Table")
        st.dataframe(df, use_container_width=True)

        st.divider()

        power_chart = px.bar(
            df,
            x="charger_id",
            y=["power_kw", "recommended_power_kw"],
            barmode="group",
            title="Actual Power vs Recommended Power"
        )

        st.plotly_chart(power_chart, use_container_width=True)

        battery_chart = px.line(
            df,
            x="ev_model",
            y="battery_level",
            markers=True,
            title="Battery Levels by EV Model"
        )

        st.plotly_chart(battery_chart, use_container_width=True)

        temp_chart = px.line(
            df,
            x="charger_id",
            y="temperature",
            markers=True,
            title="Charger Temperature Levels"
        )

        st.plotly_chart(temp_chart, use_container_width=True)

        cost_chart = px.bar(
            df,
            x="ev_model",
            y="estimated_cost_tl",
            title="Estimated Charging Cost by EV Model"
        )

        st.plotly_chart(cost_chart, use_container_width=True)

        time_chart = px.bar(
            df,
            x="ev_model",
            y="estimated_time_hour",
            title="Estimated Charging Time by EV Model"
        )

        st.plotly_chart(time_chart, use_container_width=True)

        st.divider()

        st.subheader("🚨 System Alerts")

        alerts = df[df["status"] != "Charging"]

        if alerts.empty:
            st.success("All chargers are operating normally.")
        else:
            for _, row in alerts.iterrows():
                st.warning(
                    f"{row['charger_id']} - {row['status']} | "
                    f"Temperature: {row['temperature']}°C | "
                    f"Current: {row['current']}A | "
                    f"EV Model: {row['ev_model']}"
                )

        st.divider()

        st.subheader("📁 Historical Data Summary")

        log_file = "data/charging_log.csv"

        if os.path.exists(log_file):
            history_df = pd.read_csv(log_file)

            total_records = len(history_df)
            historical_avg_power = round(history_df["power_kw"].mean(), 2)
            historical_max_temp = history_df["temperature"].max()
            total_warning_records = len(history_df[history_df["status"] != "Charging"])

            hist_col1, hist_col2, hist_col3, hist_col4 = st.columns(4)

            hist_col1.metric("Total Records", total_records)
            hist_col2.metric("Historical Avg Power", f"{historical_avg_power} kW")
            hist_col3.metric("Max Temperature", f"{historical_max_temp} °C")
            hist_col4.metric("Total Warnings", total_warning_records)

            history_chart = px.line(
                history_df.tail(50),
                x="time",
                y="power_kw",
                color="charger_id",
                title="Last 50 Power Records"
            )

            st.plotly_chart(history_chart, use_container_width=True)

        else:
            st.info("No historical data found yet.")

        st.divider()

        st.subheader("🤖 AI Optimization Notes")

        if optimized_power < total_power:
            st.info("AI optimization reduced charging power to improve safety and balance station load.")
        else:
            st.info("Charging power is operating within safe and optimal limits.")

    time.sleep(refresh_interval)