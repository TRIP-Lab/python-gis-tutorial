Python GIS Tutorial
===================

## Plan
1. Parse Google Location .json to .geojson, .shp, .csv
2. Run Jupyter notebook and iterate through spatial format data performing geographic calculations
    - distance between points
    - buffer / intersect

#### Libraries
- fiona
- jupyter
- geopy
- pyproj
- pytz
- shapely

```bash
$ pip install geopy fiona jupyter pyproj pytz shapely
```

#### Key Concepts
- Python types: **string**, **int**, **float**, **list**, **tuple**, **dict**, **set**, **None**

## Examples

### Getting Started
1. Clone the tutorial's git repository to a local directory:
   ```
   $ git clone https://github.com/TRIP-Lab/python-gis-tutorial.git
   ```
   Alternatively: _"Clone or download"_ --> _"Download ZIP"_ from the top of this page
   
2. Copy your personal Google Locations .json export the the `./data` directory


### Google Location Data to Other Formats
- From .json to .geojson and .shp (steps commented): `./examples/google_locations_gis.py`
- From .json to .csv: `./examples/google_locations_csv.py`

### Basic Analysis in Jupyter
1. Open a terminal with to the project directory and start Jupyter
```bash
$ jupyter-notebook
```
2. Open the existing `Basic GIS Analysis.ipynb` notebook for a walkthrough of performing basic GIS functions
3. New notebooks can then be created to freely explore the data

## Good Practices
- Use `virtualenv` & `virtualenvwrapper` for managing Python projects. This helps sandbox the libraries used by each project so they do not interfere with each other. It also means any breaking changes changes are simple to undo by deleting the package directory and starting again.
    - `virtualenv` provides the sandbox, but can be a little verbose
    - `virtualenvwrapper` provides simple commands for creating, activating, and deleting virtual environments