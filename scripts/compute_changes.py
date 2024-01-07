import csv
import yfinance as yf
from tqdm import tqdm

from utils import generate_days_in_year, get_last_trading_day, get_same_day_years_ago, calculate_percent_change

# Reuse the closing prices
if 'closing_prices' not in locals():
    years = range(1993, 2024)
    spx = yf.Ticker("^SPX")
    closing_prices = spx.history(period="35y")['Close']

def compute_changes(file, interval=1):
    data = []

    total_days = 365 * len(years)
    progress_bar = tqdm(total=total_days, desc="Computing Changes")

    # Collect the percent changes for each day across the years
    for year in years:
        for day in generate_days_in_year(year):
            curr_date = get_last_trading_day(day).strftime("%Y-%m-%d")
            old_date = get_last_trading_day(get_same_day_years_ago(day, interval)).strftime("%Y-%m-%d")
            curr_price = closing_prices[curr_date]
            old_price = closing_prices[old_date]
            percent_change = calculate_percent_change(curr_price, old_price)
            data.append([day.strftime("%Y-%m-%d"), percent_change])
            progress_bar.update(1)
    
    progress_bar.close()

    # Write the data to a CSV file
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Percent Change'])
        writer.writerows(data)

def main():
    # compute_changes('data/spx_1_year_change.csv', 1)
    compute_changes('data/spx_2_year_change.csv', 2)
    # compute_changes('data/spx_5_year_change.csv', 5)

if __name__ == "__main__":
    main()