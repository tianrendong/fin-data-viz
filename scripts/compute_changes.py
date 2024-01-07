import csv
import pandas as pd
import yfinance as yf
from tqdm import tqdm

from utils import years, generate_days_in_year, get_last_trading_day, get_same_day_years_ago, calculate_percent_change

def compute_changes(input_file, output_file, interval=1):
    data = []

    total_days = 365 * len(years)
    progress_bar = tqdm(total=total_days, desc="Computing Changes")

    prices_df = pd.read_csv(input_file)

    # Collect the percent changes for each day across the years
    for year in years:
        for curr_date in generate_days_in_year(year):
            base_date = get_same_day_years_ago(curr_date, interval)
            curr_price = prices_df.loc[prices_df['Year'] == year, curr_date.strftime("%m-%d")].values[0]
            base_price = prices_df.loc[prices_df['Year'] == year - interval, base_date.strftime("%m-%d")].values[0]
            percent_change = calculate_percent_change(curr_price, base_price)
            data.append([curr_date.strftime("%Y-%m-%d"), base_date, curr_price, base_price, percent_change])
            progress_bar.update(1)
    
    progress_bar.close()

    # Write the data to a CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Current_Date', 'Base_Date', 'Current_Price', 'Base_Price', 'Percent Change'])
        writer.writerows(data)

def main():
    input_file = 'data/spx_closing_prices.csv'
    compute_changes(input_file, 'data/spx_1_year.csv', 1)
    compute_changes(input_file, 'data/spx_2_year.csv', 2)
    compute_changes(input_file, 'data/spx_5_year.csv', 5)

if __name__ == "__main__":
    main()