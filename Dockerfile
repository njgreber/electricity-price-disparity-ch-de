# Base image with Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy repo files into the container
COPY . .

# Install required system dependencies and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    texlive-latex-base \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-fonts-extra \
    texlive-latex-extra \
    latexmk \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Default command to keep container running
CMD ["tail", "-f", "/dev/null"]

