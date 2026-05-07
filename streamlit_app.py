import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import random
from PIL import Image, ImageDraw

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Gas Turbine Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# ==========================================================
# DARK THEME STYLING
# ==========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #0b1220;
    color: white;
}

.metric-card {
    background-color: #111827;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #1f2937;
    margin-bottom: 10px;
}

.station-card {
    background-color: #111827;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #1f2937;
}

h1, h2, h3 {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# TITLE
# ==========================================================

st.title("⚙️ Gas Turbine Real-Time Monitoring")

# ==========================================================
# DATA STORAGE
# ==========================================================

if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=[
        "Time",
        "T1", "T2", "T3", "T4", "T9",
        "P1", "P2", "P3", "P4", "P9",
        "RPM"
    ])

history = st.session_state.history

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Live Sensor Values")

    # Simulated values
    T1 = 25 + random.uniform(-2, 2)
    T2 = 180 + random.uniform(-10, 10)
    T3 = 950 + random.uniform(-20, 20)
    T4 = 600 + random.uniform(-15, 15)
    T9 = 450 + random.uniform(-10, 10)

    P1 = 1.0 + random.uniform(-0.05, 0.05)
    P2 = 5.5 + random.uniform(-0.2, 0.2)
    P3 = 5.2 + random.uniform(-0.2, 0.2)
    P4 = 1.4 + random.uniform(-0.05, 0.05)
    P9 = 1.0 + random.uniform(-0.05, 0.05)

    rpm = 15000 + random.uniform(-300, 300)

    st.markdown(f"""
    <div class="metric-card">
    <h4>Ambient Temperature</h4>
    <h2 style="color:#4ade80;">{T1:.1f} °C</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
    <h4>Ambient Pressure</h4>
    <h2 style="color:#4ade80;">{P1:.2f} bar</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
    <h4>Spool Speed</h4>
    <h2 style="color:#4ade80;">{rpm:.0f} RPM</h2>
    </div>
    """, unsafe_allow_html=True)

# ==========================================================
# STORE HISTORY
# ==========================================================

current_time = time.time()

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
history = history.tail(200)

st.session_state.history = history

# ==========================================================
# BRAYTON CYCLE IMAGE WITH OVERLAID VALUES
# ==========================================================

st.subheader("Brayton Cycle Overview")

img = Image.open("Gas_turbine_schematic.png").convert("RGB")
draw = ImageDraw.Draw(img)

# Text positions
positions = {
    "1": (40, 380),
    "2": (430, 170),
    "3": (1080, 170),
    "4": (1150, 390),
    "9": (1490, 390),
}

# Draw temperature & pressure values
draw.text(
    positions["1"],
    f"T1={T1:.1f}C\nP1={P1:.2f}bar",
    fill=(255,140,0)
)

draw.text(
    positions["2"],
    f"T2={T2:.1f}C\nP2={P2:.2f}bar",
    fill=(255,140,0)
)

draw.text(
    positions["3"],
    f"T3={T3:.1f}C\nP3={P3:.2f}bar",
    fill=(255,140,0)
)

draw.text(
    positions["4"],
    f"T4={T4:.1f}C\nP4={P4:.2f}bar",
    fill=(255,140,0)
)

draw.text(
    positions["9"],
    f"T9={T9:.1f}C\nP9={P9:.2f}bar",
    fill=(255,140,0)
)

st.image(img, use_container_width=True)

# ==========================================================
# CHARTS
# ==========================================================

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# TEMPERATURE PLOT
# ----------------------------------------------------------

with col1:

    st.subheader("Temperature vs Time")

    fig1, ax1 = plt.subplots(figsize=(6,4))

    ax1.plot(history["T1"], label="T1")
    ax1.plot(history["T2"], label="T2")
    ax1.plot(history["T3"], label="T3")
    ax1.plot(history["T4"], label="T4")
    ax1.plot(history["T9"], label="T9")

    ax1.set_ylabel("Temperature (°C)")
    ax1.grid(True)
    ax1.legend()

    st.pyplot(fig1)

# ----------------------------------------------------------
# PRESSURE PLOT
# ----------------------------------------------------------

with col2:

    st.subheader("Pressure vs Time")

    fig2, ax2 = plt.subplots(figsize=(6,4))

    ax2.plot(history["P1"], label="P1")
    ax2.plot(history["P2"], label="P2")
    ax2.plot(history["P3"], label="P3")
    ax2.plot(history["P4"], label="P4")
    ax2.plot(history["P9"], label="P9")

    ax2.set_ylabel("Pressure (bar)")
    ax2.grid(True)
    ax2.legend()

    st.pyplot(fig2)

# ==========================================================
# THERMODYNAMIC DIAGRAMS
# ==========================================================

col3, col4 = st.columns(2)

# ----------------------------------------------------------
# T-S DIAGRAM
# ----------------------------------------------------------

with col3:

    st.subheader("T-s Diagram")

    s = [1.0, 1.2, 2.3, 2.6, 1.0]
    T = [T1, T2, T3, T4, T1]

    fig3, ax3 = plt.subplots(figsize=(5,4))

    ax3.plot(s, T, marker='o')

    for i in range(4):
        ax3.text(s[i], T[i], str(i+1))

    ax3.set_xlabel("Entropy")
    ax3.set_ylabel("Temperature (°C)")
    ax3.grid(True)

    st.pyplot(fig3)

# ----------------------------------------------------------
# P-V DIAGRAM
# ----------------------------------------------------------

with col4:

    st.subheader("P-v Diagram")

    v = [1.0, 0.45, 0.5, 1.3, 1.0]
    P = [P1, P2, P3, P4, P1]

    fig4, ax4 = plt.subplots(figsize=(5,4))

    ax4.plot(v, P, marker='o')

    for i in range(4):
        ax4.text(v[i], P[i], str(i+1))

    ax4.set_xlabel("Specific Volume")
    ax4.set_ylabel("Pressure (bar)")
    ax4.grid(True)

    st.pyplot(fig4)

# ==========================================================
# SUMMARY TABLE
# ==========================================================

st.subheader("Station Summary")

summary = pd.DataFrame({
    "Point": ["1","2","3","4","9"],
    "Temperature (°C)": [
        round(T1,1),
        round(T2,1),
        round(T3,1),
        round(T4,1),
        round(T9,1)
    ],
    "Pressure (bar)": [
        round(P1,2),
        round(P2,2),
        round(P3,2),
        round(P4,2),
        round(P9,2)
    ]
})

st.dataframe(summary, use_container_width=True)

# ==========================================================
# AUTO REFRESH
# ==========================================================

time.sleep(1)

