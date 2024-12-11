"""
upstream.py
Function for fetching data from the JAO API for use in the data pipeline.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from calendar import monthrange
import os

def fetch_auction_data(start_year, end_year, api_key, corridor, output_dir="../data/external"):
    """
    Fetch auction data from the JAO API for a range of years and save it to CSV.
    
    Parameters:
    - start_year: int, the starting year for the data.
    - end_year: int, the ending year for the data.
    - api_key: str, the API key for authentication.
    - output_dir: str, directory where the result CSV will be saved (default is 'data/external').
    
    Returns:
    - DataFrame: the combined DataFrame of all auction data.
    """
    
    Base_URL = "https://api.jao.eu/OWSMP/getauctions?"
    headers = {"AUTH_API_KEY": api_key}
    
    dfs = []

    # Loop through each year and month
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            # First and last day of the month
            first_day = (datetime(year, month, 1) - timedelta(days=1)).strftime("%Y-%m-%d")
            last_day = datetime(year, month, monthrange(year, month)[1]).strftime("%Y-%m-%d")

            params = {
                "horizon": "Daily",
                "corridor": corridor,
                "fromdate": first_day,
                "todate": last_day,
            }

            # Fetch data from the API
            response = requests.get(Base_URL, headers=headers, params=params)
            response.raise_for_status()  # Raise an error for bad HTTP responses
            data = response.json()

            # Convert the JSON data into DataFrame
            df = pd.DataFrame.from_dict(data)
            df["new"] = pd.to_datetime(df["marketPeriodStart"]).dt.strftime("%d/%m/%Y")
            df = df.sort_values(by="new", ascending=True).reset_index(drop=True)

            last_day = len(df)

            # Extract relevant data for each day
            for i_day in range(last_day):
                data_items = df["results"][i_day]
                date = datetime.fromisoformat(df["marketPeriodStart"][i_day]) + timedelta(days=1)
                
                extracted_data = [
                    {
                        "date": date.date(),
                        "productHour": item["productHour"],
                        f"{corridor}_auctionPrice": item["auctionPrice"],
                        f"{corridor}_requestedCapacity": item["requestedCapacity"],                        
                        f"{corridor}_offeredCapacity": item["offeredCapacity"],
                    }
                    for item in data_items
                ]
                
                ddf = pd.DataFrame(extracted_data)
                ddf = ddf.sort_values(by="productHour", ascending=True)
                dfs.append(ddf)
    
    # Combine all DataFrames into one
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the combined DataFrame to a CSV file
    output_file = os.path.join(output_dir, f"jao_{corridor}.csv")
    combined_df.to_csv(output_file, index=False)
    
    return combined_df
