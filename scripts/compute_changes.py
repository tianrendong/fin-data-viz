import pandas as pd
from tqdm import tqdm

from utils import years, generate_days_in_year, get_same_day_years_ago, get_same_day_last_month, calculate_percent_change

def compute_changes_yearly(input_file, output_file, interval=1):
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

def compute_changes_monthly(input_file, output_file):
    prices_df = pd.read_csv(input_file)

    dfs = []
    dfs.append(pd.DataFrame({'Year': years}))

    for day in tqdm(generate_days_in_year(2023), desc="Processing days"):
        data = []
        for year in years:
            changes = []
            curr_date = day.replace(year=year)
            base_date = curr_date

            for _ in range(12):
                curr_date = base_date
                base_date = get_same_day_last_month(curr_date)
                # Adjust 2/29 in leap years to 2/28 because price data does not have 2/29
                if base_date.month == 2 and base_date.day == 29:
                    base_date = base_date.replace(day=28)

                curr_price = prices_df.loc[prices_df['Year'] == year, curr_date.strftime("%m-%d")].values[0]
                base_price = prices_df.loc[prices_df['Year'] == base_date.year, base_date.strftime("%m-%d")].values[0]
                percent_change = calculate_percent_change(curr_price, base_price)
                changes.append(percent_change)

            capped_changes = list(map(lambda x: min(x, 1.6), changes))
            data.append(sum(capped_changes))
        dfs.append(pd.DataFrame({day.strftime("%m-%d"): data}))
    
    result_df = pd.concat(dfs, axis=1)
    result_df.to_csv(output_file)

def main():
    # input_file = 'data/spx_closing_prices.csv'
    # compute_changes_yearly(input_file, 'data/spx_1_year_changes.csv', 1)
    # compute_changes_yearly(input_file, 'data/spx_2_year_changes.csv', 2)
    # compute_changes_yearly(input_file, 'data/spx_5_year_changes.csv', 5)
    # compute_changes_monthly(input_file, 'data/spx_monthly_changes.csv')
    input_file = 'data/qqq_closing_prices.csv'
    compute_changes_yearly(input_file, 'data/qqq_1_year_changes.csv', 1)
    input_file = 'data/spy_closing_prices.csv'
    compute_changes_yearly(input_file, 'data/spy_1_year_changes.csv', 1)

if __name__ == "__main__":
    main()