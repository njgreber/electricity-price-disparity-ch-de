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

