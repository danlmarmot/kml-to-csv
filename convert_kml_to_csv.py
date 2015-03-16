#!/usr/bin/env python3
__author__ = 'danlmarmot'

"""
    Parses a KML into CSV

    Written for Python 3.4 or greater
    Designed to be used with Garmin POI Loader and custom POI icons
    Read up at icon requirements at http://www8.garmin.com/products/poiloader/creating_custom_poi_files.jsp

    CSV output is Longitude, Latitude, Name, Comment
"""

import argparse
import os
import lxml
from pandas import DataFrame
from csv import QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONNUMERIC
from shutil import copyfile

from bs4 import BeautifulSoup

OUTPUT_DIR = "output"
CSV_OUTPUT_ORDER = ['longitude', 'latitude', 'name', 'comment']


def main():
    args = parse_args()
    rows, styles = parse_kml(args.input_file)

    df = DataFrame(rows)
    print(str(df['name'].count()) + " waypoints loaded")
    print("Counts by style:")
    print(df['style'].value_counts())

    # convert lat/long strings to floats
    df[['longitude', 'latitude']] = df[['longitude', 'latitude']].astype(float)

    for s in styles:
        style_output_dir = os.path.join(OUTPUT_DIR, s)
        os.makedirs(style_output_dir, exist_ok=True)
        output_file = os.path.join(OUTPUT_DIR, s, s + ".csv")
        odf = df[df['style'] == s]
        odf.to_csv(output_file,
                   quotechar='"',
                   quoting=QUOTE_NONNUMERIC,
                   columns=CSV_OUTPUT_ORDER,
                   header=False,
                   index=False)

        # Copy bmp icon if present
        style_bmp = os.path.join('bmp', s + '.bmp')
        if os.path.exists(style_bmp):
            copyfile(style_bmp, os.path.join(style_output_dir, s + '.bmp'))


def parse_kml(input_file):
    h = open(input_file).read()
    soup = BeautifulSoup(h)

    rows = []
    styles = set([])
    for item in soup.findAll('placemark'):
        point = {}

        for c in item.findAll('coordinates'):
            coord = c.find(text=True)
            point['longitude'] = coord.split(',')[0]
            point['latitude'] = coord.split(',')[1]

        for name in item.findAll('name'):
            point['name'] = name.find(text=True)

        for comment in item.findAll('description'):
            point['comment'] = comment.find(text=True)

        for style in item.findAll('styleurl'):
            raw_style = style.find(text=True)
            style = raw_style.lstrip('#').rstrip('1234567890')
            point['style'] = style
            if style not in styles:
                print("Found " + style)
                styles.add(style)

        rows.append(point)

    return rows, styles


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        dest='input_file',
                        default='input_waypoints.kml',
                        action="store")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    main()
