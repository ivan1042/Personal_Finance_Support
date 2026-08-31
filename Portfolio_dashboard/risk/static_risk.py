import numpy as np
import pandas as pd
import scipy.stats as stats
from analytics import returns

confidence_level = 0.95
monthly_rf_ratio = ( 1 + 0.045 ) **(1/12)

def static_calc(df, monthly_art_mean, yearly_art_mean, monthly_geo_mean, yearly_geo_mean,
                risk_free, benchmark):

    #No assumption
    historical_VaR = np.percentile(df.dropna(), (1 - confidence_level) * 100) - 1
    #print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")

    #Assume normal distribution
    mu = np.mean(df)
    sigma = np.std(df)
    z_score = stats.norm.ppf(1 - confidence_level)
    parametric_VaR = mu + z_score * sigma - 1
    #print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")



    volatility = np.std(df, ddof=1)
    temp = pd.concat([df, benchmark], axis = 1, keys=['df', 'benchmark'])
    temp.dropna(inplace = True)
    beta = np.cov(temp["df"], temp["benchmark"])/ (np.std(temp["benchmark"]))**2
    expected_return = (np.mean(benchmark) - monthly_rf_ratio) * beta + monthly_rf_ratio
    sharpe_ratio = (mu - monthly_rf_ratio )/ volatility


    downside_volatility = np.std(df[df <= expected_return[0, 1]].dropna(), ddof=1)
    sortino_ratio = (mu - monthly_rf_ratio )/ downside_volatility

    wealth_index = np.cumprod(df.dropna())
    running_peaks = np.maximum.accumulate(wealth_index)
    drawdowns = (wealth_index - running_peaks) / running_peaks
    max_drawdown = np.min(drawdowns)

    return [historical_VaR, parametric_VaR, sharpe_ratio, sortino_ratio, max_drawdown, volatility]