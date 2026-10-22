#!/usr/bin/env Rscript

suppressPackageStartupMessages({
  library(EGRET)
})

# Read command line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 3) {
  stop(
    paste(
      "Usage:",
      "Rscript run_egret.R",
      "sample.csv",
      "daily.csv",
      "results.csv",
    )
  )
}
sample_file <- args[1]
daily_file  <- args[2]
result_file <- args[3]

cat("Reading input files...\n")

# Read EGRET inputs
Sample <- readUserSample(
  filePath = dirname(sample_file),
  fileName = basename(sample_file),
  separator = ","
)
Daily <- readUserDaily(
  filePath = dirname(daily_file),
  fileName = basename(daily_file),
  separator = ",",
  qUnit = 2
)

# Metadata
INFO <- data.frame(
  shortName      = "Station",
  paramShortName = "Conc",
  constitAbbrev  = "Conc",
  param.units    = "mg/L",
  drainSqKm      = NA,
  paStart        = 1,
  paLong         = 12
)

# Create EGRET object
cat("Building eList...\n")
eList <- as.egret(
  INFO = INFO,
  Daily = Daily,
  Sample = Sample
)

# Fit WRTDS
cat("Running WRTDS model...\n")
eList <- modelEstimation(
  eList
)

# Annual results
annual_results <- tableResults(
  eList
)

# Save
write.csv(
  annual_results,
  result_file,
  row.names = FALSE
)
cat(
  "Results written to:",
  result_file,
  "\n"
)
cat(
  "WRTDS complete.\n"
)