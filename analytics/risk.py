import numpy as np
import scipy.stats as stats
from analytics.returns import *

confidence_level = 0.95
risk_free = 0.045

#No assumption
historical_VaR = np.percentile(df["%Change"], (1 - confidence_level) * 100)
print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")

#Assume normal distribution
mu = np.mean(df["%Change"])
sigma = np.std(df["%Change"])
z_score = stats.norm.ppf(1 - confidence_level)
parametric_VaR = mu - z_score * sigma
print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")



volatility = np.std(df["%Change"], ddof=1)
sharpe_ratio = (monthly_geo_mean - ((1 + risk_free)**(1/12) - 1) )/ volatility
