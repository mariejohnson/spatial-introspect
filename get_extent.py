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


# One problem will be if it is not a polygon (or maybe that is dealt with?) or maybe that doesn't matter
# for point it should just show up as w,e = same coordinates and s,n = same coordinates
def get_extent_vector(shapefile):
    with fiona.open(shapefile, 'r') as src:
        bb = src.bounds # this is fiona
        bbox = list(bb)
        # Below is not technically needed but a good check
        # print(bbox)
        # print('West extent: {}\nSouth extent: {}\nEast extent: {}\nNorth extent: {}'.format(bbox[0],
        #                                                                                     bbox[1],
        #                                                                                     bbox[2],
        #                                                                                     bbox[3]))
        return bbox

get_extent_vector(shp_fn)
get_extent_vector(shp_NM)


bbox = bounds.GeoBounds(west=9085047, south=11971301, east=10104624, north=12228183)
geo_bounds = bbox.to_geographic(epsg=3857)
print(geo_bounds)



def get_extent_raster(raster):
    rbnds = RasterBounds(raster)
    bounds = list((rbnds.west, rbnds.south, rbnds.east, rbnds.north))
    print(bounds)
    return bounds

get_extent_raster(CA_rast)



# **************************************************************************************************** #

# Currently working on
# add more extensions, eventually add to larger function
def check_format(name):
    class MyException(Exception):
        pass
    if name.endswith(('.shp', '.csv', '.tif', )):
        print('Good') # maybe return something?
    else:
        raise MyException('Incompatible file format')

check_format(CA_rast)



# **************************************************************************************************** #



# # # Exceptions for rasters and vectors # # #

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
