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
import re
from fiona._transform import _transform, _transform_geom
from pyproj import Proj
from vector_bounds import RasterBounds, GeoBounds, VectorBounds
import bounds


# Issue: if it's not a polygon
def get_extent_vector(shapefile):
    vb = VectorBounds(shapefile)
    bounds = list((vb.west, vb.south, vb.east, vb.north))
    #print(bounds)
    return bounds

get_extent_vector(shp_fn)


def get_extent_raster(raster):
    rbnds = RasterBounds(raster)
    bounds = list((rbnds.west, rbnds.south, rbnds.east, rbnds.north))
    #print(bounds)
    return bounds

get_extent_raster(CA_rast)


# **************************************************************************************************** #


def get_extent(file_path):
    try:
        extent = get_extent_vector(file_path)
    except errors.FionaValueError: # this will raise an exception if it's a CSV "unsupported driver"
        extent = get_extent_raster(file_path)
    return extent



get_extent(shp_fn)

get_extent(CA_rast)

get_extent(csv_ex)

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
