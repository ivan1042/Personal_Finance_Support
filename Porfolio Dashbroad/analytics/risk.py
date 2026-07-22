import numpy as np
import scipy.stats as stats
from analytics import returns

confidence_level = 0.95
risk_free = 0.045

def risk_calc(df, monthly_art_mean, yearly_art_mean, monthly_geo_mean, yearly_geo_mean):

    #No assumption
    historical_VaR = np.percentile(df["%Change"], (1 - confidence_level) * 100)
    #print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")

    #Assume normal distribution
    mu = np.mean(df["%Change"])
    sigma = np.std(df["%Change"])
    z_score = stats.norm.ppf(1 - confidence_level)
    parametric_VaR = mu - z_score * sigma
    #print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")



    volatility = np.std(df["%Change"], ddof=1)
    sharpe_ratio = (monthly_geo_mean - ((1 + risk_free)**(1/12) ) )/ volatility

    downside_volatility = np.std(df[df["%Change"] <= 0]["%Change"], ddof=1)
    sortino_ratio = (monthly_geo_mean - ((1 + risk_free)**(1/12) ) )/ downside_volatility

    max_drawdown = np.min(df["%Change"])

    return [historical_VaR, parametric_VaR, sharpe_ratio, sortino_ratio, max_drawdown]