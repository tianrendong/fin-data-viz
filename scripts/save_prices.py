import yfinance as yf
import pandas as pd
from tqdm import tqdm

from utils import prices_years, generate_days_in_year, get_last_trading_day

def save_prices(ticker, file, period="40y"):
    # Get the closing prices from Yahoo Finance
    sec = yf.Ticker(ticker)
    closing_prices = sec.history(period=period)['Close']

    # Create a dataframe where the columns are the days in a year and the rows are the years
    # Each cell contains the closing price for that day in that year
    dfs = []
    dfs.append(pd.DataFrame({'Year': prices_years}))

    for day in tqdm(generate_days_in_year(2023), desc="Processing days"):
        prices = []
        for year in prices_years:
            date = day.replace(year=year)
            date_adjusted = get_last_trading_day(date).strftime("%Y-%m-%d")
            prices.append(closing_prices[date_adjusted])

        dfs.append(pd.DataFrame({day.strftime("%m-%d"): prices}))

    result_df = pd.concat(dfs, axis=1)
    result_df.to_csv(file)

def main():
    save_prices("^SPX", "data/spx_closing_prices.csv")

if __name__ == "__main__":
    main()
