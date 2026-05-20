# EduPredict — R Analytics API (Plumber)
# Provides statistical analysis endpoints using R

library(plumber)
library(jsonlite)

DATA_DIR <- "/app/data"

# Helper: read CSV safely
read_safe <- function(name) {
  for (folder in c("processed", "raw")) {
    path <- file.path(DATA_DIR, folder, paste0(name, ".csv"))
    if (file.exists(path)) {
      return(read.csv(path, stringsAsFactors = FALSE))
    }
  }
  return(NULL)
}

#* Health check
#* @get /health
function() {
  list(status = "ok", service = "R Analytics")
}

#* Statistical summary of student features
#* @get /summary
#* @serializer json
function() {
  df <- read_safe("student_features")
  if (is.null(df)) return(list(error = "Data not found"))

  cols <- c("age", "cumulative_gpa", "attendance_rate", "avg_grade",
            "avg_lms_time", "avg_logins", "avg_assignments")
  cols <- cols[cols %in% names(df)]

  result <- list()
  for (col in cols) {
    vals <- as.numeric(df[[col]])
    vals <- vals[!is.na(vals)]
    result[[col]] <- list(
      mean   = round(mean(vals), 3),
      median = round(median(vals), 3),
      std    = round(sd(vals), 3),
      min    = round(min(vals), 3),
      max    = round(max(vals), 3),
      q1     = round(quantile(vals, 0.25), 3),
      q3     = round(quantile(vals, 0.75), 3)
    )
  }
  list(source = "R", summary = result)
}

#* Correlation matrix
#* @get /correlation
#* @serializer json
function() {
  df <- read_safe("student_features")
  if (is.null(df)) return(list(error = "Data not found"))

  cols <- c("attendance_rate", "avg_grade", "avg_lms_time",
            "avg_logins", "avg_assignments", "avg_forum_posts")
  cols <- cols[cols %in% names(df)]
  num_df <- df[, cols, drop = FALSE]
  num_df <- num_df[complete.cases(num_df), ]

  corr_matrix <- round(cor(num_df), 3)
  list(
    source  = "R",
    columns = cols,
    matrix  = as.list(as.data.frame(corr_matrix))
  )
}

#* Per-department statistics
#* @get /department-stats
#* @serializer json
function() {
  df <- read_safe("student_features")
  if (is.null(df)) return(list(error = "Data not found"))

  departments <- unique(df$department)
  stats <- lapply(departments, function(dept) {
    sub <- df[df$department == dept, ]
    list(
      department     = dept,
      count          = nrow(sub),
      avg_gpa        = round(mean(sub$cumulative_gpa, na.rm = TRUE), 3),
      avg_attendance = round(mean(sub$attendance_rate, na.rm = TRUE), 3),
      avg_lms_time   = round(mean(sub$avg_lms_time, na.rm = TRUE), 1),
      dropout_rate   = round(mean(sub$is_dropout, na.rm = TRUE), 3)
    )
  })
  list(source = "R", stats = stats)
}

#* ANOVA test: GPA across departments
#* @get /anova
#* @serializer json
function() {
  df <- read_safe("student_features")
  if (is.null(df)) return(list(error = "Data not found"))

  model <- aov(cumulative_gpa ~ department, data = df)
  s <- summary(model)[[1]]
  list(
    source   = "R",
    test     = "One-way ANOVA (GPA ~ Department)",
    f_value  = round(s$`F value`[1], 3),
    p_value  = round(s$`Pr(>F)`[1], 5),
    significant = s$`Pr(>F)`[1] < 0.05
  )
}

#* Distribution analysis for a variable
#* @get /distribution/<variable>
#* @serializer json
function(variable) {
  df <- read_safe("student_features")
  if (is.null(df)) return(list(error = "Data not found"))
  if (!(variable %in% names(df))) return(list(error = paste("Column", variable, "not found")))

  vals <- as.numeric(df[[variable]])
  vals <- vals[!is.na(vals)]

  # Shapiro-Wilk test (sample if > 5000)
  test_vals <- if (length(vals) > 5000) sample(vals, 5000) else vals
  sw <- shapiro.test(test_vals)

  # Histogram bins
  h <- hist(vals, plot = FALSE, breaks = 15)

  list(
    source   = "R",
    variable = variable,
    n        = length(vals),
    mean     = round(mean(vals), 3),
    sd       = round(sd(vals), 3),
    skewness = round(mean(((vals - mean(vals)) / sd(vals))^3), 3),
    shapiro_p = round(sw$p.value, 5),
    is_normal = sw$p.value > 0.05,
    histogram = list(
      breaks = round(h$breaks, 2),
      counts = h$counts
    )
  )
}
