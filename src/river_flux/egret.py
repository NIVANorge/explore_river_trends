import subprocess
import tempfile
from pathlib import Path

import pandas as pd


def run_egret(
    sample_file,
    daily_file,
    script_file,
    timeout=3600,
):
    """
    Run EGRET/WRTDS model in R.

    Parameters
    ----------
    sample_file : str or Path
        Sample chemistry CSV.

    daily_file : str or Path
        Daily flow CSV.

    script_file : str or Path
        Path to run_egret.R.

    drain_sqkm : float
        Catchment area.

    timeout : int
        Maximum runtime (seconds).

    Returns
    -------
    pd.DataFrame
        Raw EGRET annual results.
    """

    sample_file = Path(sample_file)
    daily_file = Path(daily_file)
    script_file = Path(script_file)

    with tempfile.TemporaryDirectory() as tmp:

        result_file = Path(tmp) / "egret_results.csv"

        cmd = [
            "Rscript",
            str(script_file),
            str(sample_file),
            str(daily_file),
            str(result_file),
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        if result.stdout:
            print(result.stdout)

        if result.returncode != 0:

            print("\n=== R STDERR ===")
            print(result.stderr)

            raise RuntimeError(f"EGRET script failed (exit code {result.returncode})")

        if not result_file.exists():

            raise FileNotFoundError(f"EGRET output file not created: {result_file}")

        egret_df = pd.read_csv(result_file)

    return egret_df


def clean_egret_output(
    df,
    parameter,
):
    """
    Convert EGRET results to repository
    naming conventions.
    """

    par = parameter.split("_")[0]

    required_cols = [
        "Year",
        "Flux [10^6kg/yr]",
        "FN Flux [10^6kg/yr]",
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:

        raise ValueError("Missing columns in EGRET output: " + ", ".join(missing))

    df = df.copy()

    # Convert million kg to tonnes
    # 1e6 kg / 1000 = 1000 tonnes
    df["Flux [10^6kg/yr]"] *= 1000
    df["FN Flux [10^6kg/yr]"] *= 1000

    df = df.rename(
        columns={
            "Year": "year",
            "Flux [10^6kg/yr]": f"EGRET_{par}_tonn",
            "FN Flux [10^6kg/yr]": f"EGRET_FN_{par}_tonn",
        }
    )

    # EGRET reports water-year endpoints
    # align with calendar year convention
    df["year"] = df["year"] - 1

    return df[
        [
            "year",
            f"EGRET_{par}_tonn",
            f"EGRET_FN_{par}_tonn",
        ]
    ]