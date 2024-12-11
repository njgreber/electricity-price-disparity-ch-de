"""
utils.py
A collection of statistical tests for the analysis in 3_results.ipynb
"""


import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

def test_stationarity(series):
    """
    Conducts the Augmented Dickey-Fuller (ADF) test to check if a time series is stationary.

    Args:
        series (pd.Series): The time series to be tested.

    Returns:
        dict: A dictionary containing:
            - 'adf_stat': The ADF test statistic.
            - 'p_value': The p-value for the test.
    """
    result = adfuller(series.dropna())  # Drops missing values before running the test
    return {'adf_stat': result[0], 'p_value': result[1]}


def test_autocorr_specific_lag(series, lag):
    """
    Tests for autocorrelation at a specific lag using the z-statistic.

    Args:
        series (pd.Series): The time series to be tested.
        lag (int): The lag at which autocorrelation is evaluated.

    Returns:
        dict: A dictionary containing:
            - 'acf': The autocorrelation coefficient at the specified lag.
            - 'z_stat': The z-statistic for the autocorrelation.
            - 'p_value': The p-value for the z-statistic (two-sided test).
    """
    acf = pd.Series(series).autocorr(lag=lag)  # Autocorrelation at the specified lag
    n = len(series)  # Number of observations in the series
    se = np.sqrt(1 / n)  # Standard error under the null hypothesis
    z_stat = acf / se  # Z-statistic for the autocorrelation
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))  # Two-sided p-value for the z-statistic
    return {'acf': acf, 'z_stat': z_stat, 'p_value': p_value}


def run_hac_test(series):
    """
    Performs a mean test with Newey-West Heteroskedasticity and Autocorrelation Consistent (HAC) standard errors.

    Args:
        series (pd.Series): The time series to be tested.

    Returns:
        dict: A dictionary containing:
            - 't_stat': The t-statistic for the mean test.
            - 'p_value': The p-value for the test.
    """
    X = np.ones(len(series.dropna()))  # Constant term for the regression (mean test)
    y = series.dropna()  # Drops missing values
    model = sm.OLS(y, X)  # Ordinary Least Squares regression
    results = model.fit(cov_type='HAC', cov_kwds={'maxlags': 96})  # HAC-adjusted standard errors
    return {
        't_stat': float(results.tvalues.iloc[0]),  # Extract the t-statistic
        'p_value': float(results.pvalues.iloc[0])  # Extract the p-value
    }

def test_variance_trend(series1, series2, error_series, window_days=30):
   """
   Test for trend in normalized error variance
   
   Args:
       series1: First day-ahead price series
       series2: Second day-ahead price series 
       error_series: Error series
       window_days: Rolling window size in days
   """
   # Calculate normalized error
   avg_price = (series1 + series2)/2
   norm_error = error_series/avg_price
   
   # Calculate rolling variance
   rolling_var = norm_error.rolling(window=window_days).var()
   
   # Test for trend
   time_index = np.arange(len(rolling_var))
   slope, _, r_value, p_value, _ = stats.linregress(
       time_index[~np.isnan(rolling_var)], 
       rolling_var.dropna()
   )
   
   return {
       'slope': slope,
       'p_value': p_value,
       'r_squared': r_value**2
   }



def variance_ratio_test(series1, series2, error_series, split_ratio=0.5):
    """
    Perform a variance ratio test to compare the variances between two time periods.
    
    Args:
        series: The time series to analyze (e.g., normalized error term).
        split_ratio: The fraction of the series to assign to the first period (default: 0.5).
        
    Returns:
        A dictionary containing the variance ratio, F-statistic, and p-value.
    """
    # Calculate normalized error   
    avg_price = (series1 + series2)/2
    norm_error = error_series/avg_price
   
    # Split the series into two periods
    split_index = int(len(norm_error) * split_ratio)
    series_early = norm_error[:split_index]
    series_late = norm_error[split_index:]
    
    # Calculate variances
    var_early = np.var(series_early, ddof=1)
    var_late = np.var(series_late, ddof=1)
    
    # Variance ratio
    variance_ratio = var_late / var_early
    
    # F-statistic
    df1 = len(series_late) - 1  # Degrees of freedom for the later period
    df2 = len(series_early) - 1  # Degrees of freedom for the earlier period
    f_statistic = variance_ratio
    
    # Two-tailed p-value
    p_value = 2 * min(stats.f.cdf(f_statistic, df1, df2), 1 - stats.f.cdf(f_statistic, df1, df2))
    
    return {
        "variance_ratio": variance_ratio,
        "f_statistic": f_statistic,
        "p_value": p_value,
        "df1": df1,
        "df2": df2
    }
def run_yearly_tests(df, years):
    """
    Performs yearly statistical tests on the error term to evaluate stationarity, 
    mean deviation, and autocorrelation for each year in the dataset.

    Args:
        df (pd.DataFrame): A DataFrame with a DateTime index and a column 'error' 
                           containing the time series to be analyzed.
        years (list): A list of years to be analyzed.

    Returns:
        pd.DataFrame: A DataFrame summarizing the results of the statistical tests 
                      for each year, including:
                      - ADF Statistic and p-value
                      - HAC-adjusted t-statistic and p-value
                      - Autocorrelation at lag 24 and its p-value
    """
    results = {}  # Initialize a dictionary to store results for each year

    for year in years:
        # Filter data for the specific year
        year_df = df[df.index.year == year].copy()

        # Augmented Dickey-Fuller (ADF) Test for stationarity
        adf_result = adfuller(year_df['error'].dropna())[0:2]  # ADF Statistic and p-value

        # HAC-adjusted t-test for mean deviation
        X = np.ones(len(year_df['error'].dropna()))  # Constant term for regression
        y = year_df['error'].dropna()  # Drop missing values
        model = sm.OLS(y, X)  # Ordinary Least Squares regression
        hac_results = model.fit(cov_type='HAC', cov_kwds={'maxlags': 96})  # HAC adjustment

        # Autocorrelation at lag 24
        autocorr = year_df['error'].autocorr(lag=24)  # Compute autocorrelation
        n = len(year_df['error'])  # Number of observations
        t_stat = autocorr * np.sqrt((n - 2) / (1 - autocorr**2))  # t-statistic for autocorrelation
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), n - 2))  # Two-sided p-value for t-statistic

        # Store results for the year
        results[year] = {
            'ADF_stat': adf_result[0],
            'ADF_pvalue': adf_result[1],
            'HAC_tstat': float(hac_results.tvalues.iloc[0]),
            'HAC_pvalue': float(hac_results.pvalues.iloc[0]),
            'Autocorr_24': autocorr,
            'Autocorr_pvalue': p_value
        }

    # Create a DataFrame to summarize yearly results
    df_results = pd.DataFrame({
        'Year': list(results.keys()),  # Years
        'ADF Statistic': [results[y]['ADF_stat'] for y in years],  # ADF statistics
        'ADF p-value': [results[y]['ADF_pvalue'] for y in years],  # ADF p-values
        'HAC t-stat': [results[y]['HAC_tstat'] for y in years],  # HAC t-statistics
        'HAC p-value': [results[y]['HAC_pvalue'] for y in years],  # HAC p-values
        'Autocorr(24)': [results[y]['Autocorr_24'] for y in years],  # Autocorrelation
        'Autocorr p-value': [results[y]['Autocorr_pvalue'] for y in years]  # Autocorrelation p-values
    })

    # Return the results as a DataFrame, setting 'Year' as the index and rounding values
    return df_results.set_index('Year').round(4)
