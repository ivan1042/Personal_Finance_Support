import matplotlib.pyplot as plt
from returns import *
import numpy as np
import scipy.stats as stats

#No assumption
confidence_level = 0.95
historical_var = -np.percentile(df["%Change"], (1 - confidence_level) * 100)

#Assume normal distribution
mu = np.mean(df["%Change"])
sigma = np.std(df["%Change"])
z_score = stats.norm.ppf(1 - confidence_level)
parametric_var = mu - z_score * sigma

print(f"Historical VaR (95% Confidence): {historical_var:.2%}")
print(f"Parametric VaR (95% Confidence): {parametric_var:.2%}")

plt.hist(df["%Change"])
plt.show()