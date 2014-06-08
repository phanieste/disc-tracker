# ==============================
# Disc Tracker File Writer
# by Stephanie Huang
# May 2014
# ==============================

import csv
import os

def readWrite(date, name, minutes):
    infile = open('data.csv', 'rb')
    outfile = open('temp.csv.tmp', 'wb')
    newName = False
    
    tsvreader = csv.DictReader(infile)

    header = tsvreader.fieldnames
    if name in header:
        pass
    else:
        header.append(name)
        newName = True
    
    tsvwriter = csv.DictWriter(outfile, header)

    tsvwriter.writeheader()

    dateFound = False
    for row in tsvreader:
        if newName:
            row[name] = 0
        if row['date'] == date:
            dateFound = True
            row[name] = minutes
        tsvwriter.writerow(row)

    if not dateFound:
        row = {}
        for field in header:
            if field == 'date':
                row[field] = date
            elif field == name:
                row[field] = minutes
            else:
                row[field] = 0
        tsvwriter.writerow(row)

    infile.close()
    outfile.close()
    os.remove('data.csv')
    os.rename('temp.csv.tmp','data.csv')