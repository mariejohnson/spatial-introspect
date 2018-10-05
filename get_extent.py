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
from fiona._transform import _transform, _transform_geom
from pyproj import Proj
from bounds import RasterBounds
from bounds import GeoBounds
import bounds



shp_fn = "/Users/datateam/repos/spatial_introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial_introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
CA_rast = "/Users/datateam/repos/spatial_introspect/NE1_50M_SR_W_tenth_CA.tif"
csv_ex = "/Users/datateam/repos/spatial_introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv"
NM_rast = "/Users/datateam/Desktop/test_data/soil_color_NM/NM_125cm.tif"
sampling_sites = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.5.5"
csv_no_geo = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.10.2"
shp_NM = "/Users/datateam/Desktop/snotel_201701_1169_shp/snotel_201701_1169.shp"


# need to turn this into a function
# One problem will be if it is not a polygon (or maybe that is dealt with?) or maybe that doesn't matter
def get_extent_vector(shapefile):
    with fiona.open(shapefile, 'r') as src:
        bb = src.bounds
        bbox = list(bb)
        west = []
        south = []
        east = []
        north = []
        for i in bbox: #this doesn't exactly work
            west.append(bbox[0])
            south.append(bbox[1])
            east.append(bbox[2])
            north.append(bbox[3])

            print(bbox[i]) # Need to turn this into w, s, e, n
            # maybe print i? No. I'm thinking about this wrong

get_extent_vector(shp_fn)




shp_file = fiona.open(shp_fn, 'r')
fiona_bb = shp_file.bounds
print(fiona_bb) # Need to turn this into w, s, e, n

with fiona.open(shapefile, 'r') as src:
    for bbox in src:
        fiona_bb = shp_file.bounds

NM_shp_file = fiona.open(shp_NM, 'r')
fiona_bb = shp_file.bounds
print(fiona_bb) # Need to turn this into w, s, e, n

bbox = bounds.GeoBounds(west=9085047, south=11971301, east=10104624, north=12228183)
geo_bounds = bbox.to_geographic(epsg=3857)
print(geo_bounds)


# Need to convert when using files like NM_raster that are in meters, this does that

bounds1 = RasterBounds(raster=CA_rast)
print(bounds1)

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
