FROM python:3.15.0b1-slim

# nmap is the scanner binary that python-nmap drives
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

# Create directory for output
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
ENTRYPOINT ["netprobe"]
CMD ["--help"]
