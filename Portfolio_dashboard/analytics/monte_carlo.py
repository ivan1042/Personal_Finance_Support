import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

max_sim = 100
def simulation(raw_mon_return_temp, mon_re_temp, stock = ["VFINX", "AAPL"], weight = [0.7, 0.3], timeframe = 40):
    return_df = pd.concat(raw_mon_return_temp, axis=1)
    return_matrix = np.array(mon_re_temp).T
    time = timeframe * 12
    initial_amount = 10000
    weight = np.array(weight).T
    meanM = np.full(shape = (time, len(weight)), fill_value = return_matrix - 1)
    meanM = meanM.T
    portfolio_sim = np.full(shape = (time, max_sim), fill_value = 0.0)
    if len(stock) == 1:
        variance = return_df.iloc[:, 0].var(ddof=0)
        cov_matrix = np.array([[variance]])
    else:
        cov_matrix = return_df.cov()

    L = np.linalg.cholesky(cov_matrix)

    for m in range(0, max_sim):
        Z = np.random.normal(size = (time, len(weight)))
        monthly_return = meanM + np.inner(L, Z)
        portfolio_sim[: ,m] = np.cumprod(np.inner(weight, monthly_return.T + 1)) * initial_amount

    return portfolio_sim
