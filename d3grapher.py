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
import collections, os, boto, json
from bokeh.plotting import *
from bokeh.objects import *
from boto.s3.key import Key

def graph():
    ''' This method generates JSON data for d3.js graphing '''

    # # download file from s3 using boto
    # S3_BUCKET = 'disc-tracker-assets'

    # conn = boto.connect_s3()
    # bucket = conn.get_bucket(S3_BUCKET, validate=False)

    # k = Key(bucket)
    # k.key = 'data.csv'
    # k.get_contents_to_filename('data.csv')

    # use pandas to read csv file
    raw_data = pd.read_csv('data.csv', parse_dates=['date'])

    # spectral 5-class
    colors = ["#d7191c", "#fdae61", "#000000", "#abdda4", "#2b83ba", "#7a0177"]

    # groups
    group_1 = ['becca', 'nia', 'audrey', 'ava']
    group_2 = ['steph', 'jess', 'taylor', 'jordan', 'katja']
    group_3 = ['vso', 'zoe', 'erica', 'marguerite', 'robyn']
    group_4 = ['georgelle', 'priya', 'clarissa', 'lo', 'louisa']
    group_5 = ['sophie', 'stitties', 'adele', 'roz']
    alumni = ['melissa', 'rebecca', 'emma']

    groups = [group_1, group_2, group_3, group_4, group_5, alumni]

    group_header = ['date', 'group1', 'group2', 'group3', 'group4', 'group5', 'alumni']

    # new dataframe with group data
    zero_entries = pd.Series(np.zeros(len(raw_data.index)))

    group_data = pd.DataFrame({
        'date': raw_data['date'],
        'group1': zero_entries,
        'group2': zero_entries,
        'group3': zero_entries,
        'group4': zero_entries,
        'group5': zero_entries,
        'alumni': zero_entries })

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
        elif group == alumni:
            group_name = 'alumni'

        for member in group:
            group_data[group_name] += raw_data[member]

    group_data = group_data.sort(['date'])

    # create mapping for renaming indices
    dateIndex = { i : group_data['date'][i] for i in group_data.index.values }
    # print dateIndex # test
    
    # make dates indices
    group_data = group_data.rename(index=dateIndex)
    group_data.index.name = 'date'
    # remove duplicate column
    del group_data['date']

    # make custom json
    data_json = { col : [{group_data.index.name : str(i), "minutes" : group_data[col][i]} for i in group_data.index.values ] for col in group_data.columns.values }
    # print json.dumps(data_json) # test
    # print group_data.to_string() # test
    return json.dumps(data_json)
    # print group_data.to_json() # test

    # # BAR CHART OF TOTAL DISC TIME
    # bar_height = []
    # for group in group_header[1:]:
    #     bar_height.append(group_data[group].sum())

    # table = pd.DataFrame({'bar_height': bar_height}, index=group_header[1:])

    # figure(
    #     plot_width=800, 
    #     title="Total Disc Time by Group", 
    #     tools="hover,reset",
    #     x_range=group_header[1:],
    #     y_range=Range1d(start=0, end=max(bar_height)*1.1)
    # )

    # # create bars
    # rect(range(1,7), 
    #     [height/2 for height in table['bar_height']], 
    #     .8, 
    #     table['bar_height'],
    #     color=colors
    # )

    # xgrid().grid_line_color=None

    # hover = [t for t in curplot().tools if isinstance(t, HoverTool)][0]
    # hover.tooltips = collections.OrderedDict([
    #     ("group", "$x"),
    #     ("total time", "@height")
    # ])

    # show()

# graph()