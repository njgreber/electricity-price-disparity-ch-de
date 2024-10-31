import pandas as pd
import requests
import ast
from datetime import datetime, timedelta
from calendar import monthrange

Base_URL = "https://api.jao.eu/OWSMP/getauctions?"

headers = {"AUTH_API_KEY": "..."}

data = "results"

result = dict()

# Start and end years
start_year = 2016
end_year = 2022

dfs = []

# Loop through each year and month
for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        # First day of the month
        first_day = datetime(year, month, 1).strftime("%Y-%m-%d")
        # Last day of the month
        last_day = datetime(year, month, monthrange(year, month)[1]).strftime(
            "%Y-%m-%d"
        )

        params = {
            "horizon": "Daily",
            "corridor": "de-ch",
            "fromdate": first_day,
            "todate": last_day,
        }

        r = requests.get(Base_URL, headers=headers, params=params, json=data)
        j = r.json()
        df = pd.DataFrame.from_dict(j)

        df["new"] = pd.to_datetime(df["marketPeriodStart"]).dt.strftime("%d/%m/%Y")
        df = df.sort_values(by="new", ascending=True).reset_index(drop=True)

        last_day = len(df)

        for i_day in range(last_day):

            # Provided data structure
            data = df["results"][i_day]
            date = (
                datetime.fromisoformat(df["marketPeriodStart"][i_day])
                + timedelta(days=1)
            ).date()

            extracted_data = [
                {
                    "date": date,
                    "productHour": item["productHour"],
                    "auctionPrice": item["auctionPrice"],
                }
                for item in data
            ]

            ddf = pd.DataFrame(extracted_data)
            ddf = ddf.sort_values(by="productHour", ascending=True)
            dfs.append(ddf)


combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv("jao_de_ch_hourly.csv")
