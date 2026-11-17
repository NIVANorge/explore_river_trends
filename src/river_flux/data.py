import numpy as np
import pandas as pd


def load_station_data(
    station,
    parameter,
    chemistry_file,
    flow_file,
):
    """
    Read chemistry and flow data for a station.
    """
    chem_df = (
        pd.read_excel(chemistry_file)
        .rename(columns={"sample_date": "date"})
        .query("station_code == @station")[["date", parameter]]
        .set_index("date")
        .resample("D")
        .mean()
        .dropna(subset=[parameter])
    )

    flow_df = (
        pd.read_excel(flow_file)[["date", f"{station}_m3/s"]]
        .set_index("date")
        .resample("D")
        .mean()
        .rename(columns={f"{station}_m3/s": "flow_m3/s"})
    )

    # Make sure the flow series is complete
    flow_df.loc[flow_df["flow_m3/s"] <= 0, "flow_m3/s"] = np.nan
    n_missing_before = flow_df["flow_m3/s"].isna().sum()
    flow_df["flow_m3/s"] = flow_df["flow_m3/s"].interpolate(
        method="linear", limit_area="inside"
    )
    n_missing_after = flow_df["flow_m3/s"].isna().sum()
    n_filled = n_missing_before - n_missing_after

    if n_filled > 0:
        print(f"WARNING: {n_filled} flow days filled by linear interpolation.")

    return chem_df, flow_df