# Electricity Price Disparity CH-DE

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

We are interested in analyzing the auction prices from the Joint Allocation Office (JAO) at the Swiss border, where electricity production and supply companies purchase capacity for importing and exporting electricity. Specifically, we aim to investigate whether the auction prices at the border between Switzerland and Germany correspond to the price differences in the respective day-ahead electricity markets. We plan to use the day-ahead prices from the entso-e transparency platform and auction price data via the JAO API.

## Setup Instructions

### Prerequisites

- **Docker**: Make sure Docker is installed and running on your system.
- **JAO API Authentication Key**: Access to the JAO API requires an authentication key. You’ll need to include this key in the Python script to authorize API requests.

### Obtaining the JAO API Key

1. Visit the [JAO API documentation](https://www.jao.eu/) and follow their instructions for requesting an API key.
2. Once you receive your key, keep it secure, as you’ll need to insert it into the script before running the project.

### Project Structure

- `Dockerfile`: Defines the Docker environment with Python.
- `requirements.txt`: Lists required Python packages.
- `/data/raw/data_api_script.py`: The main Python script that connects to the JAO API and pulls data.

### Preparing the Script for Authentication

Before running the script, ensure you add the API key to the `headers` variable in `data_api_script.py`:

```python
headers = {"AUTH_API_KEY": "your_api_key_here"}
```

The PV data from: https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/monitoring-energiestrategie-2050.exturl.html/aHR0cHM6Ly9wdWJkYi5iZmUuYWRtaW4uY2gvZGUvcHVibGljYX/Rpb24vZG93bmxvYWQvMTAzMjI=.html 


## Python-LaTeX Docker Environment

This project provides a Dockerized environment for working with Python, Jupyter Notebook, and LaTeX. The setup ensures compatibility for both browser-based Jupyter workflows and development within Visual Studio Code (VS Code).

---

### Features

- **Python & Jupyter**: Pre-configured Python environment with Jupyter Notebook support.
- **LaTeX**: Pre-installed LaTeX packages for compiling `.tex` files.
- **VS Code Integration**: Designed to work seamlessly with the VS Code Remote - Containers extension.
- **Browser Access**: Jupyter Notebook accessible in your web browser.

---

### Setup

#### 1. Build the Container

To build the container, run:
```bash
make build
```
Once built, reopen the folder in VS Code using the **Remote - Containers** extension to start working within the Docker container.

---

#### 2. Run Jupyter Notebook

##### Option 1: Access via Browser

Start Jupyter Notebook and access it in your browser:
```bash
make jupyter-browser
```
The command will output a link (e.g., `http://127.0.0.1:8888`). Copy and paste it into your browser to interact with your notebooks.

##### Option 2: Access via VS Code

1. Open a `.ipynb` file in VS Code.
2. Ensure the Jupyter kernel is set to **Python 3 (Docker)**.

---

#### 3. Run the Full Pipeline

To execute the complete pipeline (data processing, notebook execution, and LaTeX compilation), run:
```bash
make run-all
```

---

### File Overview

#### `docker-compose.yml`

Defines the services and configurations for the Docker container.

#### `.devcontainer/devcontainer.json`

Configures the development environment for VS Code.

#### `Dockerfile`

Specifies the container setup, including:
- Python 3.10
- LaTeX packages
- Installation of Python dependencies from `requirements.txt`.

#### `Makefile`

Defines the available commands:
- `make build`: Builds the Docker container.
- `make jupyter-browser`: Starts Jupyter Notebook and opens it in a browser.
- `make process`: Executes and updates Jupyter Notebooks.
- `make compile`: Compiles LaTeX files to generate PDFs.
- `make run-all`: Runs the full pipeline (build, process, compile).

---

### Commands Overview

| Command                | Description                                      |
|------------------------|--------------------------------------------------|
| `make build`           | Builds the Docker container.                     |
| `make jupyter`         | Starts Jupyter Notebook (no browser).            |
| `make jupyter-browser` | Starts Jupyter Notebook and opens it in a browser. |
| `make process`         | Executes and updates Jupyter Notebooks.          |
| `make compile`         | Compiles LaTeX files to generate PDFs.           |
| `make run-all`         | Runs the full pipeline (build, process, compile).|

---

### Notes

- Ensure you have Docker installed and running on your machine.
- Use the VS Code **Remote - Containers** extension for a fully integrated development environment.

This setup is designed for flexibility and ease of use in both browser and VS Code-based workflows. Let us know if further adjustments are needed!


## Project Organization

```
├── README.md          <- The top-level README for developers using this project.
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── Dockerfile         <- Dockerfile for creating a Docker image
│
├── data
│   ├── processed               <- The final, canonical data sets for modeling.
│   └── raw                     <- The original, immutable data dump.
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│   │
│   ├── 1_process_data.ipynb    <- Makes the data ready for analysis
│   └── 2_analysis.py           <- Main Analysis Notebook
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   │
│   ├── main.tex                <- The main report tex file
│   └── figures                 <- Generated graphics and figures to be used in reporting
│
│
└── src                <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes src a Python module
    ├── config.py               <- Store useful variables and configuration
    ├── features.py             <- Code to create features for modeling
    ├── datafeed                <- Scripts to download or generate data
    │   ├── __init__.py 
    │   ├── connect.py          <- Code to connect to the JAO API
    │   ├── upstream.py         <- Code to run model inference with trained models          
    │   └── utilities.py        <- Code to train models
    └── plots.py                <- Code to create visualizations
```

--------

