from analytics import returns
from analytics import risk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df, monthly_art_mean, yearly_art_mean, monthly_geo_mean, yearly_geo_mean = returns.stats()
stock = ["VFINX", "AAPL"]
max_sim = 100
time = (100 - 65) * 12
initial_amount = 10000
weight = np.array([0.5, 0.5]).T
meanM = np.full(shape = (time, len(weight)), fill_value = monthly_geo_mean)
meanM = meanM.T
portfolio_sim = np.full(shape = (time, max_sim), fill_value = 0.0)
if len(stock) <= 1:
    cov_matrix = np.array([[risk.volatility ** 2]])
else:
    return_df = df["Ratio"]
    cov_matrix = return_df.cov()

for m in range(0, max_sim):
    Z = np.random.normal(size = (time, len(weight)))
    L = np.linalg.cholesky(cov_matrix)
    monthly_return = meanM + np.inner(L, Z)
    portfolio_sim[: ,m] = np.cumprod(np.inner(weight, monthly_return.T + 1)) * initial_amount

plt.plot(portfolio_sim)
plt.show()