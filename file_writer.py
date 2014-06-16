# ==============================
# Disc Tracker File Writer
# by Stephanie Huang
# May 2014
# ==============================

import csv, os, boto
from boto.s3.key import Key

def readWrite(date, name, minutes):
    # fetch file from s3 using boto
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    conn = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket('disc-tracker-assets')
    k = Key(bucket)
    k.key = 'data.csv'
    k.get_contents_to_filename('data.csv')

    # actual reading/writing
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
#    os.rename('temp.csv.tmp','data.csv')