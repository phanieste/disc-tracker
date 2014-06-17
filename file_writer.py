# ==============================
# Disc Tracker File Writer
# by Stephanie Huang
# May 2014
# ==============================

import csv, os, boto
from boto.s3.key import Key

def readWrite(date, name, minutes):
    # fetch file from s3 using botoK
    S3_BUCKET = 'disc-tracker-assets'

    conn = boto.connect_s3()
    bucket = conn.get_bucket(S3_BUCKET, validate=False)
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