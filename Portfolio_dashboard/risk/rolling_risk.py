import pandas as pd
import scipy.stats as stats
import numpy as np


confidence_level = 0.95
period = 36

def rolling_calc(df, risk_free, benchmark):

    output = pd.DataFrame()
    df.dropna(inplace=True)
    #No assumption
    output["historical_VaR"] = df.rolling(36).quantile((1 - confidence_level))
    #print(f"Historical VaR (95% Confidence): {historical_VaR:.2%}")

    #Assume normal distribution
    output["mu"] = df.rolling(period).mean()
    output["sigma"] = df.rolling(window=period).std()
    z_score = stats.norm.ppf(1 - confidence_level)
    output["parametric_VaR"] = output["mu"] - z_score * output["sigma"]
    #print(f"Parametric VaR (95% Confidence): {parametric_VaR:.2%}")



    output["volatility"] = output["sigma"]
    output["Beta"] = df.rolling(window=36).cov(benchmark) / (output["volatility"]) ** 2
    output["sharpe_ratio"] = (output["mu"] - ((1 + risk_free)**(1/12) ) )/ output["volatility"]

    output["downside_volatility"] = df[df <= 1].dropna().rolling(window=period).std()
    output["sortino_ratio"] = (output["mu"] - ((1 + risk_free)**(1/12) ) )/ output["downside_volatility"]

    output["wealth_index"] = df.rolling(36).apply(np.prod, raw=True)
    output["running_peaks"] = output["wealth_index"].rolling(36).max()
    output["drawdowns"] = (output["wealth_index"] - output["running_peaks"]) / output["running_peaks"]
    output["max_drawdown"] = output["drawdowns"].rolling(36).min()
    print(output)
    return output
