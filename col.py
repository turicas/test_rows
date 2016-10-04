#!/usr/bin/env python
# coding: utf-8

# This script imports data from the Catalogue of Life (www.catalogueoflife.org)
# webservice using the rows library.
#
# To see results in your terminal, run:
#    ./col.py species-name
# Example:
#    ./col Okapia
#
# To export results, run:
#    ./col.py species-name --output=filename.extension
# Where `extension` can be any format supported by rows, such as csv, xls,
# xlsx, html, among others.
# Example:
#     ./col.py Okapia --output=okapia.csv

import json

from io import BytesIO

import requests
import rows
import rows.utils


URL = 'http://www.catalogueoflife.org/col/webservice'


def search_species(name):
    'Search species and return a `rows.Table` with results'

    response = requests.get(URL, params={'name': name, 'format': 'json'})
    json_result = response.json()
    if 'error_message' in json_result and \
            json_result['error_message'].strip() != '':
        raise RuntimeError(json_result['error_message'])

    # Need to dump again to JSON (to get a `bytes` object) and then import as
    # JSON, since there is a little bug on rows
    json_rows = json.dumps(json_result['results'])
    return rows.import_from_json(BytesIO(json_rows))


if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument('species_name')
    parser.add_argument('--output')
    args = parser.parse_args()

    result = search_species(args.species_name)

    if args.output is None:
        print(rows.export_to_txt(result))
    else:
        rows.utils.export_to_uri(result, args.output)
