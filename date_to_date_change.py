import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pandas_market_calendars import get_calendar

def generate_days(year):
    """
    Generate dates for each day in the specified year.

    Parameters:
    - year (int): The year for which to generate dates.

    Yields:
    - datetime: A datetime object representing each day in the specified year.
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

def get_same_day(date, years_ago=1):
    """
    Get the corresponding day in the previous year, considering leap years.

    Parameters:
    - date (datetime): The date for which to get the corresponding day.
    - years_ago (int): The number of years ago to get the corresponding day.

    Returns:
    - datetime: A datetime object representing the corresponding day in the previous year.
    """
    return date - relativedelta(years=years_ago)

def is_trading_day(date):
    """
    Check if a given date is a U.S. stock market trading day.

    Parameters:
    - date (datetime): The date to check.

    Returns:
    - bool: True if the date is a trading day, False otherwise.
    """
    # XNYS is the code for the New York Stock Exchange calendar
    nyse = get_calendar("XNYS")
    return nyse.valid_days(start_date=date, end_date=date).size > 0

def get_last_trading_day(date):
    """
    Get the last trading day before the specified date.

    Parameters:
    - date (datetime): The date for which to get the last trading day.

    Returns:
    - datetime: A datetime object representing the last trading day before the specified date.
    """
    if is_trading_day(date):
        return date
    else:
        return get_last_trading_day(date - timedelta(days=1))

def calculate_percent_change(new_price, old_price):
    """
    Calculate the percent change between two prices.
    
    Parameters:
    - new_price (float): The new price.
    - old_price (float): The old price.

    Returns:
    - float: The percent change between the two prices.
    """
    return (new_price - old_price) / old_price * 100

def main():
    spx = yf.Ticker("^SPX")
    closing_prices = spx.history(period="25y")['Close']
    years = range(2022, 2024)
    plt.figure(figsize=(12, 6))
    
    for year in years:
        dates = []
        changes = []
        for day in generate_days(year):
            curr_date = get_last_trading_day(day).strftime("%Y-%m-%d")
            old_date = get_last_trading_day(get_same_day(day)).strftime("%Y-%m-%d")
            curr_price = closing_prices[curr_date]
            old_price = closing_prices[old_date]
            percent_change = calculate_percent_change(curr_price, old_price)
            dates.append(day.strftime('%Y-%m-%d'))
            changes.append(percent_change)

        plt.plot(dates, changes, label=f'{year}-{year+1}')

    plt.xlabel('Date')
    plt.xticks([])
    plt.ylabel('Percent Change')
    plt.title('S&P 500 1-Year Change for 2022-2023')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
