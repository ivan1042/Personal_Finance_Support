import numpy as np
import scipy.stats as stats

confidence_level = 0.95

def historical_VaR():#No assumption
    historical_VaR = np.percentile(df["%Change"], (1 - confidence_level) * 100)
    print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")
    return historical_VaR
#Assume normal distribution
def parametric_VaR():
    mu = np.mean(df["%Change"])
    sigma = np.std(df["%Change"])
    z_score = stats.norm.ppf(1 - confidence_level)
    parametric_VaR = mu - z_score * sigma
    print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")
    return parametric_VaR

def volatility():
    volatility = np.std(df["%Change"], ddof=1)
    return volatility

print(historical_VaR())

