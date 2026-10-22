#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(mgcv)
  library(dplyr)
  library(MASS)
})

# Read command line arguments

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop(
    paste(
      "Usage:",
      "Rscript run_gam.R",
      "sample.csv",
      "daily.csv",
      "results.csv"
    )
  )
}
sample_file <- args[1]
daily_file  <- args[2]
result_file <- args[3]
cat("Reading input files...\n")

# Read data
sample_df <- read.csv(
  sample_file,
  stringsAsFactors = FALSE
)
daily_df <- read.csv(
  daily_file,
  stringsAsFactors = FALSE
)
sample_df$date <- as.Date(sample_df$date)
daily_df$date  <- as.Date(daily_df$date)

# Prepare daily data
daily_df <- daily_df %>%
  dplyr::filter(
    !is.na(Q),
    Q > 0
  ) %>%
  dplyr::mutate(
    year = as.integer(format(date, "%Y")),
    doy = as.integer(format(date, "%j")),
    dec_year = year + (doy - 0.5) / 365.25
  )

# Merge chemistry and flow
sample_df <- sample_df %>%
  dplyr::left_join(
    daily_df %>%
      dplyr::select(date, Q),
    by = "date"
  ) %>%
  dplyr::mutate(
    year = as.integer(format(date, "%Y")),
    doy = as.integer(format(date, "%j")),
    dec_year = year + (doy - 0.5) / 365.25
  ) %>%
  dplyr::filter(
    !is.na(Conc),
    !is.na(Q),
    Conc > 0,
    Q > 0
  )
cat(
  "Samples used:",
  nrow(sample_df),
  "\n"
)
if (nrow(sample_df) < 20) {
  stop(
    paste(
      "Too few samples for GAM:",
      nrow(sample_df)
    )
  )
}

# Fit GAM
cat("Fitting GAM...\n")
gam_fit <- mgcv::gam(
  log(Conc) ~
    s(log(Q), k = 10) +
    s(dec_year, k = 20) +
    s(doy, bs = "cc", k = 20) +
    ti(
      log(Q),
      doy,
      bs = c("tp", "cc"),
      k = c(10, 10)
    ),
  data = sample_df,
  method = "REML"
)

# Prediction uncertainty
resid_var <- var(
  residuals(gam_fit)
)
daily_df$pred_log_c <- predict(
  gam_fit,
  newdata = daily_df
)
daily_df$pred_c <- exp(
  daily_df$pred_log_c +
    0.5 * resid_var
)

# Daily loads
# mg/L × m3/s × 86.4 = kg/day
daily_df$load_kg_day <-
  daily_df$pred_c *
  daily_df$Q *
  86.4

# Annual loads
annual_loads <- daily_df %>%
  dplyr::group_by(year) %>%
  dplyr::summarise(
    load_kg = sum(
      load_kg_day,
      na.rm = TRUE
    ),
    .groups = "drop"
  ) %>%
  dplyr::mutate(
    load_tonnes = load_kg / 1000
  )

# Bayesian posterior simulation
n_sim <- 1000
cat(
  "Running",
  n_sim,
  "posterior simulations...\n"
)
Xp <- predict(
  gam_fit,
  newdata = daily_df,
  type = "lpmatrix"
)
beta_hat <- coef(gam_fit)
Vp <- vcov(
  gam_fit,
  unconditional = TRUE
)
beta_sim <- MASS::mvrnorm(
  n = n_sim,
  mu = beta_hat,
  Sigma = Vp
)
annual_sim <- matrix(
  NA_real_,
  nrow = nrow(annual_loads),
  ncol = n_sim
)
for (i in seq_len(n_sim)) {
  pred_log_sim <- as.vector(
    Xp %*% beta_sim[i, ]
  )
  pred_c_sim <- exp(
    pred_log_sim +
      0.5 * resid_var
  )
  annual_i <- data.frame(
    year = daily_df$year,
    load_kg =
      pred_c_sim *
      daily_df$Q *
      86.4
  ) %>%
    dplyr::group_by(year) %>%
    dplyr::summarise(
      load_kg = sum(
        load_kg,
        na.rm = TRUE
      ),
      .groups = "drop"
    )
  annual_sim[, i] <- annual_i$load_kg
}

# Credible intervals
annual_loads$lower_kg <- apply(
  annual_sim,
  1,
  quantile,
  probs = 0.025,
  na.rm = TRUE
)
annual_loads$upper_kg <- apply(
  annual_sim,
  1,
  quantile,
  probs = 0.975,
  na.rm = TRUE
)
annual_loads <- annual_loads %>%
  dplyr::mutate(
    lower_tonnes = lower_kg / 1000,
    upper_tonnes = upper_kg / 1000,
    rel_uncertainty_pct =
      100 *
      (upper_tonnes - lower_tonnes) /
      (2 * load_tonnes)
  )

# Save
write.csv(
  annual_loads,
  result_file,
  row.names = FALSE
)
cat(
  "Results written to:",
  result_file,
  "\n"
)
cat(
  "GAM analysis complete.\n"
)