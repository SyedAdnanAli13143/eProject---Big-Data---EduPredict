# ============================================================
# EduPredict — R Data Visualizations
# Generates PNG charts for reports and presentations
# Run: Rscript r-analytics/visualizations.R
# Output: r-analytics/plots/ directory
# ============================================================

cat("========================================\n")
cat("  EduPredict R Visualizations\n")
cat("========================================\n\n")

# --- Setup ---
PLOT_DIR <- ifelse(dir.exists("/app"), "/app/plots", "r-analytics/plots")
dir.create(PLOT_DIR, showWarnings = FALSE, recursive = TRUE)

DATA_DIR <- ifelse(dir.exists("/app/data"), "/app/data", "data")

load_data <- function(name) {
  for (folder in c("processed", "raw")) {
    path <- file.path(DATA_DIR, folder, paste0(name, ".csv"))
    if (file.exists(path)) return(read.csv(path, stringsAsFactors = FALSE))
  }
  return(NULL)
}

students <- load_data("student_features")
courses  <- load_data("course_demand_features")

if (is.null(students)) {
  cat("No data found. Run pipeline first.\n")
  quit(status = 1)
}

# --- Color Palette ---
COLORS <- c("#3B82F6", "#EF4444", "#10B981", "#F59E0B", "#8B5CF6",
            "#06B6D4", "#F97316", "#EC4899")

# ============================================================
# 1. GPA DISTRIBUTION HISTOGRAM
# ============================================================
cat("  1. GPA Distribution...\n")
png(file.path(PLOT_DIR, "gpa_distribution.png"), width=800, height=500, res=120)
par(mar=c(5, 4, 3, 2))
hist(students$cumulative_gpa, breaks=20, col=COLORS[1], border="white",
     main="Student GPA Distribution", xlab="Cumulative GPA", ylab="Frequency",
     font.main=2, col.main="#1E293B")
abline(v=mean(students$cumulative_gpa), col=COLORS[2], lwd=2, lty=2)
legend("topright", legend=sprintf("Mean = %.2f", mean(students$cumulative_gpa)),
       col=COLORS[2], lty=2, lwd=2, bty="n")
dev.off()

# ============================================================
# 2. DEPARTMENT COMPARISON BARPLOT
# ============================================================
cat("  2. Department Comparison...\n")
png(file.path(PLOT_DIR, "department_comparison.png"), width=900, height=500, res=120)
par(mar=c(7, 4, 3, 2))
dept_gpa <- tapply(students$cumulative_gpa, students$department, mean)
dept_gpa <- sort(dept_gpa, decreasing=TRUE)
bp <- barplot(dept_gpa, col=COLORS[1:length(dept_gpa)], border="white",
              main="Average GPA by Department", ylab="Average GPA",
              las=2, ylim=c(0, max(dept_gpa)*1.15), font.main=2, col.main="#1E293B")
text(bp, dept_gpa, labels=sprintf("%.2f", dept_gpa), pos=3, cex=0.9, font=2)
dev.off()

# ============================================================
# 3. DROPOUT RISK PIE CHART
# ============================================================
cat("  3. Dropout Risk Distribution...\n")
png(file.path(PLOT_DIR, "dropout_pie.png"), width=700, height=500, res=120)
dropout_counts <- table(ifelse(students$is_dropout == 1, "At Risk", "Active"))
pct <- round(100 * dropout_counts / sum(dropout_counts), 1)
labels <- paste0(names(dropout_counts), "\n", dropout_counts, " (", pct, "%)")
pie(dropout_counts, labels=labels, col=c(COLORS[3], COLORS[2]),
    main="Student Dropout Risk", font.main=2, col.main="#1E293B", border="white")
dev.off()

# ============================================================
# 4. CORRELATION HEATMAP
# ============================================================
cat("  4. Correlation Heatmap...\n")
png(file.path(PLOT_DIR, "correlation_heatmap.png"), width=800, height=700, res=120)

corr_cols <- c("attendance_rate", "avg_grade", "avg_lms_time", "avg_logins", "avg_assignments")
corr_cols <- corr_cols[corr_cols %in% names(students)]
corr_mat <- cor(students[, corr_cols], use="complete.obs")

# Short labels
short_names <- c("Attendance", "Grade", "LMS Time", "Logins", "Assignments")
short_names <- short_names[1:length(corr_cols)]

par(mar=c(8, 8, 3, 2))
n <- nrow(corr_mat)
image(1:n, 1:n, t(corr_mat[n:1, ]), col=colorRampPalette(c("#EF4444","#FBBF24","#10B981"))(50),
      axes=FALSE, xlab="", ylab="", main="Feature Correlation Matrix",
      font.main=2, col.main="#1E293B")
axis(1, at=1:n, labels=short_names, las=2, cex.axis=0.85)
axis(2, at=1:n, labels=rev(short_names), las=1, cex.axis=0.85)
for (i in 1:n) for (j in 1:n) {
  text(i, n-j+1, sprintf("%.2f", corr_mat[j,i]), cex=0.75, font=2)
}
dev.off()

# ============================================================
# 5. ATTENDANCE VS GRADE SCATTER
# ============================================================
cat("  5. Attendance vs Grade Scatter...\n")
png(file.path(PLOT_DIR, "attendance_vs_grade.png"), width=800, height=500, res=120)
par(mar=c(5, 4, 3, 2))
colors <- ifelse(students$is_dropout == 1, COLORS[2], COLORS[1])
plot(students$attendance_rate, students$avg_grade,
     col=adjustcolor(colors, alpha.f=0.5), pch=19, cex=0.8,
     main="Attendance Rate vs Average Grade",
     xlab="Attendance Rate", ylab="Average Grade",
     font.main=2, col.main="#1E293B")
abline(lm(avg_grade ~ attendance_rate, data=students), col=COLORS[4], lwd=2)
legend("bottomright", c("Active", "Dropout Risk"),
       col=c(COLORS[1], COLORS[2]), pch=19, bty="n", cex=0.9)
dev.off()

# ============================================================
# 6. DEPARTMENT DROPOUT RATE BAR
# ============================================================
cat("  6. Department Dropout Rates...\n")
png(file.path(PLOT_DIR, "department_dropout.png"), width=900, height=500, res=120)
par(mar=c(7, 5, 3, 2))
dept_dropout <- tapply(students$is_dropout, students$department, mean) * 100
dept_dropout <- sort(dept_dropout, decreasing=TRUE)
bp <- barplot(dept_dropout, col=COLORS[2], border="white",
              main="Dropout Rate by Department (%)", ylab="Dropout Rate (%)",
              las=2, ylim=c(0, max(dept_dropout)*1.3), font.main=2, col.main="#1E293B")
text(bp, dept_dropout, labels=sprintf("%.1f%%", dept_dropout), pos=3, cex=0.9, font=2)
dev.off()

# ============================================================
# 7. COURSE DEMAND TRENDS
# ============================================================
if (!is.null(courses)) {
  cat("  7. Course Demand Trends...\n")
  png(file.path(PLOT_DIR, "course_demand_trends.png"), width=900, height=500, res=120)
  par(mar=c(5, 4, 3, 2))

  depts <- unique(courses$department)
  agg <- aggregate(enrolled_count ~ department + period_num, data=courses, FUN=sum)

  plot(NULL, xlim=range(agg$period_num), ylim=c(0, max(agg$enrolled_count)*1.1),
       main="Course Enrollment Trends by Department",
       xlab="Academic Period", ylab="Total Enrollment",
       font.main=2, col.main="#1E293B")

  for (i in seq_along(depts)) {
    sub <- agg[agg$department == depts[i], ]
    sub <- sub[order(sub$period_num), ]
    lines(sub$period_num, sub$enrolled_count, col=COLORS[i], lwd=2, type="b", pch=19)
  }
  legend("topleft", legend=depts, col=COLORS[1:length(depts)], lwd=2, pch=19,
         bty="n", cex=0.8)
  dev.off()
}

cat(sprintf("\nAll plots saved to: %s\n", PLOT_DIR))
cat(sprintf("Files: %s\n", paste(list.files(PLOT_DIR, pattern="\\.png$"), collapse=", ")))
cat("\nVisualization complete!\n")
