# ==============================
# Main Disc Tracker App
# by Stephanie Huang
# May 2014
# Using Flask
# This product includes color specifications and designs developed 
# by Cynthia Brewer (http://colorbrewer.org/).
# ==============================

import numpy as np
import pandas as pd
from bokeh.plotting import *
from bokeh.objects import *


def graph():
    # use pandas to read csv file
    data = pd.read_csv('data.csv', parse_dates=['date'])
    data = data.sort(['date'])

    output_file("templates/graph.html", title="disc time graph")

    header = list(data.columns.values)

    # spectral, rdpu, pubu
    colors = [
        "#9e0142","#d53e4f","#f46d43","#fdae61","#fee08b","#ffffbf",
        "#e6f598","#abdda4","#66c2a5","#3288bd","#5e4fa2","#fff7f3","#fde0dd",
        "#fcc5c0","#fa9fb5","#f768a1","#dd3497","#ae017e","#7a0177","#49006a",
        "#fff7fb","#ece7f2","#d0d1e6","#a6bddb","#74a9cf","#3690c0","#0570b0",
        "#045a8d","#023858"
    ]

    # LINE CHART
    # place all lines on one graph
    hold()

    # drawing graph
    col_count = 0
    for value in header:
        if value == 'date':
            col_count += 1
            continue
        elif col_count == 1:
            line(
                data['date'], 
                data[value],
                color = colors[col_count-1],
                legend = value,
                x_axis_type = "datetime",
                tools = "pan,reset",
                plot_width=800
            )
        else:
            line(data['date'], data[value], color = colors[col_count-1], legend = value)
        col_count += 1

    # edit properties
    curplot().title = "NYPD Disc"
    grid().grid_line_alpha = 0

    yaxis().axis_label = "Disc Time (min)"

    # BAR CHART OF TOTAL DISC TIME
    # figure()

    # # create bars
    # col_count = 0
    # for value in header:
    #     if value == 'date':
    #         col_count += 1
    #         continue
    #     else:
    #         rect(

    #         )
    #     col_count += 1

    show()