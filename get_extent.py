import fiona
from fiona import errors
import rasterio
from rasterio import RasterioIOError
import os
import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas import GeoDataFrame
import shapely
from shapely.geometry import Point
import sys
import matplotlib
import matplotlib.cbook
import re


shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
CA_rast = "/Users/datateam/repos/spatial-introspect/NE1_50M_SR_W_tenth_CA.tif"
csv_ex = "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv"
NM_rast = "/Users/datateam/Desktop/test_data/soil_color_NM/NM_125cm.tif"

def get_extent_for_vector(shapefile):
    lats = []
    lons = []
    with fiona.open(shapefile, 'r') as src:
        for feat in src:
            coords = feat['geometry']['coordinates'][0] # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
            [(lons.append(x), lats.append(y)) for x, y in coords]

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    print('South extent: {}\nNorth extent: {}\nWest extent: {}\nEast extent: {}'.format(min_lat,
                                                                                        max_lat,
                                                                                        min_lon,
                                                                                        max_lon))
get_extent_for_vector(shp_fn)

# Need to convert when using files like NM_raster that are in meters
'''rightm but that's probably what you're going to want. if you want to find it's bounds in geographic coordinates you need to 
'reproject' the coordinates you have, or reproject the entire raster. 
rasterio will reproject the raster, if you want to do that programmatically. 
or you can use `pyproj` to convert the coordinates directly'''
def get_extent_for_raster(raster):
    with rasterio.open(raster, 'r') as ds:
        print(ds.bounds)
        print(ds.meta) #gets more info about the raster



#documentation: http://geopandas.org/gallery/create_geopandas_from_pandas.html#sphx-glr-gallery-create-geopandas-from-pandas-py

#Needs to be applied more broadly, find some way not to just use "Long" "Lat"
def get_extent_csv(filepath):
    df = pd.read_csv(filepath)
    df['coordinates'] = list(zip(df.Long, df.Lat))
    df['coordinates'] = df['coordinates'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='coordinates')
    bnds = gdf.total_bounds
    print(bnds)

get_extent_csv(csv_ex)


class MissingLongitude(Exception):
    pass

class MissingLatitude(Exception):
    pass

def get_lon(csv_file):
    df = pd.read_csv(csv_file)
    cols = df.columns
    if "lon" in cols:
        lon_ix = cols.index('lon')
        print(lon_ix)
    elif "x" in cols:
        lon_ix = cols.index('x')
    else:
        raise MissingLongitude('This csv appears to be missing a longitude field')

get_lon(csv_ex)


def get_lat(csv_file):
    df = pd.read_csv(csv_file)
    cols = df.columns
    if "lat" in cols:
        lon_ix = cols.index('lon')
    elif "y" in cols:
        lon_ix = cols.index('x')
    else:
        raise MissingLatitude('This csv appears to be missing a latitude field')





'''
#Bonus Points!
def get_extent_for_csv(file_path, long_col_name=None, lat_col_name=None):
    """
    potential example with geopandas: https://gist.github.com/nygeog/2731427a74ed66ca0e420eaa7bcd0d2b
    
    # outline
    
    1. figure out column names if they're not provided 
    2. convert to point geodataframe (geopandas)
    """
    if long_col_name is None:
        # do stuff to figure out the long_col_name
        pass
'''


# How to make exception for csv?

def get_extent(file_path):
    try:
        extent = get_extent_for_vector(file_path)
    except errors.FionaValueError:
        extent = get_extent_for_raster(file_path)

    return extent


# # # CSV # # #

# Check lat lon in column names functions

# to do: Something will need to be done about

sampling_sites = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.5.5"
csv_no_geo = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.10.2"
other = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.11.6"

def the_actual_whole_function(csv):
    csv_df = pd.read_csv(csv)
    class MyException(Exception):
        pass

    def generic_check_for_cols(csv_df, col_string):
        results = []
        pat = re.compile(col_string, flags=re.IGNORECASE)
        for col_name in csv_df.columns:
            if pat.match(col_name) is not None:
                results.append(col_name)
        if len(results) != 1:
            raise MyException
        return results

    def check_lat(csv_df):
        return generic_check_for_cols(csv_df, "lat")

    def check_lon(csv_df):
        return generic_check_for_cols(csv_df, "lon")

    try:
        lat_name = check_lat(csv_df)
    except MyException:
        raise MyException('Latitude cannot be guessed.')
    try:
        lon_name = check_lon(csv_df)
    except MyException:
        raise MyException('Longitude cannot be guessed.')

    csv_df['geometry'] = csv_df.apply(lambda r: Point(r[lon_name], r[lat_name]), axis=1)
    pnt_gdf = gpd.GeoDataFrame(csv_df)

    return pnt_gdf.total_bounds

the_actual_whole_function(sampling_sites)
the_actual_whole_function(csv_no_geo)
# this has text that has lat in it
the_actual_whole_function(other)
# doesn't have lat or lon it but I'm not sure if it's calling the exception correctly or not

# this is the old version, I think it works the same
try:
    lat_name = check_lat(csv_df)
    lon_name = check_lon(csv_df)
except MyException:
    raise MyException('Latitude or longitude cannot be guessed.')
