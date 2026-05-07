import streamlit as st
import pandas as pd
import time
import random
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Gas Turbine Dashboard',
    page_icon='⚙️',
    layout="wide"
)

st.title("Gas Turbine Real-Time Monitoring")

# ---------------------------------------------------
# SIMULATED BRAYTON CYCLE POINTS
# ---------------------------------------------------
# T1 = Compressor Inlet
# T2 = Compressor Exit
# T3 = Combustor Exit / Turbine Inlet
# T4 = Turbine Exit
# T9 = Exhaust

# Placeholder for live updates
placeholder = st.empty()

# Data storage
history = pd.DataFrame(columns=[
    "Time",
    "T1", "T2", "T3", "T4", "T9",
    "P1", "P2", "P3", "P4", "P9",
    "RPM"
])

start_time = time.time()

# ---------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------
while True:

    current_time = time.time() - start_time

    # ---------------------------------------------------
    # SIMULATED SENSOR VALUES
    # ---------------------------------------------------

    # Temperatures (°C)
    T1 = 25 + random.uniform(-2, 2)
    T2 = 180 + random.uniform(-10, 10)
    T3 = 950 + random.uniform(-20, 20)
    T4 = 600 + random.uniform(-15, 15)
    T9 = 450 + random.uniform(-10, 10)

    # Pressures (bar)
    P1 = 1.0 + random.uniform(-0.05, 0.05)
    P2 = 5.5 + random.uniform(-0.2, 0.2)
    P3 = 5.2 + random.uniform(-0.2, 0.2)
    P4 = 1.4 + random.uniform(-0.05, 0.05)
    P9 = 1.0 + random.uniform(-0.05, 0.05)

    # RPM
    rpm = 15000 + random.uniform(-300, 300)

    # ---------------------------------------------------
    # STORE DATA
    # ---------------------------------------------------
    new_row = pd.DataFrame({
        "Time": [current_time],

        "T1": [T1],
        "T2": [T2],
        "T3": [T3],
        "T4": [T4],
        "T9": [T9],

        "P1": [P1],
        "P2": [P2],
        "P3": [P3],
        "P4": [P4],
        "P9": [P9],

        "RPM": [rpm]
    })

    history = pd.concat([history, new_row], ignore_index=True)

    # Keep last 200 points
    history = history.tail(200)

    # ---------------------------------------------------
    # DASHBOARD DISPLAY
    # ---------------------------------------------------
    with placeholder.container():

        st.header("Live Gas Turbine Cycle")

        # =====================================================
        # SCHEMATIC WITH TEMPERATURE & PRESSURE LABELS
        # =====================================================

        st.markdown("## Brayton Cycle Station Values")

        colA, colB, colC, colD, colE = st.columns(5)

        with colA:
            st.metric("T1", f"{T1:.1f} °C")
            st.metric("P1", f"{P1:.2f} bar")

        with colB:
            st.metric("T2", f"{T2:.1f} °C")
            st.metric("P2", f"{P2:.2f} bar")

        with colC:
            st.metric("T3", f"{T3:.1f} °C")
            st.metric("P3", f"{P3:.2f} bar")

        with colD:
            st.metric("T4", f"{T4:.1f} °C")
            st.metric("P4", f"{P4:.2f} bar")

        with colE:
            st.metric("T9", f"{T9:.1f} °C")
            st.metric("P9", f"{P9:.2f} bar")

        st.metric("Spool Speed", f"{rpm:.0f} RPM")

        # =====================================================
        # TEMPERATURE VS TIME
        # =====================================================

        st.markdown("---")
        st.subheader("Temperature vs Time")

        temp_df = history.set_index("Time")[[
            "T1", "T2", "T3", "T4", "T9"
        ]]

        st.line_chart(temp_df)

        # =====================================================
        # PRESSURE VS TIME
        # =====================================================

        st.subheader("Pressure vs Time")

        pressure_df = history.set_index("Time")[[
            "P1", "P2", "P3", "P4", "P9"
        ]]

        st.line_chart(pressure_df)

        # =====================================================
        # T-s DIAGRAM
        # =====================================================

        st.subheader("Temperature-Entropy (T-s) Diagram")

        # Approximate entropy values for Brayton cycle
        s_vals = [1.0, 1.2, 2.1, 2.4, 1.0]
        T_vals = [T1, T2, T3, T4, T1]

        fig_ts, ax_ts = plt.subplots(figsize=(6,4))

        ax_ts.plot(s_vals, T_vals, marker='o')

        ax_ts.set_xlabel("Entropy (s)")
        ax_ts.set_ylabel("Temperature (°C)")
        ax_ts.set_title("Brayton Cycle T-s Diagram")
        ax_ts.grid(True)

        ax_ts.annotate("1", (s_vals[0], T_vals[0]))
        ax_ts.annotate("2", (s_vals[1], T_vals[1]))
        ax_ts.annotate("3", (s_vals[2], T_vals[2]))
        ax_ts.annotate("4", (s_vals[3], T_vals[3]))

        st.pyplot(fig_ts)

        # =====================================================
        # P-v DIAGRAM
        # =====================================================

        st.subheader("Pressure-Volume (P-v) Diagram")

        # Approximate specific volume values
        v_vals = [1.0, 0.4, 0.45, 1.2, 1.0]
        P_vals = [P1, P2, P3, P4, P1]

        fig_pv, ax_pv = plt.subplots(figsize=(6,4))

        ax_pv.plot(v_vals, P_vals, marker='o')

        ax_pv.set_xlabel("Specific Volume (v)")
        ax_pv.set_ylabel("Pressure (bar)")
        ax_pv.set_title("Brayton Cycle P-v Diagram")
        ax_pv.grid(True)

        ax_pv.annotate("1", (v_vals[0], P_vals[0]))
        ax_pv.annotate("2", (v_vals[1], P_vals[1]))
        ax_pv.annotate("3", (v_vals[2], P_vals[2]))
        ax_pv.annotate("4", (v_vals[3], P_vals[3]))

        st.pyplot(fig_pv)


    time.sleep(0.5)
