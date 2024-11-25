"""
Analyse the price differences between the bidding zones
together with the cross-border prices.
"""

import pandas as pd
import matplotlib.pyplot as plt

path = "src/data/raw/ch-de/"

################################################### Read Day-Ahead Data

bidding_zones = ["CH", "DE-LU", "DE-AT-LU"]
bidding_zones_others = ["DE-LU", "DE-AT-LU"]
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

# Dictionary to store dataframes
dataframes = {}

# Dictionary to store concatenated dataframes for each bidding zone
df = {}

for bidding_zone in bidding_zones:
    # List to hold dataframes for a particular bidding zone
    dfs = []
    for year in years:
        # Create a unique key for each dataframe
        try:
            key = f"{bidding_zone}_{year}"
            file_name = f"{path}{bidding_zone}_Day-ahead Prices_{year}.csv"

            print(f"{path}{bidding_zone}_Day-ahead Prices_{year}.csv")

            # import csv file and store it in the dictionary
            dataframes[key] = pd.read_csv(file_name)
            dfs.append(dataframes[key])
        except:
            pass
    # concatenating dataframes for each bidding zone
    df[bidding_zone] = pd.concat(dfs)

for bidding_zone in bidding_zones:
    # Ensure the index is a datetime
    df[bidding_zone]["MTU (CET/CEST)"] = pd.to_datetime(
        df[bidding_zone]["MTU (CET/CEST)"].str.split(" - ").str[0],
        dayfirst=True,
        errors="coerce",
    )
    df[bidding_zone].sort_values(by="MTU (CET/CEST)", inplace=True)
    df[bidding_zone].set_index("MTU (CET/CEST)", inplace=True)
    df[bidding_zone]["Day-ahead Price [EUR/MWh]"] = pd.to_numeric(
        df[bidding_zone]["Day-ahead Price [EUR/MWh]"], errors="coerce"
    )


df_de_ch = pd.read_csv("src/data/raw/jao_de_ch_hourly.csv")

df_de_ch["start_hour"] = df_de_ch["productHour"].str.split("-").str[0]
df_de_ch["datetime"] = pd.to_datetime(df_de_ch["date"] + " " + df_de_ch["start_hour"])
df_de_ch = df_de_ch.drop(["Unnamed: 0", "date", "productHour", "start_hour"], axis=1)

de1 = df["DE-LU"]["Day-ahead Price [EUR/MWh]"] - df["CH"]["Day-ahead Price [EUR/MWh]"]
de2 = (
    df["DE-AT-LU"]["Day-ahead Price [EUR/MWh]"] - df["CH"]["Day-ahead Price [EUR/MWh]"]
)

DE1 = pd.merge(
    left=de1, right=df_de_ch, left_on="MTU (CET/CEST)", right_on="datetime", how="right"
)

DE2 = pd.merge(
    left=de2, right=df_de_ch, left_on="MTU (CET/CEST)", right_on="datetime", how="right"
)

# rolling means
DE1["7d_auction_price"] = DE1["auctionPrice"].rolling(window=168, min_periods=1).mean()
DE1["7d_day_ahead"] = (
    DE1["Day-ahead Price [EUR/MWh]"].rolling(window=168, min_periods=1).mean()
)

DE2["7d_auction_price"] = DE2["auctionPrice"].rolling(window=168, min_periods=1).mean()
DE2["7d_day_ahead"] = (
    DE2["Day-ahead Price [EUR/MWh]"].rolling(window=168, min_periods=1).mean()
)


plt.figure(figsize=(12, 6))

# Plot 30-day average of "Day-ahead Price [EUR/MWh]"
plt.plot(
    DE1["datetime"],
    DE1["7d_day_ahead"],
    label="7-day Average Day-Ahead Price Difference",
    color="blue",
)

# Shade the area for the 30-day average of the price difference
plt.fill_between(
    DE1["datetime"],
    DE1["7d_day_ahead"],
    DE1["7d_day_ahead"] + DE1["7d_auction_price"],
    color="skyblue",
    alpha=0.3,
    label="7-day Average Auction Price",
)

plt.ylabel("7-Day Average Price [EUR/MWh]")
plt.title(
    "7-Day Average Day-ahead Price Difference between DE-LU and CH plus JAO Auction price DE-CH"
)
plt.legend()
# Show the plot
plt.grid(True)


plt.figure(figsize=(12, 6))

# Plot 30-day average of "Day-ahead Price [EUR/MWh]"
plt.plot(
    DE2["datetime"],
    DE2["7d_day_ahead"],
    label="7-day Average Day-Ahead Price Difference",
    color="blue",
)

# Shade the area for the 30-day average of the price difference
plt.fill_between(
    DE2["datetime"],
    DE2["7d_day_ahead"],
    DE2["7d_day_ahead"] + DE2["7d_auction_price"],
    color="skyblue",
    alpha=0.3,
    label="7-day Average Auction Price",
)


plt.ylabel("7-Day Average Price [EUR/MWh]")
plt.title(
    "7-Day Average Day-ahead Price Difference between DE-AT-LU and CH plus JAO Auction price DE-CH"
)
plt.legend()

# Show the plot
plt.grid(True)
plt.show()
