import pandas as pd
import os

# Function to load day-ahead price data for a specific bidding zone across multiple years
def load_price_series(bidding_zone, years, path="../data/raw/"):
    dfs = []  # List to store DataFrames for each year
    for year in years:
        # Construct the filename based on the bidding zone and year
        filename = f"{bidding_zone}_Day-ahead Prices_{year}.csv"
        filepath = os.path.join(path, filename)  # Full path to the file
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(filepath)
            # Parse the datetime from the "MTU (CET/CEST)" column and use the start time of the interval
            df["MTU (CET/CEST)"] = pd.to_datetime(
                df["MTU (CET/CEST)"].str.split(" - ").str[0],  # Extract the start time of the interval
                format="%d.%m.%Y %H:%M",  # Specify the format of the datetime
                errors="coerce"  # Coerce parsing errors to NaT
            )
            # Drop duplicate timestamps, keeping the first occurrence (means that one hour of each year is missing because CET/CEST changes,
            # but since all dataframes are in CET/CEST, this is not a problem and negligible for our analysis)
            df = df.loc[~df["MTU (CET/CEST)"].duplicated()]
            # Set the datetime column as the index
            df.set_index("MTU (CET/CEST)", inplace=True)
            # Append the "Day-ahead Price" column to the list of DataFrames
            dfs.append(df["Day-ahead Price [EUR/MWh]"])
        except Exception as e:
            # Ignore missing files or other exceptions and continue
            # Uncomment the print statement to debug missing files
            print(f"Missing {filepath}: {e}")
            continue
    # Concatenate all yearly DataFrames if any exist, otherwise return an empty Series
    return pd.concat(dfs) if dfs else pd.Series(dtype=float)