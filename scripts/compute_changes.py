import csv
import yfinance as yf
from tqdm import tqdm

from utils import years, generate_days_in_year, get_last_trading_day, get_same_day_years_ago, calculate_percent_change

# Reuse the closing prices
if 'closing_prices' not in locals():
    spx = yf.Ticker("^SPX")
    closing_prices = spx.history(period="35y")['Close']

def compute_changes(file, interval=1):
    data = []

    total_days = 365 * len(years)
    progress_bar = tqdm(total=total_days, desc="Computing Changes")

    # Collect the percent changes for each day across the years
    for year in years:
        for curr_date in generate_days_in_year(year):
            curr_date_adjusted = get_last_trading_day(curr_date).strftime("%Y-%m-%d")
            base_date = get_same_day_years_ago(curr_date, interval)
            base_date_adjusted = get_last_trading_day(base_date).strftime("%Y-%m-%d")
            curr_price = closing_prices[curr_date_adjusted]
            base_price = closing_prices[base_date_adjusted]
            percent_change = calculate_percent_change(curr_price, base_price)
            data.append([curr_date.strftime("%Y-%m-%d"), base_date, curr_price, base_price, percent_change])
            progress_bar.update(1)
    
    progress_bar.close()

    # Write the data to a CSV file
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Current_Date', 'Base_Date', 'Current_Price', 'Base_Price', 'Percent Change'])
        writer.writerows(data)

def main():
    compute_changes('data/spx_1_year.csv', 1)
    compute_changes('data/spx_2_year.csv', 2)
    compute_changes('data/spx_5_year.csv', 5)

if __name__ == "__main__":
    main()