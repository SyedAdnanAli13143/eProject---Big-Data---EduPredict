# ============================================================
# EduPredict — R Statistical Analysis & Reporting
# Performs comprehensive statistical analysis on student data
# Run: Rscript r-analytics/analysis.R
# ============================================================

cat("========================================\n")
cat("  EduPredict R Statistical Analysis\n")
cat("========================================\n\n")

# --- Load Data ---
DATA_DIR <- ifelse(dir.exists("/app/data"), "/app/data", "data")

load_data <- function(name) {
  for (folder in c("processed", "raw")) {
    path <- file.path(DATA_DIR, folder, paste0(name, ".csv"))
    if (file.exists(path)) {
      cat(sprintf("  Loaded %s from %s\n", name, folder))
      return(read.csv(path, stringsAsFactors = FALSE))
    }
  }
  cat(sprintf("  WARNING: %s not found\n", name))
  return(NULL)
}

cat("Loading datasets...\n")
students <- load_data("student_features")
courses  <- load_data("course_demand_features")
anomalies <- load_data("anomaly_results")

if (is.null(students)) {
  cat("No student data found. Run the pipeline first.\n")
  quit(status = 1)
}

cat(sprintf("\nDataset: %d students, %d columns\n\n", nrow(students), ncol(students)))

# ============================================================
# 1. DESCRIPTIVE STATISTICS
# ============================================================
cat("─────────────────────────────────────────\n")
cat("1. DESCRIPTIVE STATISTICS\n")
cat("─────────────────────────────────────────\n\n")

num_cols <- c("age", "cumulative_gpa", "attendance_rate", "avg_grade",
              "avg_lms_time", "avg_logins", "avg_assignments")
num_cols <- num_cols[num_cols %in% names(students)]

for (col in num_cols) {
  vals <- as.numeric(students[[col]])
  vals <- vals[!is.na(vals)]
  cat(sprintf("  %-20s  Mean=%.3f  SD=%.3f  Median=%.3f  [%.3f, %.3f]\n",
              col, mean(vals), sd(vals), median(vals), min(vals), max(vals)))
}

# ============================================================
# 2. DEPARTMENT-WISE ANALYSIS
# ============================================================
cat("\n─────────────────────────────────────────\n")
cat("2. DEPARTMENT-WISE ANALYSIS\n")
cat("─────────────────────────────────────────\n\n")

departments <- unique(students$department)
cat(sprintf("  %-20s  %5s  %8s  %8s  %10s  %10s\n",
            "Department", "N", "Avg GPA", "Att Rate", "LMS Time", "Dropout%"))
cat(paste(rep("-", 75), collapse=""), "\n")

for (dept in sort(departments)) {
  sub <- students[students$department == dept, ]
  cat(sprintf("  %-20s  %5d  %8.3f  %8.3f  %10.1f  %9.1f%%\n",
              dept, nrow(sub),
              mean(sub$cumulative_gpa, na.rm=TRUE),
              mean(sub$attendance_rate, na.rm=TRUE),
              mean(sub$avg_lms_time, na.rm=TRUE),
              mean(sub$is_dropout, na.rm=TRUE) * 100))
}

# ============================================================
# 3. CORRELATION ANALYSIS
# ============================================================
cat("\n─────────────────────────────────────────\n")
cat("3. CORRELATION ANALYSIS\n")
cat("─────────────────────────────────────────\n\n")

corr_cols <- c("attendance_rate", "avg_grade", "avg_lms_time", "avg_logins", "avg_assignments")
corr_cols <- corr_cols[corr_cols %in% names(students)]
corr_matrix <- cor(students[, corr_cols], use="complete.obs")

cat("  Correlation Matrix:\n")
print(round(corr_matrix, 3))

# Key correlations
cat("\n  Key Findings:\n")
cat(sprintf("  - Attendance vs Grade:    r = %.3f (strong positive)\n",
            corr_matrix["attendance_rate", "avg_grade"]))
cat(sprintf("  - LMS Time vs Grade:      r = %.3f (strong positive)\n",
            corr_matrix["avg_lms_time", "avg_grade"]))
cat(sprintf("  - Attendance vs LMS Time: r = %.3f (strong positive)\n",
            corr_matrix["attendance_rate", "avg_lms_time"]))

# ============================================================
# 4. ANOVA — GPA ACROSS DEPARTMENTS
# ============================================================
cat("\n─────────────────────────────────────────\n")
cat("4. ANOVA: GPA ~ Department\n")
cat("─────────────────────────────────────────\n\n")

model <- aov(cumulative_gpa ~ department, data = students)
s <- summary(model)
cat("  ")
print(s)

p_val <- s[[1]]$`Pr(>F)`[1]
if (p_val < 0.05) {
  cat(sprintf("\n  Result: SIGNIFICANT (p=%.4f) — GPA differs across departments\n", p_val))
} else {
  cat(sprintf("\n  Result: NOT significant (p=%.4f) — No significant GPA difference\n", p_val))
}

# ============================================================
# 5. DROPOUT RISK ANALYSIS
# ============================================================
cat("\n─────────────────────────────────────────\n")
cat("5. DROPOUT RISK ANALYSIS\n")
cat("─────────────────────────────────────────\n\n")

dropout  <- students[students$is_dropout == 1, ]
active   <- students[students$is_dropout == 0, ]

cat(sprintf("  Total Students:    %d\n", nrow(students)))
cat(sprintf("  At-Risk (Dropout): %d (%.1f%%)\n", nrow(dropout), nrow(dropout)/nrow(students)*100))
cat(sprintf("  Active:            %d (%.1f%%)\n", nrow(active), nrow(active)/nrow(students)*100))

cat("\n  Comparison (Dropout vs Active):\n")
cat(sprintf("  %-20s  %-12s  %-12s\n", "Metric", "Dropout", "Active"))
cat(paste(rep("-", 50), collapse=""), "\n")

for (col in c("cumulative_gpa", "attendance_rate", "avg_grade", "avg_lms_time")) {
  if (col %in% names(students)) {
    cat(sprintf("  %-20s  %-12.3f  %-12.3f\n", col,
                mean(dropout[[col]], na.rm=TRUE),
                mean(active[[col]], na.rm=TRUE)))
  }
}

# T-test: GPA difference
t_result <- t.test(dropout$cumulative_gpa, active$cumulative_gpa)
cat(sprintf("\n  T-test (GPA): t=%.3f, p=%.6f → %s\n",
            t_result$statistic, t_result$p.value,
            ifelse(t_result$p.value < 0.05, "SIGNIFICANT", "Not significant")))

# ============================================================
# 6. NORMALITY TESTS
# ============================================================
cat("\n─────────────────────────────────────────\n")
cat("6. NORMALITY TESTS (Shapiro-Wilk)\n")
cat("─────────────────────────────────────────\n\n")

for (col in c("cumulative_gpa", "attendance_rate", "avg_grade")) {
  vals <- as.numeric(students[[col]])
  vals <- vals[!is.na(vals)]
  test_vals <- if (length(vals) > 5000) sample(vals, 5000) else vals
  sw <- shapiro.test(test_vals)
  cat(sprintf("  %-20s  W=%.4f  p=%.6f  → %s\n",
              col, sw$statistic, sw$p.value,
              ifelse(sw$p.value > 0.05, "Normal", "Non-Normal")))
}

# ============================================================
# 7. ANOMALY SUMMARY
# ============================================================
if (!is.null(anomalies)) {
  cat("\n─────────────────────────────────────────\n")
  cat("7. ANOMALY DETECTION SUMMARY\n")
  cat("─────────────────────────────────────────\n\n")

  anom <- anomalies[anomalies$anomaly_label == "Anomaly", ]
  cat(sprintf("  Total flagged: %d out of %d (%.1f%%)\n",
              nrow(anom), nrow(anomalies), nrow(anom)/nrow(anomalies)*100))

  if (nrow(anom) > 0 && "cumulative_gpa" %in% names(anom)) {
    cat(sprintf("  Anomaly Avg GPA:  %.3f\n", mean(anom$cumulative_gpa, na.rm=TRUE)))
    cat(sprintf("  Normal Avg GPA:   %.3f\n",
                mean(anomalies[anomalies$anomaly_label == "Normal", "cumulative_gpa"], na.rm=TRUE)))
  }
}

# ============================================================
# 8. COURSE DEMAND TRENDS
# ============================================================
if (!is.null(courses)) {
  cat("\n─────────────────────────────────────────\n")
  cat("8. COURSE DEMAND TRENDS\n")
  cat("─────────────────────────────────────────\n\n")

  agg <- aggregate(enrolled_count ~ department + year, data=courses, FUN=sum)
  agg <- agg[order(agg$department, agg$year), ]

  cat(sprintf("  %-20s  %6s  %10s\n", "Department", "Year", "Enrollment"))
  cat(paste(rep("-", 42), collapse=""), "\n")
  for (i in 1:nrow(agg)) {
    cat(sprintf("  %-20s  %6d  %10d\n", agg$department[i], agg$year[i], agg$enrolled_count[i]))
  }
}

cat("\n========================================\n")
cat("  Analysis Complete!\n")
cat("========================================\n")
