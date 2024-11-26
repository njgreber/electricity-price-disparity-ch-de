# MONTHLY

import pandas as pd
import requests
import ast

Base_URL = "https://api.jao.eu/OWSMP/getauctions?"

headers = {"AUTH_API_KEY": "47d85929-d42b-447a-9536-f217b9b27ee2"}

data = "results"

result = dict()


first_days_of_month = [
    "2016-01-01",
    "2016-02-01",
    "2016-03-01",
    "2016-04-01",
    "2016-05-01",
    "2016-06-01",
    "2016-07-01",
    "2016-08-01",
    "2016-09-01",
    "2016-10-01",
    "2016-11-01",
    "2016-12-01",
    "2017-01-01",
    "2017-02-01",
    "2017-03-01",
    "2017-04-01",
    "2017-05-01",
    "2017-06-01",
    "2017-07-01",
    "2017-08-01",
    "2017-09-01",
    "2017-10-01",
    "2017-11-01",
    "2017-12-01",
    "2018-01-01",
    "2018-02-01",
    "2018-03-01",
    "2018-04-01",
    "2018-05-01",
    "2018-06-01",
    "2018-07-01",
    "2018-08-01",
    "2018-09-01",
    "2018-10-01",
    "2018-11-01",
    "2018-12-01",
    "2019-01-01",
    "2019-02-01",
    "2019-03-01",
    "2019-04-01",
    "2019-05-01",
    "2019-06-01",
    "2019-07-01",
    "2019-08-01",
    "2019-09-01",
    "2019-10-01",
    "2019-11-01",
    "2019-12-01",
    "2020-01-01",
    "2020-02-01",
    "2020-03-01",
    "2020-04-01",
    "2020-05-01",
    "2020-06-01",
    "2020-07-01",
    "2020-08-01",
    "2020-09-01",
    "2020-10-01",
    "2020-11-01",
    "2020-12-01",
    "2021-01-01",
    "2021-02-01",
    "2021-03-01",
    "2021-04-01",
    "2021-05-01",
    "2021-06-01",
    "2021-07-01",
    "2021-08-01",
    "2021-09-01",
    "2021-10-01",
    "2021-11-01",
    "2021-12-01",
    "2022-01-01",
    "2022-02-01",
    "2022-03-01",
    "2022-04-01",
    "2022-05-01",
    "2022-06-01",
    "2022-07-01",
    "2022-08-01",
    "2022-09-01",
    "2022-10-01",
    "2022-11-01",
    "2022-12-01",
    "2023-01-01",
    "2023-02-01",
    "2023-03-01",
    "2023-04-01",
    "2023-05-01",
    "2023-06-01",
    "2023-07-01",
    "2023-08-01",
    "2023-09-01",
    "2023-10-01",
    "2023-11-01",
    "2023-12-01",
]

i = 1
for day in first_days_of_month[:-1]:
    params = {
        "horizon": "Daily",
        "corridor": "de-ch",  # CHANGE HERE
        "fromdate": day,
        "shadow": 0,
        "withoutcreditlimitrejection": True,
    }

    r = requests.get(Base_URL, headers=headers, params=params, json=data)
    j = r.json()
    df = pd.DataFrame.from_dict(j)
    df.to_csv("test1.csv")
    auction_prices = [
        d["auctionPrice"] for d in df["results"].iloc[0] if "auctionPrice" in d
    ][0]
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

result_df.to_csv("de-ch_daily.csv")  # CHANGE HERE
