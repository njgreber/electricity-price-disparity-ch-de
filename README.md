# Electricity Price Disparity CH-DE

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

We are interested in analyzing the auction prices from the Joint Allocation Office (JAO) at the Swiss border, where electricity production and supply companies purchase capacity for importing and exporting electricity. Specifically, we aim to investigate whether the auction prices at the border between Switzerland and Germany correspond to the price differences in the respective day-ahead electricity markets. We plan to use the day-ahead prices from the entso-e transparency platform and auction price data via the JAO API.

# Electricity Price Disparity Analysis

This project analyzes electricity auction prices from the JAO API between Germany and Switzerland. It uses Docker to set up a reproducible environment with Python, ensuring that the data-gathering script can run independently of local dependencies.

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
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         electricity_price_disparity_ch_de and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── electricity_price_disparity_ch_de   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes electricity_price_disparity_ch_de a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

