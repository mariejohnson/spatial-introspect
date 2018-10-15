import re

import fiona
import geopandas as gpd
import pandas as pd
from fiona import errors
from pandas import errors
from shapely.geometry import Point

from vector_bounds import RasterBounds, VectorBounds


# Local sample files
shp_file = "/Users/datateam/repos/spatial_introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
CA_rast = "/Users/datateam/repos/spatial_introspect/test_data/NE1_50M_SR_W_tenth_CA.tif"
csv_ex = "/Users/datateam/repos/spatial_introspect/test_data/SitiosMuestreoPasto.csv"
test_csv = "/Users/datateam/Desktop/no_geo.csv"

# On github
herd_shp = "https://github.com/mariejohnson/spatial_introspect/raw/master/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
# can't get the shapefile to download via github but it works locally
CA_raster = "https://github.com/mariejohnson/spatial_introspect/raw/master/test_data/NE1_50M_SR_W_tenth_CA.tif"
csv_no_geo = "https://raw.githubusercontent.com/mariejohnson/spatial_introspect/master/test_data/no_geo.csv"
csv_geo = "https://raw.githubusercontent.com/mariejohnson/spatial_introspect/master/test_data/SitiosMuestreoPasto.csv"


def get_extent_vector(shapefile):
    vb = VectorBounds(shapefile)
    bounds = list((vb.west, vb.south, vb.east, vb.north))
    return bounds

def get_extent_raster(raster):
    rbnds = RasterBounds(raster)
    bounds = list((rbnds.west, rbnds.south, rbnds.east, rbnds.north))
    # print(bounds)
    return bounds

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


# **************************************************************************************************** #

# works for CSV's, vectors, rasters
def get_extent(file_path):
    try:
        extent = get_extent_csv(file_path)
    except pd.errors.ParserError:
        try:
            extent = get_extent_vector(file_path)
        except fiona.errors.FionaValueError:
            extent = get_extent_raster(file_path)
    return extent






