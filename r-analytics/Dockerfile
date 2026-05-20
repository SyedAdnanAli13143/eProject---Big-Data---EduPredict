FROM rocker/r-ver:4.3.2

# Install ALL system deps needed for plumber and its dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev libssl-dev libxml2-dev \
    libsodium-dev zlib1g-dev make gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Install R packages separately so errors are visible
RUN Rscript -e "install.packages('jsonlite', repos='https://cloud.r-project.org/')"
RUN Rscript -e "install.packages('plumber', repos='https://cloud.r-project.org/')"

# Verify plumber installed
RUN Rscript -e "library(plumber); cat('plumber OK\n')"

WORKDIR /app
COPY r-analytics/api.R /app/api.R
COPY r-analytics/analysis.R /app/analysis.R
COPY r-analytics/visualizations.R /app/visualizations.R
RUN mkdir -p /app/data/raw /app/data/processed /app/plots

EXPOSE 8787
CMD ["Rscript", "-e", "pr <- plumber::plumb('/app/api.R'); pr$run(host='0.0.0.0', port=8787)"]
