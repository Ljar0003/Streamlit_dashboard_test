import streamlit as st
import pandas as pd
import time
import random

st.set_page_config(
    page_title='Gas Turbine Dashboard',
    page_icon='⚙️',
)

st.title("Gas Turbine Real-Time Monitoring")
st.image('Gas_turbine_schematic.png')

# Placeholder for live data
placeholder = st.empty()

# Create empty dataframe
data = pd.DataFrame(columns=["Time", "Temperature", "Pressure", "RPM"])
temperatures = pd.DataFrame(columns=["T1","T2","T3","T4","T9"])

start_time = time.time()

while True:
    current_time = time.time() - start_time

    # ---- Simulated sensor values (replace later with real data) ----
    temperature = 400 + random.uniform(-10, 10)   # °C
    pressure = 5 + random.uniform(-0.5, 0.5)      # bar
    rpm = 15000 + random.uniform(-500, 500)       # RPM

    new_row = pd.DataFrame({
        "Time": [current_time],
        "Temperature": [temperature],
        "Pressure": [pressure],
        "RPM": [rpm],
    })

    temp_row = pd.DataFrame({
        "T1": [1],
        "T2": [2],
        "T3": [3],
        "T4": [4],
        "T9": [5]
    })

    data = pd.concat([data, new_row], ignore_index=True)
    temperatures = pd.concat([temperatures,temp_row],ignore_index=True)

    # Keep last 100 points
    data = data.tail(100)
    temperatures = temperatures.tail(100)

    with placeholder.container():
        st.subheader("Live Sensor Values")

        col1, col2, col3 = st.columns(3)

        col1.metric("Temperature (°C)", f"{temperature:.1f}")
        col2.metric("Pressure (bar)", f"{pressure:.2f}")
        col3.metric("Spool Speed (RPM)", f"{rpm:.0f}")

        st.subheader("Trends")

        st.line_chart(data.set_index("Time"))

    time.sleep(1)