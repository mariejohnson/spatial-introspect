import re

import fiona
import geopandas as gpd
import pandas as pd
from fiona import errors
from pandas import errors
from shapely.geometry import Point

from vector_bounds import RasterBounds, VectorBounds


# Sample files
shp_fn = "/Users/datateam/repos/spatial_introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial_introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
CA_rast = "/Users/datateam/repos/spatial_introspect/NE1_50M_SR_W_tenth_CA.tif"
csv_ex = "/Users/datateam/repos/spatial_introspect/test_data/SitiosMuestreoPasto.csv"
NM_rast = "/Users/datateam/Desktop/test_data/soil_color_NM/NM_125cm.tif"
sampling_sites = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.5.5"
csv_no_geo = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/huayhuash.10.2"
shp_NM = "/Users/datateam/Desktop/snotel_201701_1169_shp/snotel_201701_1169.shp"
test_csv = "/Users/datateam/Desktop/no_geo.csv"


def get_extent_vector(shapefile):
    vb = VectorBounds(shapefile)
    bounds = list((vb.west, vb.south, vb.east, vb.north))
    return bounds


# get_extent_vector(shp_NM)


def get_extent_raster(raster):
    rbnds = RasterBounds(raster)
    bounds = list((rbnds.west, rbnds.south, rbnds.east, rbnds.north))
    # print(bounds)
    return bounds


# get_extent_raster(CA_rast)


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

    return pnt_gdf.total_bounds.tolist()

get_extent_csv(test_csv)

# **************************************************************************************************** #


def get_extent(file_path):
    try:
        extent = get_extent_csv(file_path)
    except pd.errors.ParserError:
        try:
            extent = get_extent_vector(file_path)
        except fiona.errors.FionaValueError:
            extent = get_extent_raster(file_path)
    return extent


get_extent(shp_fn) # works

print(get_extent(CA_rast)) # works

get_extent(test_csv) # works
