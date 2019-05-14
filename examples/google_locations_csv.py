#!/usr/bin/env python3
import csv
from datetime import datetime
import json
import pytz


tz = pytz.timezone('America/Montreal')


# Reads in Google Locations .json data
def read_csv():
    json_data = json.load(open('../data/Location History.json'))
    coordinates = json_data['locations']
    return coordinates


# Formats a Google Locations .json feature to a .csv row dict
def format_row(row):
    ts = int(float(row['timestampMs']) / 1000)
    dt = datetime.fromtimestamp(ts, tz=tz)
    latitude = row['latitudeE7'] / 1E7
    longitude = row['longitudeE7'] / 1E7
    csv_row = {
        'timestamp': dt.isoformat(),
        'timestampMs': row['timestampMs'],
        'accuracy': row['accuracy'],
        'verticalAccuracy': row.get('verticalAccuracy'),
        'altitude': row.get('altitude'),
        'velocity': row.get('velocity'),
        'latitude': latitude,
        'longitude': longitude
    }
    return csv_row


def main():
    coordinates = read_csv()

    headers = ['timestamp', 'timestampMs', 'accuracy', 'verticalAccuracy',
               'altitude', 'velocity', 'latitude', 'longitude']
    with open('../data/location_history.csv', 'w') as csv_f:
        writer = csv.DictWriter(csv_f, fieldnames=headers)
        writer.writeheader()

        for row in coordinates:
            csv_row = format_row(row)
            writer.writerow(csv_row)


if __name__ == '__main__':
    main()
