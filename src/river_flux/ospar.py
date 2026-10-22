import nivapy3 as nivapy


def run_ospar(
    flow_df,
    chem_df,
    parameter,
):

    par = parameter.split("_")[0]

    df = (
        nivapy.stats.estimate_fluxes(
            flow_df,
            chem_df,
            base_freq="D",
            agg_freq="YE",
            method="ospar_annual",
        )
        .dropna(how="all")
        .reset_index()
    )

    df[f"OSPAR_{par}_tonn"] = df[f"{par}_kg"] / 1000

    df.drop(
        columns=[f"{par}_kg"],
        inplace=True,
    )

    return df[
        [
            "year",
            f"OSPAR_{par}_tonn",
        ]
    ]