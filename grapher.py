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
import collections
import os
from bokeh.plotting import *
from bokeh.objects import *

def graph():
    # use pandas to read csv file
    raw_data = pd.read_csv('data.csv', parse_dates=['date'])

    os.remove('templates/graph.html')
    output_file("templates/graph.html", title="disc time graph")

    # spectral 5-class
    colors = ["#d7191c", "#fdae61", "#000000", "#abdda4", "#2b83ba"]

    # groups
    group_1 = ['becca', 'nia', 'audrey', 'ava']
    group_2 = ['steph', 'jess', 'taylor', 'jordan', 'katja']
    group_3 = ['vso', 'zoe', 'erica', 'marguerite']
    group_4 = ['georgelle', 'priya', 'clarissa', 'lo', 'louisa']
    group_5 = ['sophie', 'stitties', 'adele', 'roz']

    groups = [group_1, group_2, group_3, group_4, group_5]

    group_header = ['date', 'group1', 'group2', 'group3', 'group4', 'group5']

    # new dataframe with group data
    zero_entries = pd.Series(np.zeros(len(raw_data.index)))

    group_data = pd.DataFrame({
        'date': raw_data['date'],
        'group1': zero_entries,
        'group2': zero_entries,
        'group3': zero_entries,
        'group4': zero_entries,
        'group5': zero_entries })

    for group in groups:
        if group == group_1:
            group_name = 'group1'
        elif group == group_2:
            group_name = 'group2'
        elif group == group_3:
            group_name = 'group3'
        elif group == group_4:
            group_name = 'group4'
        elif group == group_5:
            group_name = 'group5'

        for member in group:
            group_data[group_name] += raw_data[member]

    group_data = group_data.sort(['date'])

    # LINE CHART
    # place all lines on one graph
    hold()

    # drawing graph
    col_count = 0
    for value in group_header:
        if value == 'date':
            col_count += 1
            continue
        elif col_count == 1:
            line(
                group_data['date'], 
                group_data[value],
                color = colors[col_count-1],
                legend = value,
                x_axis_type = "datetime",
                tools = "pan,reset",
                plot_width=800
            )
        else:
            line(
                group_data['date'], 
                group_data[value], 
                color = colors[col_count-1], 
                legend = value
            )
        col_count += 1

    # edit properties
    curplot().title = "NYPD Disc Tracker"
    grid().grid_line_alpha = 0

    yaxis().axis_label = "Disc Time (min)"

    # BAR CHART OF TOTAL DISC TIME
    bar_height = []
    for group in group_header[1:]:
        bar_height.append(group_data[group].sum())

    table = pd.DataFrame({'bar_height': bar_height}, index=group_header[1:])

    figure(
        plot_width=800, 
        title="Total Disc Time by Group", 
        tools="hover,reset",
        x_range=group_header[1:],
        y_range=Range1d(start=0, end=max(bar_height)*1.1)
    )

    # create bars
    rect(range(1,6), 
        [height/2 for height in table['bar_height']], 
        .8, 
        table['bar_height'],
        color=colors
    )

    hover = [t for t in curplot().tools if isinstance(t, HoverTool)][0]
    hover.tooltips = collections.OrderedDict([
        ("group", "$x"),
        ("total time", "@height")
    ])

    show()