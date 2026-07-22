from scipy.stats import gmean
import pandas as pd

def returns(df):

    monthly_art_mean = df["Ratio"].mean()
    yearly_art_mean = monthly_art_mean**12-1
    monthly_geo_mean = gmean(df["Ratio"])
    yearly_geo_mean = monthly_geo_mean**12-1

    return [monthly_art_mean, yearly_art_mean, monthly_geo_mean, yearly_geo_mean]






