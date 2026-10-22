import subprocess
import tempfile
from pathlib import Path

import pandas as pd


def run_gam(
    sample_file,
    daily_file,
    script_file,
    timeout=3600,
):
    """
    Run GAM flux estimation in R.

    Parameters
    ----------
    sample_file : str or Path
        Sample chemistry CSV.

    daily_file : str or Path
        Daily flow CSV.

    script_file : str or Path
        Path to run_gam.R.

    timeout : int
        Maximum runtime (seconds).

    Returns
    -------
    pd.DataFrame
        Annual GAM results.
    """

    sample_file = Path(sample_file)
    daily_file = Path(daily_file)
    script_file = Path(script_file)

    with tempfile.TemporaryDirectory() as tmp:

        result_file = Path(tmp) / "gam_results.csv"

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

            raise RuntimeError(f"GAM script failed (exit code {result.returncode})")

        if not result_file.exists():

            raise FileNotFoundError(f"GAM output file not created: {result_file}")

        gam_df = pd.read_csv(result_file)

    return gam_df


def clean_gam_output(
    df,
    parameter,
):
    """
    Rename GAM output columns to match
    repository naming conventions.
    """

    par = parameter.split("_")[0]

    required_cols = [
        "year",
        "load_tonnes",
        "lower_tonnes",
        "upper_tonnes",
    ]

    missing = [col for col in required_cols if col not in df.columns]

    if missing:

        raise ValueError("Missing columns in GAM output: " + ", ".join(missing))

    df = (
        df[required_cols]
        .copy()
        .rename(
            columns={
                "load_tonnes": f"GAM_{par}_tonn",
                "lower_tonnes": f"lower_GAM_{par}_tonn",
                "upper_tonnes": f"upper_GAM_{par}_tonn",
            }
        )
    )

    return df