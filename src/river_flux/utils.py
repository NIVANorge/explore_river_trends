from pathlib import Path


def convert_to_mg_per_l(
    values,
    units,
):
    """
    Convert concentration values to mg/L.

    Parameters
    ----------
    values : pandas.Series

    units : str
        Concentration units

    Returns
    -------
    pandas.Series
    """

    units = units.lower()

    conversion_factors = {
        "ug/l": 1 / 1000,
        "mg/l": 1,
    }

    if units not in conversion_factors:

        raise ValueError(f"Unsupported units: {units}")

    return values * conversion_factors[units]


def prepare_model_inputs(
    chem_df,
    flow_df,
    parameter,
    work_dir,
):
    """
    Prepare standard input files for EGRET and GAM.

    Creates:

        samples.csv
        daily.csv

    Concentrations are converted to mg/L,
    regardless of the original units.

    Parameters
    ----------
    chem_df : pandas.DataFrame

    flow_df : pandas.DataFrame

    parameter : str
        e.g.

            TOTN_ug/l
            TOTP_ug/l
            NO3_mg/l

    work_dir : str | Path

    Returns
    -------
    tuple(Path, Path)

        (
            sample_file,
            daily_file
        )
    """

    work_dir = Path(work_dir)

    work_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Extract parameter information
    try:

        par_name, units = parameter.split(
            "_",
            1,
        )

    except ValueError:

        raise ValueError(
            f"Parameter must be in format " f"'NAME_units'. Got '{parameter}'."
        )

    # Restrict chemistry data to flow record period
    q_start = flow_df.index.min()
    q_end = flow_df.index.max()
    chem_df = chem_df.loc[(chem_df.index >= q_start) & (chem_df.index <= q_end)].copy()

    # Output paths
    sample_file = work_dir / "samples.csv"
    daily_file = work_dir / "daily.csv"

    # Chemistry file
    samples = chem_df.reset_index().rename(columns={parameter: "Conc"})
    samples["Conc"] = convert_to_mg_per_l(
        samples["Conc"],
        units,
    )
    samples["remarkCode"] = ""
    samples["date"] = samples["date"].dt.strftime("%Y-%m-%d")
    samples = samples[
        [
            "date",
            "remarkCode",
            "Conc",
        ]
    ]
    samples.to_csv(
        sample_file,
        index=False,
    )

    # Daily flow file
    daily = flow_df.reset_index().rename(columns={"flow_m3/s": "Q"})
    q_offset = daily.loc[
        daily["Q"] > 0,
        "Q",
    ].min()

    print(f"Adding flow offset of " f"{q_offset:.6f} m3/s " f"to avoid zero flows.")

    daily["Q"] += q_offset
    daily["date"] = daily["date"].dt.strftime("%Y-%m-%d")
    daily = daily[
        [
            "date",
            "Q",
        ]
    ]
    daily.to_csv(
        daily_file,
        index=False,
    )

    return (
        sample_file,
        daily_file,
    )