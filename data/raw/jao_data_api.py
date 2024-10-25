# MONTHLY

import pandas as pd
import requests
import ast
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


Base_URL = "https://api.jao.eu/OWSMP/getauctions?"

headers = {"AUTH_API_KEY": "..."}

data = "results"

result = dict()

# Define the start and end dates
start_date = datetime(2016, 1, 1)
end_date = datetime(2023, 12, 1)

# Generate the first day of each month
first_days_of_month = []
current_date = start_date
while current_date <= end_date:
    first_days_of_month.append(current_date.strftime("%Y-%m-%d"))
    current_date += relativedelta(months=1)

i = 1
for day in first_days_of_month[:-1]:
    params = {
        "horizon": "Monthly",
        "corridor": "de-ch",  # CHANGE HERE
        "fromdate": day,
        "shadow": 0,
        "withoutcreditlimitrejection": True,
    }

    r = requests.get(Base_URL, headers=headers, params=params, json=data)
    j = r.json()
    df = pd.DataFrame.from_dict(j)
    df.to_csv("test1.csv")
    auction_prices = [d["auctionPrice"] for d in df["results"].iloc[0] if "auctionPrice" in d][0]
    gate_open = df["bidGateOpening"].iloc[0][:10]
    gate_close = df["bidGateClosure"].iloc[0][:10]

    month = first_days_of_month[i]

    result[month] = {
        "auction_prices": auction_prices,
        "bidGateOpening": gate_open,
        "bidGateClose": gate_close,
    }
    i += 1


result_df = pd.DataFrame(data=result).T

result_df.to_csv("de_ch_monthly.csv")  # CHANGE HERE
