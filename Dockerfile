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

# Install Jupyter Notebook and register the kernel
RUN pip install --upgrade pip \
    && pip install jupyter ipykernel \
    && python -m ipykernel install --user --name python3 --display-name "Python 3 (Docker)"

# Install additional Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Jupyter port for browser and VS Code
EXPOSE 8888

# Default command to keep the container running
CMD ["tail", "-f", "/dev/null"]

