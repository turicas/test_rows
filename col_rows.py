# This script imports data from the Catalogue of Life (www.catalogueoflife.org) webservice
# using the rows library.

import urllib # using the standard urllib
#import requests
import json
import csv
import rows
#from collections import OrderedDict
from io import BytesIO

# standard fields in the CoL response; they should be automatically detected by rows
#col_fields = OrderedDict([('id', rows.fields.IntegerField),
#                         ('name', rows.fields.TextField),
#                         ('rank', rows.fields.TextField),
#                         ('name_status', rows.fields.TextField),
#                         ('name_html', rows.fields.TextField),
#                         ('url', rows.fields.TextField),
#                         ('is_extinct', rows.fields.TextField),
#                         ('online_resource', rows.fields.TextField),
#                         ('source_database', rows.fields.TextField),
#                         ('source_database_url', rows.fields.TextField),
#                        ])

# get data for target species (in this case, the okapi)
species = "Okapia johnstoni"
url = "http://www.catalogueoflife.org/col/webservice?name=" + urllib.quote_plus(species) + "&format=json&response=terse"
json_data = urllib.urlopen(url).read()

# the lines below do not work; a KeyError arises.
#json_data = requests.get(url).content  # Download JSON data
#print json_data
#row_data = rows.import_from_json(BytesIO(json_data))  # already imported!
#print row_data

# parse data using json
json_parsed = json.loads(json_data)
data = json_parsed['results']

# open a csv file for writing
col_data = open('ColData.csv', 'w')

# create the csv writer object
csvwriter = csv.writer(col_data)

# write json parsed data to csv 
count = 0
for record in data:
    if count == 0:
        header = record.keys() # header row
        csvwriter.writerow(header)
    count += 1
    csvwriter.writerow(record.values())
col_data.close()

# open csv fil for reading
infile = open('ColData.csv', 'r')

# parse csv file with rows
row_data = rows.import_from_csv(infile)
print row_data