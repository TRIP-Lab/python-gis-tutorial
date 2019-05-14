#!/usr/bin/env python3
from collections import OrderedDict
from datetime import datetime
import fiona
from fiona.crs import from_epsg
import json
import pytz


# Declare the local timezone for Montreal
tz = pytz.timezone('America/Montreal')


# Read in Google Locations .json data
json_data = json.load(open('../data/Location History.json'))
coordinates = json_data['locations']
print('Found {n} coordinates in Google Locations data...'.format(n=len(coordinates)))


# Quickly check keys that are available to us in the Google Locations data. It's
# best to refer to the documentation for something like this.
keys = set()
for c in coordinates:
    keys.update(set(c.keys()))
print('Google Locations keys: {k}'.format(k=keys))


# Create a GeoJSON schema for the data type we are representing. Fiona will
# use this as the common input format for exporting to shapefiles and other
# geodata. Since the location history is GPS coordinates, a collection of
# the type Point is appropriate.
geojson_data = {
    'type': 'FeatureCollection',
    'features': []
}


# Iterate over the loaded coordinates data and format each as a geojson
# object. Append the point object to the full feature collection.
for c in coordinates:
    # Google Location data is provided as an integer. Divide this by 10,000,000 to
    # represent the point as a decimal with 7 digit precision.
    latitude = c['latitudeE7'] / 1E7
    longitude = c['longitudeE7'] / 1E7

    # Python expects Unix time as integer seconds while provides milliseconds.
    ts = int(float(c['timestampMs']) / 1000)
    # Either work in UTC time (using .fromtimestamputc) or carefully explicitly
    # assign the timezone here.
    dt = datetime.fromtimestamp(ts, tz=tz)

    # Python shares objects in memory whenever possible. Simply copying the
    # object performs a "shallow" copy which may not be wanted for nested
    # objects. In those cases, Python offers deepcopy although note the
    # performance tradeoffs. Here we just initialize a new point in each pass to
    # avoid the issue.
    point = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [longitude, latitude]  # note the ordering is x, y (lon, lat).
        },
        # Use OrderedDict here to preserve the column ordering for the output shapefile.
        'properties': OrderedDict([
            # Use .isoformat() formats the datetime object to the ISO8601 string format.
            ('timestamp', dt.isoformat()),
            ('timestampMs', c['timestampMs']),
            ('accuracy', c['accuracy']),
            # Google Locations only returns properties when available depending on various
            # device decisions. Use .get() for the rest of the properties to handle when
            # the data is not availabe.
            ('altitude', c.get('altitude')),
            ('verticalAccuracy', c.get('verticalAccuracy')),
            ('velocity', c.get('velocity'))
        ])
    }
    # Append to the feature collection
    geojson_data['features'].append(point)


# At this stage, we can directly export the data as .geojson. This may be sufficient
# converting the data to work with QGIS.
with open('../data/location_history.geojson', 'w') as geojson_f:
    geojson_f.write(json.dumps(geojson_data))


# Otherwise for a shapefile, the columns must be declared and data written with fiona.
shp_schema = {
    'geometry': 'Point',
    'properties': {
        'timestamp': 'str',
        'timestampMs': 'int',
        'accuracy': 'int',
        'altitude': 'int',
        'verticalAccuracy': 'int',
        'velocity': 'int'
    }
}
with fiona.open('../data/location_history.shp', 'w',
                crs=from_epsg(4326),
                driver='ESRI Shapefile',
                schema=shp_schema) as shp_f:
    for feature in geojson_data['features']:
        shp_f.write(feature)

