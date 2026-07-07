from returns import *
import numpy as np
import scipy.stats as stats

#No assumption
confidence_level = 0.95
historical_VaR = np.percentile(df["%Change"], (1 - confidence_level) * 100)
#Assume normal distribution
mu = np.mean(df["%Change"])
volatility = np.std(df["%Change"], ddof=1)
sigma = np.std(df["%Change"])
z_score = stats.norm.ppf(1 - confidence_level)
parametric_VaR = mu - z_score * sigma

print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")
print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")
