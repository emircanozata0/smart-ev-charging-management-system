import random
import pandas as pd
from datetime import datetime
import os


EV_MODELS = [
    {"model": "TOGG T10X", "battery_capacity_kwh": 88.5},
    {"model": "Tesla Model 3", "battery_capacity_kwh": 75},
    {"model": "BMW i4", "battery_capacity_kwh": 83.9},
    {"model": "Hyundai Ioniq 5", "battery_capacity_kwh": 77.4}
]


def generate_charger_data(total_power_limit=120):
    vehicles = []

    for i in range(1, 5):
        ev = EV_MODELS[i - 1]

        battery_level = random.randint(15, 95)
        temperature = random.randint(25, 75)
        voltage = random.randint(380, 420)
        current = random.randint(20, 90)

        power = round((voltage * current) / 1000, 2)

        if temperature > 60:
            status = "Warning: High Temperature"
            recommended_power = round(power * 0.65, 2)

        elif current > 80:
            status = "Warning: Overcurrent"
            recommended_power = round(power * 0.75, 2)

        elif battery_level > 85:
            status = "Battery Nearly Full"
            recommended_power = round(power * 0.50, 2)

        else:
            status = "Charging"
            recommended_power = power

        battery_capacity = ev["battery_capacity_kwh"]

        energy_needed = round(
            ((100 - battery_level) / 100) * battery_capacity,
            2
        )

        if recommended_power > 0:
            estimated_time = round(energy_needed / recommended_power, 2)
        else:
            estimated_time = 0

        vehicles.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "charger_id": f"Charger {i}",
            "ev_model": ev["model"],
            "battery_capacity_kwh": battery_capacity,
            "battery_level": battery_level,
            "energy_needed_kwh": energy_needed,
            "estimated_time_hour": estimated_time,
            "temperature": temperature,
            "voltage": voltage,
            "current": current,
            "power_kw": power,
            "recommended_power_kw": recommended_power,
            "status": status
        })

    df = pd.DataFrame(vehicles)

    total_recommended_power = df["recommended_power_kw"].sum()

    if total_recommended_power > total_power_limit:
        scale_factor = total_power_limit / total_recommended_power

        df["recommended_power_kw"] = round(
            df["recommended_power_kw"] * scale_factor,
            2
        )

        df["estimated_time_hour"] = round(
            df["energy_needed_kwh"] / df["recommended_power_kw"],
            2
        )

    return df


def save_charging_data(df):
    os.makedirs("data", exist_ok=True)

    file_path = "data/charging_log.csv"

    if os.path.exists(file_path):
        try:
            existing_df = pd.read_csv(file_path)

            if list(existing_df.columns) == list(df.columns):
                df.to_csv(
                    file_path,
                    mode="a",
                    header=False,
                    index=False
                )
            else:
                df.to_csv(
                    file_path,
                    index=False
                )

        except Exception:
            df.to_csv(
                file_path,
                index=False
            )

    else:
        df.to_csv(
            file_path,
            index=False
        )