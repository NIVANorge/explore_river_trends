from pathlib import Path

import pandas as pd

APP_DIR = Path(__file__).resolve().parent
PROJECT_DIR = APP_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "output"


def load_data():
    fluxes = pd.read_csv(OUTPUT_DIR / "annual_fluxes_tonnes.csv")
    trends = pd.read_csv(OUTPUT_DIR / "trend_results_tonnes.csv").drop(
        columns="intercept"
    )

    return fluxes, trends