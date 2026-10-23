import matplotlib.pyplot as plt
import numpy as np

plt.style.use("ggplot")


def add_trendline(
    ax,
    df,
    col,
    trend_df,
):
    """
    Add Sen-slope trendline.

    p <= 0.05:
        red solid, lw=2

    0.05 < p <= 0.10:
        red dashed, lw=2

    p > 0.10:
        black dashed, lw=1
    """

    if col not in trend_df.index:
        return

    trend = trend_df.loc[col]

    pval = trend["p_value"]

    slope = trend["slope_tonnes-per-year"]
    intercept = trend["intercept"]

    x = np.asarray(df.index)

    y = slope * x + intercept

    if pval <= 0.05:

        color = "red"
        linestyle = "-"
        linewidth = 2

    elif pval <= 0.10:

        color = "red"
        linestyle = "--"
        linewidth = 2

    else:

        color = "black"
        linestyle = "--"
        linewidth = 1

    ax.plot(
        x,
        y,
        color=color,
        linestyle=linestyle,
        linewidth=linewidth,
        # label=f"Trend (p={pval:.3f})",
        label=f"Trend",
        zorder=10,
    )


def add_trend_summary(
    ax,
    col,
    trend_df,
):
    """
    Add textbox showing trend statistics.
    """

    if col not in trend_df.index:
        return

    trend = trend_df.loc[col]

    pval = trend["p_value"]

    slope = trend["slope_tonnes-per-year"]

    pct_change = trend["pct_change"]

    if pval <= 0.05:
        edgecolor = "red"

    elif pval <= 0.10:
        edgecolor = "red"

    else:
        edgecolor = "black"

    text = (
        f"Slope: {slope:+.1f} t/yr\n" f"Change: {pct_change:+.1f}%\n" f"p = {pval:.3f}"
    )

    ax.text(
        0.03,
        0.97,
        text,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox=dict(
            facecolor="white",
            edgecolor=edgecolor,
            alpha=0.9,
            boxstyle="round,pad=0.3",
        ),
    )


def plot_fluxes(
    df,
    parameter,
    trend_df=None,
):
    """
    Plot annual flux estimates from:

    - OSPAR
    - EGRET
    - EGRET Flow-Normalised
    - GAM

    Parameters
    ----------
    df : pandas.DataFrame

    parameter : str

    trend_df : pandas.DataFrame, optional
        Output from calculate_trends().
    """

    par = parameter.split("_")[0]

    fig, axes = plt.subplots(
        nrows=2,
        ncols=2,
        figsize=(10, 6),
        sharex=True,
        sharey=True,
    )

    axes = axes.flatten()

    plot_info = [
        (
            f"OSPAR_{par}_tonn",
            "k",
            "OSPAR",
        ),
        (
            f"EGRET_{par}_tonn",
            "b",
            "EGRET",
        ),
        (
            f"EGRET_FN_{par}_tonn",
            "g",
            "EGRET Flow-Normalised",
        ),
        (
            f"GAM_{par}_tonn",
            "r",
            "GAM",
        ),
    ]

    for ax, (col, color, title) in zip(
        axes,
        plot_info,
    ):

        if col not in df.columns:
            ax.set_visible(False)
            continue

        df[col].plot(
            ax=ax,
            color=color,
            marker="o",
            linewidth=1.5,
        )

        if trend_df is not None:

            add_trendline(
                ax,
                df,
                col,
                trend_df,
            )

            add_trend_summary(
                ax,
                col,
                trend_df,
            )

        if title == "GAM":

            lower_col = f"lower_GAM_{par}_tonn"

            upper_col = f"upper_GAM_{par}_tonn"

            if lower_col in df.columns and upper_col in df.columns:

                ax.fill_between(
                    df.index,
                    df[lower_col],
                    df[upper_col],
                    color="red",
                    alpha=0.2,
                    label="95% CI",
                )

        ax.set_title(title)

        ax.set_ylabel(f"{par} load (tonnes/year)")

        ax.set_xlabel("")

        # ax.legend(
        #     loc="lower left",
        #     fontsize=8,
        # )

        if ax.get_visible():
            ax.set_xticks(
                np.arange(
                    (df.index.min() // 5) * 5,
                    df.index.max() + 1,
                    5,
                )
            )

    plt.tight_layout()

    return fig