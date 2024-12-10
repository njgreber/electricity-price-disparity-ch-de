# Base image with Python
FROM --platform=linux/arm64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy repo files into the container
COPY . .

# Add retry and mirror configuration
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries \
    && echo "deb [trusted=yes] http://ftp.debian.org/debian bookworm main" > /etc/apt/sources.list \
    && echo "deb [trusted=yes] http://ftp.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb [trusted=yes] http://security.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list

# Install required system dependencies and Python packages
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        texlive-latex-base \
        texlive-fonts-recommended \
        texlive-latex-recommended \
        texlive-fonts-extra \
        texlive-latex-extra \
        latexmk \
    && rm -rf /var/lib/apt/lists/*

# Install Jupyter Notebook and register the kernel
RUN pip install --upgrade pip \
    && pip install jupyter ipykernel \
    && python -m ipykernel install --user --name python3 --display-name "Python 3 (Docker)"

# Install additional Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Jupyter port
EXPOSE 8888

# Default command
CMD ["tail", "-f", "/dev/null"]