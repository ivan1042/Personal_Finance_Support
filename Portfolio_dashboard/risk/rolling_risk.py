import pandas as pd
import scipy.stats as stats
import numpy as np


confidence_level = 0.95
period = 36

def rolling_calc(df, risk_free, benchmark):

    output = pd.DataFrame()
    df.dropna(inplace=True)
    #No assumption
    output["historical_VaR"] = df.rolling(36).quantile((1 - confidence_level)) - 1
    #print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")

    #Assume normal distribution
    output["mu"] = df.rolling(period).mean()
    output["sigma"] = df.rolling(window=period).std()
    z_score = stats.norm.ppf(1 - confidence_level)
    output["parametric_VaR"] = output["mu"] + z_score * output["sigma"] - 1
    #print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")



    output["volatility"] = output["sigma"]
    output["Beta"] = df.rolling(window=36).cov(benchmark) / (benchmark.rolling(window=period).std()) ** 2
    output["Expected_return"] = (benchmark.rolling(window=period).mean() - risk_free) * output["Beta"] + risk_free
    output["sharpe_ratio"] = (output["mu"] - (risk_free) )/ output["volatility"]

    output["downside_volatility"] = df[df <= output["Expected_return"]].dropna().rolling(window=period).std()
    output["sortino_ratio"] = (output["mu"] - (risk_free ) )/ output["downside_volatility"]

    def window_max_drawdown(gross_factors):
        wealth = np.r_[1.0, gross_factors].cumprod()
        drawdown = wealth / np.maximum.accumulate(wealth) - 1
        return drawdown.min()

    output["max_drawdown"] = df.rolling(
        window=period,
        min_periods=period,
    ).apply(window_max_drawdown, raw=True)
    print(output)
    return output
