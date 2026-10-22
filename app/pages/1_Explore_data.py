from pathlib import Path

import pandas as pd
import streamlit as st
from utils import load_data

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent.parent
OUTPUT_DIR = PROJECT_DIR / "output"
PLOTS_DIR = OUTPUT_DIR / "plots"

st.set_page_config(
    page_title="Explore data",
    layout="wide",
)

# Load data
fluxes_df, trends_df = load_data()

# Sidebar
st.sidebar.header("Selection")
station = st.sidebar.selectbox(
    "Station code",
    sorted(fluxes_df["station"].unique()),
)
parameter = st.sidebar.selectbox(
    "Parameter",
    sorted(fluxes_df["parameter"].unique()),
)

# Filter data
flux_filt = fluxes_df.loc[
    (fluxes_df["station"] == station) & (fluxes_df["parameter"] == parameter)
].copy()

trend_filt = trends_df.loc[
    (trends_df["station"] == station) & (trends_df["parameter"] == parameter)
].copy()

# Title
st.title(f"{station} | {parameter}")

# Plot
plot_file = PLOTS_DIR / f"{station}_{parameter}_tonnes.png"

if plot_file.exists():
    st.image(str(plot_file), width='stretch')
else:
    st.warning(f"Plot not found: {plot_file.name}")

# Trends
st.subheader("Trend results")
st.download_button(
    label="Download trends CSV",
    data=trend_filt.to_csv(index=False),
    file_name=(f"{station}_{parameter}_trends.csv"),
    mime="text/csv",
)
st.dataframe(
    trend_filt,
    width='stretch',
    hide_index=True,
)

# Fluxes
st.subheader("Annual flux estimates")
st.download_button(
    label="Download flux CSV",
    data=flux_filt.to_csv(index=False),
    file_name=(f"{station}_{parameter}_fluxes.csv"),
    mime="text/csv",
)
st.dataframe(
    flux_filt,
    width='stretch',
    hide_index=True,
)