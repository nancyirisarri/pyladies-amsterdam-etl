FROM rocker/r-ver:3.5.1

LABEL maintainer="Nancy Irisarri Mendez <nancyirisarri@gmail.com>"

# Install R dependencies
RUN /bin/bash -c set -o pipefail && \
    # Hotfix repo connection error since 4 september 2019 @Microsoft - Just remove it for now.
    sed -i '/microsoft/d' /usr/local/lib/R/etc/Rprofile.site && \
    # Install required build-dependencies.
    BUILDDEPS="libcurl4-openssl-dev \
        libpq-dev \
        libssl-dev \
        libxml2-dev \
        make \
        r-cran-littler \
        zlib1g-dev" && \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends $BUILDDEPS && \
    apt-get update -qq && \
    apt-get -y --no-install-recommends install libglu1-mesa-dev && \
    R -e "install.packages('dplyr', dependencies = TRUE, repos = 'http://cran.rstudio.com/')" && \
    R -e "install.packages('readr', dependencies = TRUE, repos = 'http://cran.rstudio.com/')" && \
    apt-get remove --purge -y $BUILDDEPS && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    rm -rf /tmp/*

# Install Python and dependencies
RUN export DEBIAN_FRONTEND=noninteractive; \
    # Install required packages.
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y --no-install-recommends \
        git \
        python3 \
        python3-pip \
        ssh-client && \
    pip3 install wheel && \
    pip3 install setuptools && \
    pip3 install pandas && \
    pip3 install google-cloud-bigquery && \
    pip3 install google-cloud-storage && \
    # Cleanup.
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    rm -rf /tmp/* && \
    rm -r /root/.cache && \
    find /usr/lib/python3.*/ -name 'tests' -exec rm -r '{}' + && \
    rm /usr/include/xlocale.h

COPY pyladiesamsterdametl /src

COPY data /src/data

# Run as user nobody
RUN mkdir -p /nonexistent/.ssh && \
    chown -R nobody.nogroup /src/ /nonexistent/.ssh/
USER nobody

CMD ["python3", "-m", "src.main"]

