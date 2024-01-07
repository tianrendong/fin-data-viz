import csv
import pandas as pd
import yfinance as yf
from tqdm import tqdm

from utils import years, generate_days_in_year, get_same_day_years_ago, calculate_percent_change

def compute_changes(input_file, output_file, interval=1):
    prices_df = pd.read_csv(input_file)

    dfs = []
    dfs.append(pd.DataFrame({'Year': years}))

    for day in tqdm(generate_days_in_year(2023), desc="Processing days"):
        data = []
        for year in years:
            curr_date = day.replace(year=year)
            base_date = get_same_day_years_ago(curr_date, interval)
            curr_price = prices_df.loc[prices_df['Year'] == year, curr_date.strftime("%m-%d")].values[0]
            base_price = prices_df.loc[prices_df['Year'] == year - interval, base_date.strftime("%m-%d")].values[0]
            percent_change = calculate_percent_change(curr_price, base_price)
            data.append(percent_change)
        dfs.append(pd.DataFrame({day.strftime("%m-%d"): data}))
    
    result_df = pd.concat(dfs, axis=1)
    result_df.to_csv(output_file)

def main():
    input_file = 'data/spx_closing_prices.csv'
    compute_changes(input_file, 'data/spx_1_year_changes.csv', 1)
    compute_changes(input_file, 'data/spx_2_year_changes.csv', 2)
    compute_changes(input_file, 'data/spx_5_year_changes.csv', 5)

if __name__ == "__main__":
    main()