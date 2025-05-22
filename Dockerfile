FROM python:3.13-slim

# Install system dependencies including nmap
RUN apt-get update && apt-get install -y \
    nmap \
    libsnmp-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create directories for output and templates
RUN mkdir -p /app/output /app/templates

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
ENTRYPOINT ["network-discovery"]
CMD ["--help"]
