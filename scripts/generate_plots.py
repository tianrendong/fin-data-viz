import csv
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool
from tqdm import tqdm

from utils import years, generate_days_in_year

dates = []
for day in generate_days_in_year(2022):
    dates.append(day.strftime("%m-%d"))

def generate_plots(data_file, plot_title, html_file):
    """
    Generate an interactive plot with hover.

    Parameters:
    - data_file (str): The path to the CSV file.
    - plot_title (str): The title of the plot.
    - html_file (str): The path to the output html.

    Returns:
    - None
    """
    output_file(html_file)
    p = figure(x_range=dates, title=plot_title, y_axis_label="Percent Change", toolbar_location=None, tools="", width=1200, height=600)
    
    total_days = 365 * len(years)
    progress_bar = tqdm(total=total_days, desc="Reading Data")

    with open(data_file, 'r') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader)

        # i is the index into the years list
        # day keeps track of the number days in a year processed
        # changes is a list of percent changes for each day in a year
        i, day, changes = 0, 0, []
        for row in reader:
            day += 1
            
            if day == 366:
                p.vbar(x=dates, top=changes, line_width=0.9, fill_alpha=0.1, line_color=None)
                day = 0
                changes = []
                i += 1
                
            changes.append(float(row[4]))
            progress_bar.update(1) 

        progress_bar.close() 

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
    generate_plots("data/spx_1_year.csv", "S&P 500 1 Year Same Date Change for 1993-2023", "plots/spx_1_year_change.html")
    generate_plots("data/spx_2_year.csv", "S&P 500 2 Year Same Date Change for 1993-2023", "plots/spx_2_year_change.html")
    generate_plots("data/spx_5_year.csv", "S&P 500 5 Year Same Date Change for 1993-2023", "plots/spx_5_year_change.html")

if __name__ == "__main__":
    main()