# Get the base image
FROM openjdk:8-jdk-slim-buster
COPY --from=python:3.7-slim-buster / /
LABEL maintainer="Abdurrahman Ansari <sm_ar_t@yahoo.com>"

# Argument for labels
ARG BUILD_DATE
ARG VCS_REF
ARG BUILD_VERSION

# Labels
LABEL com.asansari.schema-version="1.0"
LABEL com.asansari.build-date=$BUILD_DATE
LABEL com.asansari.name="Pay Slip Analysis"
LABEL com.asansari.description="Pay Slip Analysis"
LABEL com.asansari.url="https://www.asansari.com/"
LABEL com.asansari.vcs-url="https://github.com/asansari/payslip-analysis"
LABEL com.asansari.vcs-ref=$VCS_REF
LABEL com.asansari.vendor="Abdurrahman Ansari"
LABEL com.asansari.version=$BUILD_VERSION
LABEL com.asansari.docker.cmd='docker run -it --rm --name payslip-analysis-container -v "$PWD":/usr/src/app -w /usr/src/app payslip-analysis:1.0'

# Set the workign directory
WORKDIR /usr/src/app

# Copy requirements.txt to install the required dependencies
COPY requirements.txt constants.py pay_slip_analysis.py environment.py ./

# Install Python libraries followed by setting the locale
RUN DEBIAN_FRONTEND=noninteractive && \
apt-get update && \
apt-get install --no-install-recommends -y locales && \
localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 && \
pip install --default-timeout=120 --no-cache-dir -r requirements.txt

# Trigger the script to generate assets
ENTRYPOINT [ "python", "-B", "./pay_slip_analysis.py" ]
