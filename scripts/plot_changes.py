import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from tqdm import tqdm

from utils import years, generate_days_in_year

dates = []
for day in generate_days_in_year(2022):
    dates.append(day.strftime("%m-%d"))

def plot_changes(data_file, plot_title, html_file):
    """
    Plot the changes of SPX for each day.

    Parameters:
    - data_file (str): The path to the CSV file.
    - plot_title (str): The title of the plot.
    - html_file (str): The path to the output html.

    Returns:
    - None
    """
    output_file(html_file)
    p = figure(x_range=dates, title=plot_title, y_axis_label="Percent Change", toolbar_location=None, tools="", width=1200, height=600)

    prices_df = pd.read_csv(data_file)
    for year in tqdm(years, desc="Processing years"):
        changes = []
        for day in generate_days_in_year(2023):
            changes.append(prices_df.loc[prices_df['Year'] == year, day.strftime("%m-%d")].values[0])
        p.vbar(x=dates, top=changes, line_width=0.9, fill_alpha=0.1, line_color=None)

    # Show detail value when hovering
    hover = HoverTool()
    hover.tooltips = [("Date", "@x"), ("Percent Change", "@top")]
    p.add_tools(hover)

    p.xaxis.axis_label = "Day of Year"
    p.xaxis.major_label_text_color = None
    p.xaxis.major_tick_line_color = None
    p.xaxis.minor_tick_line_color = None
    p.grid.grid_line_color = None

    show(p)

def main():
    # plot_changes("data/spx_1_year_changes.csv", "S&P 500 1 Year Same Date Change for 1993-2023", "web/plots/spx_1_year_change.html")
    # plot_changes("data/spx_2_year_changes.csv", "S&P 500 2 Year Same Date Change for 1993-2023", "web/plots/spx_2_year_change.html")
    # plot_changes("data/spx_5_year_changes.csv", "S&P 500 5 Year Same Date Change for 1993-2023", "web/plots/spx_5_year_change.html")
    plot_changes("data/spx_monthly_changes.csv", "S&P 500 Monthly Same Date Change for 1993-2023", "web/plots/spx_monthly_change.html")

if __name__ == "__main__":
    main()