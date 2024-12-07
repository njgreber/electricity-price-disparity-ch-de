import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy import stats
import statsmodels.api as sm
import matplotlib.pyplot as plt


def test_stationarity(series):
   result = adfuller(series.dropna())
   return {'adf_stat': result[0], 'p_value': result[1]}

def test_autocorr_specific_lag(series, lag):
   acf = pd.Series(series).autocorr(lag=lag)
   n = len(series)
   se = np.sqrt(1/n)  # Standard error under null hypothesis
   z_stat = acf/se
   p_value = 2*(1 - stats.norm.cdf(abs(z_stat)))  # Two-sided test
   return {'acf': acf, 'z_stat': z_stat, 'p_value': p_value}


def run_hac_test(series):
   X = np.ones(len(series.dropna()))
   y = series.dropna()
   model = sm.OLS(y, X)
   results = model.fit(cov_type='HAC', cov_kwds={'maxlags': 96})
   return {
       't_stat': float(results.tvalues.iloc[0]),
       'p_value': float(results.pvalues.iloc[0])
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
