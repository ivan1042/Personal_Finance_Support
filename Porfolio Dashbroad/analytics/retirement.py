from analytics.returns import *
from analytics.risk import *

def retirement_amount(monthly_geo_mean,
                      retire_age = 65, death_age = 100, monthly_expense = 8681, yearly_inflation = 0.03):
    period = (death_age - retire_age) * 12
    monthly_return = monthly_geo_mean - 1
    monthly_inflation = (1 + yearly_inflation) ** (1/12) - 1

    cash = monthly_expense / (monthly_return - monthly_inflation)
    ratio = (1 - ((1 + monthly_inflation )/ (1 + monthly_return )) ** period)

    retirement_amount = cash * ratio
    return f"{retirement_amount:.0f}"

