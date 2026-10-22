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

    return chem_df, flow_df