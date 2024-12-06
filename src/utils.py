import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox
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

def test_variance_trend(df):
   # Calculate average prices
   df['avg_price'] = (df['CH'] + df['DE-LU'])/2
   
   # Calculate normalized error
   df['norm_error'] = df['error']/df['avg_price']
   
   # Calculate rolling variance (e.g., monthly)
   rolling_var = df['norm_error'].rolling(window=24*4*30).var()  # 30 days
   
   # Test for trend in variance
   time_index = np.arange(len(rolling_var))
   slope, intercept, r_value, p_value, std_err = stats.linregress(
       time_index[~np.isnan(rolling_var)], 
       rolling_var.dropna()
   )
   
   return {
       'slope': slope,
       'p_value': p_value,
       'r_squared': r_value**2
   }