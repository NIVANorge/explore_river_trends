import nivapy3 as nivapy
import pandas as pd


def calculate_trends(df):
    """
    Calculate Mann-Kendall trends and Sen slopes
    for all result columns.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame indexed by year.

    Returns
    -------
    pandas.DataFrame
        Indexed by method with columns:

        trend
        p_value
        slope
        intercept
        pct_change
    """

    results = []

    cols = [
        col
        for col in df.columns
        if not col.startswith(
            (
                "lower",
                "upper",
            )
        )
    ]

    for col in cols:

        mk = nivapy.stats.mk_test(
            df,
            col,
            alpha=0.05,
        )

        sen_df, _ = nivapy.stats.sens_slope(
            df,
            col,
            index_col=df.index,
            alpha=0.05,
        )

        trend = mk.loc[
            "trend",
            "value",
        ]

        pval = mk.loc[
            "p",
            "value",
        ]

        slope = sen_df.loc[
            "sslp",
            "value",
        ]

        intercept = sen_df.loc[
            "icpt",
            "value",
        ]

        start_val = slope * df.index.min() + intercept

        end_val = slope * df.index.max() + intercept

        pct_change = 100.0 * (end_val - start_val) / start_val

        results.append(
            {
                "method": col,
                "trend": trend,
                "p_value": pval,
                "slope_tonnes-per-year": slope,
                "intercept": intercept,
                "pct_change": pct_change,
            }
        )

    return pd.DataFrame(results).set_index("method").sort_index()