import pandas as pd
from tqdm import tqdm

from utils import generate_days_in_year

def calculate_indexed_annuity_values(start_year, input_file, output_file, interval=1, capped=True):
    growth_years = list(range(start_year, start_year + 21))
    growth_years_adjusted = []
    for i in range(0, len(growth_years), interval):
        growth_years_adjusted.append(growth_years[i])

    changes_df = pd.read_csv(input_file)

    dfs = []
    dfs.append(pd.DataFrame({'Year': growth_years_adjusted}))

    for day in tqdm(generate_days_in_year(2003), desc="Processing days"):
        value = 125000
        values = []
        for year in growth_years_adjusted:
            curr_date = day.replace(year=year)
            curr_change = changes_df.loc[changes_df['Year'] == year, curr_date.strftime("%m-%d")].values[0]
            if capped:
                if curr_change >= 6.25:
                    value *= (1 + (0.0625 * 2.5))
                elif curr_change > 0:
                    value *= (1 + (curr_change/100 * 2.5))
            else:
                value *= (1 + (curr_change/100 * 2.5))
            values.append(value)
        dfs.append(pd.DataFrame({day.strftime("%m-%d"): values}))

    result_df = pd.concat(dfs, axis=1)
    result_df.to_csv(output_file)

def main():
    # input_file = 'data/spx_1_year_changes.csv'
    # calculate_indexed_annuity_values(input_file, f'data/indexed_annuity/spx_1_year_growths_{start_year}_start.csv')
    # input_file = 'data/spx_2_year_changes.csv'
    # calculate_indexed_annuity_values(input_file, f'data/indexed_annuity/spx_2_year_growths_{start_year}_start.csv', 2)
    # input_file = 'data/spx_5_year_changes.csv'
    # calculate_indexed_annuity_values(input_file, f'data/indexed_annuity/spx_5_year_growths_{start_year}_start.csv', 5)
    input_file = 'data/spx_monthly_changes.csv'
    for start_year in range(1998, 2004):
        calculate_indexed_annuity_values(start_year, input_file, f'data/indexed_annuity/monthly/spx_monthly_growths_{start_year}_start.csv', 1, False)

if __name__ == "__main__":
    main()