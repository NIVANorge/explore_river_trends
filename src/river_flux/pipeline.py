import tempfile

from river_flux.data import load_station_data
from river_flux.egret import clean_egret_output, run_egret
from river_flux.gam import clean_gam_output, run_gam
from river_flux.ospar import run_ospar
from river_flux.plotting import plot_fluxes
from river_flux.trends import calculate_trends
from river_flux.utils import prepare_model_inputs


def run_station_parameter(
    station,
    parameter,
    chemistry_file,
    flow_file,
    wrtds_script,
    gam_script,
):

    chem_df, flow_df = load_station_data(
        station,
        parameter,
        chemistry_file,
        flow_file,
    )

    ospar_df = run_ospar(
        flow_df,
        chem_df,
        parameter,
    )

    with tempfile.TemporaryDirectory() as tmp:

        sample_file, daily_file = prepare_model_inputs(
            chem_df,
            flow_df,
            parameter,
            tmp,
        )

        egret_df = run_egret(
            sample_file,
            daily_file,
            wrtds_script,
        )

        gam_df = run_gam(
            sample_file,
            daily_file,
            gam_script,
        )

    egret_df = clean_egret_output(
        egret_df,
        parameter,
    )

    gam_df = clean_gam_output(
        gam_df,
        parameter,
    )

    combined = (
        ospar_df.merge(
            egret_df,
            on="year",
            how="inner",
        )
        .merge(
            gam_df,
            on="year",
            how="inner",
        )
        .set_index("year")
        .round(1)
    )

    trends = calculate_trends(combined)

    fig = plot_fluxes(
        combined,
        parameter,
        trend_df=trends,
    )

    return {
        "data": combined,
        "trends": trends,
        "figure": fig,
        "ospar": ospar_df,
        "egret": egret_df,
        "gam": gam_df,
    }