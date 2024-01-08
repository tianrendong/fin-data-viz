import os
import math
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from tqdm import tqdm

def plot_indexed_annuity_values(data_dir, plot_title, html_file):
    """
    Plot the final values of the indexed annuity calculations.

    Parameters:
    - data_dir (str): The path to the directory containing data.
    - plot_title (str): The title of the plot.
    - html_file (str): The path to the output html.

    Returns:
    - None
    """
    values = []
    for filename in os.listdir(data_dir):
        file_path = os.path.join(data_dir, filename)
        if os.path.isfile(file_path):
            values_df = pd.read_csv(file_path)
            values += values_df.iloc[-1, 2:].values.tolist()

    min_val, max_val = math.floor(min(values)), math.ceil(max(values))
    num_bins = 10
    step = (max_val - min_val) / num_bins
    bins = [min_val + i * step for i in range(num_bins+1)]
    labels = [str(math.floor(bins[i])) + "-" + str(math.floor(bins[i + 1])) for i in range(num_bins)]
    categories = pd.cut(values, bins, labels=labels)
    value_counts = categories.value_counts().sort_index()
    value_ranges, counts = value_counts.index.tolist(), value_counts.values.tolist()

    output_file(html_file)
    p = figure(x_range=value_ranges, title=plot_title, y_axis_label="Number of Days", toolbar_location=None, tools="", width=1200, height=600)
    p.vbar(x=value_ranges, top=counts, line_width=0.9, line_color=None)

    # Show detail value when hovering
    hover = HoverTool()
    hover.tooltips = [("Value", "@x"), ("Number of Days", "@top")]
    p.add_tools(hover)

    p.xaxis.axis_label = "Final Value"
    p.grid.grid_line_color = None

    show(p)

def main():
    # plot_indexed_annuity_values("data/indexed_annuity/1_year/", "20 Year Period Indexed Annuity Values based on SPX With 1 Year Interval", "web/plots/indexed_annuity/1_year_values.html")
    # plot_indexed_annuity_values("data/indexed_annuity/2_year/", "20 Year Period Indexed Annuity Values based on SPX with 2 Year Interval", "web/plots/indexed_annuity/2_year_values.html")
    # plot_indexed_annuity_values("data/indexed_annuity/5_year/", "20 Year Period Indexed Annuity Values based on SPX with 5 Year Interval", "web/plots/indexed_annuity/5_year_values.html")
    plot_indexed_annuity_values("data/indexed_annuity/monthly/", "20 Year Period Indexed Annuity Values based on SPX with Monthly Interval", "web/plots/indexed_annuity/monthly_values.html")

if __name__ == "__main__":
    main()