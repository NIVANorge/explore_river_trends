import streamlit as st

st.set_page_config(
    page_title="Oslofjord river loads",
    layout="wide",
)

st.title("Oslofjord river loads")

st.markdown(
    """
## Overview

This application allows you to explore long-term trends in nutrient transport from major rivers draining to the Oslofjord. Results are based on more than three decades of monitoring data and provide insights into how riverine loads have changed through time.

**To begin, select `Explore data` from the sidebar.**

## Data sources

The application combines:

- **Water chemistry data** collected through the [Elveovervåkingsprogrammet](https://www.miljodirektoratet.no/ansvarsomrader/overvaking-arealplanlegging/miljoovervaking/overvakingsprogrammer/forurensning-og-klimagasser/elveovervakningsprogrammet/)
- **River discharge data** provided by [NVE](https://www.nve.no/)

All analyses are based on monitoring data collected between **1990 and 2024**. For nitrogen, sampling strategies, laboratory methods, and analytical procedures have remained broadly consistent throughout this period, making these datasets particularly well suited for assessing long-term environmental change.

For phosphorus, changes in laboratories, analytical methods, and detection limits prior to 2004 introduced clear step changes in the data. To ensure comparability over time, phosphorus loads are therefore presented only for the period **2004 to 2024**.

There are also known issues with the TOC datasets for **Skienselva** and **Numedalslågen** prior to 1999. Consequently, TOC analyses for these rivers are restricted to the period **1999 to 2024**.

Results are presented for four major rivers:

- **Drammenselva** at Mjøndalsbrua (`BUSEDRA`)
- **Skienselva** at Klosterfossen (`TELESKI`)
- **Numedalslågen** at Bommestad (`VESENUM`)
- **Glomma** at Sarpsfoss (`ØSTEGLO`)

The monitoring stations represent most, but not all, inputs to the Oslofjord. Discharges entering the rivers downstream of these stations, such as from wastewater treatment or industrial plants, are not included in the estimates.

The following parameters are available:

- **Total Nitrogen** (`TOTN`) from 1990 to 2024.
- **Nitrate Nitrogen** (`NO3-N`) from 1990 to 2024.
- **Total Phosphorus** (`TOTP`) from 2004 to 2024.
- **Phosphate Phosphorus** (`PO4-P`) from 2004 to 2024. Note that, within Elveovervåkingsprogrammet, phosphate is analysed on **unfiltered** samples. This fraction is commonly referred to as **Total Reactive Phosphorus (TRP)**.
- **Total Organic Carbon** (`TOC`) from 1990 to 2024 for Glomma and Drammenselva; 1999 to 2024 for Skienselva and Numedalslågen.
- **Suspended Particulate Material** (`SPM`) from 1990 to 2024.

## Estimating annual loads

There are many different ways of estimating river loads (or fluxes). By comparing several approaches, this application provides insight into the uncertainty associated with methodological choices and helps to identify robust patterns in the data.

Results are presented using four complementary methods.

### OSPAR Method

The OSPAR method is widely used for routine environmental reporting and regulatory monitoring. It is computationally efficient, performs well with irregular sampling intervals, and is generally less biased than other simple load-estimation approaches, such as linear interpolation. For these reasons, it is extensively used within Norwegian monitoring programmes, including Elveovervåkingsprogrammet.

### EGRET

EGRET (Exploration and Graphics for RivEr Trends) is an advanced statistical modelling framework designed to analyse long-term water-quality and flux trends.

Unlike the OSPAR method, which estimates loads directly from individual measurements, EGRET models the relationship between **concentration**, **river flow**, **seasonality**, and **long-term temporal change**. By using information from the entire monitoring record, EGRET can make more effective use of sparse or irregularly sampled datasets and often provides a more robust interpretation of long-term trends.

This application presents two EGRET-derived metrics:

1. **Absolute fluxes** represent the estimated annual mass transported by the river to the Oslofjord. These estimates reflect changes in both water quality and river flow and are directly comparable to results from the OSPAR and GAM approaches.

2. **Flow-normalised fluxes** remove the influence of year-to-year variation in river discharge. They represent the flux that would be expected under average hydrological conditions and are therefore particularly useful for assessing changes caused by management actions, land-use change, or shifts in pollutant sources.

### Generalised Additive Models

Generalised Additive Models (GAMs) are flexible statistical models that can describe complex, non-linear environmental trends. In this application, GAMs are used to estimate annual fluxes from the observed concentration and flow data. The models also provide **95 % confidence intervals for the estimated annual fluxes**. These intervals indicate the range of annual fluxes that are consistent with the fitted GAM and the available data. Note that they reflect uncertainty in the modelled mean annual fluxes and do not account for all potential sources of uncertainty.

Because GAMs impose fewer assumptions about the shape of long-term trends, they are particularly well suited to environmental datasets where responses change gradually and non-linearly over time.

## Estimating trends

Long-term trends in annual fluxes are evaluated using the **Mann-Kendall test**, a widely used non-parametric method for detecting monotonic trends in environmental time series.

Trend significance is indicated on the plots as follows:

- **Significant trends** ($p \le 0.05$) are shown as a **thick, solid red line**.
- **Marginally significant trends** ($0.05 < p \le 0.10$) are shown as a **thick, dashed red line**.
- **Non-significant trends** ($p > 0.10$) are shown as a **thin, dashed black line**.

For each time series, the **Sen's slope** is also calculated and reported. This provides a robust estimate of the rate of change in annual flux (tonnes.yr⁻¹). In addition, the **mean percentage change** between the beginning and end of the trend line is presented to help quantify the magnitude of long-term change.

## Interpreting the plots

The following approach may help when interpreting the results:

1. **Start by examining the annual flux estimates from the `OSPAR`, `EGRET`, and `GAM methods`** (i.e. ignore the `EGRET Flow-Normalised` plot initially). These three estimates represent annual fluxes under observed hydrological conditions and are directly comparable. Differences between them provide an indication of methodological uncertainty. In most cases, the three methods produce broadly similar results.

2. **Compare the trend lines and slope estimates for the `OSPAR`, `EGRET`, and `GAM` results.** Consistent trends across all three methods increase confidence that observed changes are real and not an artefact of the estimation approach.

3. **Examine the `EGRET Flow-Normalised` results.** Because the influence of year-to-year variation in river flow has been removed, this time series is generally smoother than the others. Trends in the flow-normalised series highlight changes that are independent of hydrological variability and are therefore more likely to reflect factors such as land-use change, catchment management measures, wastewater treatment improvements, or changes in pollutant sources.

4. **Interpret all plots together.** In some cases, the flow-normalised series shows a significant decreasing trend, while the annual flux estimates from `OSPAR`, `EGRET`, and `GAM` show increasing trends. This pattern suggests that the catchment would be exporting less nutrients under equivalent hydrological conditions, but increasing river discharge and/or hydrological variability mean that annual nutrient loads to the Oslofjord are nevertheless increasing.

5. **Pay attention to uncertainty as well as trend direction.** Small differences between methods are often less important than the overall pattern. When multiple methods indicate similar long-term trajectories, confidence in the interpretation is generally higher than when conclusions depend on a single modelling approach.
"""
)