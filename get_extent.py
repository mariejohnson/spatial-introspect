import fiona
from fiona import errors
import rasterio
from rasterio import RasterioIOError
from rasterio import features
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
from bounds import RasterBounds
from fiona.transform import transform
import bounds



shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
CA_rast = "/Users/datateam/repos/spatial-introspect/NE1_50M_SR_W_tenth_CA.tif"
csv_ex = "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv"
NM_rast = "/Users/datateam/Desktop/test_data/soil_color_NM/NM_125cm.tif"
sampling_sites = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.5.5"
csv_no_geo = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.10.2"

shp_NM = "/Users/datateam/Desktop/snotel_201701_1169_shp/snotel_201701_1169.shp"

bounds1 = RasterBounds(raster=rast_ex)
print(bounds1)


# for both vector and raster I need to reproject

class MyException(Exception):
    pass


def get_extent_for_vector(shapefile):
    lats = []
    lons = []
    with fiona.open(shapefile, 'r') as src:
        for feat in src:
            # if ['geometry'] is not type Point:
            #     raise MyException('Point data') look at formatting here: https://github.com/Toblerity/Fiona/blob/master/fiona/transform.py
            # work on this later, work on transforming first
            coords = feat['geometry']['coordinates'][0] # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
            [(lons.append(x), lats.append(y)) for x, y in coords]
            # transform('EPSG:4326', 'EPSG:4326', xs=lons, ys=lats) # this might need to be x, y
            print(lats, lons)

    # min_lat, max_lat = min(lats), max(lats)
    # min_lon, max_lon = min(lons), max(lons)
    # print('South extent: {}\nNorth extent: {}\nWest extent: {}\nEast extent: {}'.format(min_lat,
    #                                                                                     max_lat,
    #                                                                                     min_lon,
    #                                                                                     max_lon))
get_extent_for_vector(shp_fn)


# Practice using transform before putting it in a function
abc = fiona.open(shp_fn, 'r')
rec = next(abc)
print(rec['geometry']['coordinates'])
lats = []
lons = []
crds = rec['geometry']['coordinates']
crds0 = rec['geometry']['coordinates'][0] # [0] gets rid of one of the brackets
[(lons.append(x), lats.append(y)) for x, y in coords] # I think I need to iterate through the list to extract x, y
print(crds0)

for

coords = ['coordinates'][0] # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
[(lons.append(x), lats.append(y)) for x, y in coords]
transform('EPSG:4326', 'EPSG:26953', lons, lats)


from shapely.geometry import shape
c = fiona.open("/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp")
# first record
country = c.next()
print(country)
print(c)
c.bounds
c.next

shapely.geometry.shape(c)



# Need to convert when using files like NM_raster that are in meters
'''rightm but that's probably what you're going to want. if you want to find it's bounds in geographic coordinates you need to 
'reproject' the coordinates you have, or reproject the entire raster. 
rasterio will reproject the raster, if you want to do that programmatically. 
or you can use `pyproj` to convert the coordinates directly'''
def get_extent_for_raster(raster):
    with rasterio.open(raster, 'r') as ds:
        #ds.features.bounds(geometry = polygon, north_up = True, transform = None)
        print(ds.bounds) # need to transform and probably do return here instead of print
        print(ds.meta) #gets more info about the raster

get_extent_for_raster(NM_rast)


def get_extent(file_path):
    try:
        extent = get_extent_for_vector(file_path)
    except errors.FionaValueError:
        extent = get_extent_for_raster(file_path)

    return extent


# # # CSV # # #

# Extracts extent if lat and lon exist in column names
def get_extent_csv(csv):
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
        lon_name = check_lon(csv_df)
    except MyException:
        raise MyException('Latitude or longitude cannot be guessed.')

    csv_df['geometry'] = csv_df.apply(lambda r: Point(r[lon_name], r[lat_name]), axis=1)
    pnt_gdf = gpd.GeoDataFrame(csv_df)

    return pnt_gdf.total_bounds
