FROM r-base:4.3.3

# Install system deps needed for R packages
RUN apt-get update && \
    apt-get install -y -o Dpkg::Options::="--force-overwrite" --no-install-recommends \
    libcurl4-gnutls-dev libssl-dev libxml2-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Install R packages one by one for better error visibility
RUN Rscript -e "install.packages('jsonlite', repos='https://cloud.r-project.org/')"
RUN Rscript -e "install.packages('plumber', repos='https://cloud.r-project.org/')"
RUN Rscript -e "install.packages('dplyr', repos='https://cloud.r-project.org/')"

WORKDIR /app

# Copy R scripts
COPY r-analytics/api.R /app/api.R

# Create data directory
RUN mkdir -p /app/data/raw /app/data/processed

EXPOSE 8787

CMD ["Rscript", "-e", "pr <- plumber::plumb('/app/api.R'); pr$run(host='0.0.0.0', port=8787)"]
