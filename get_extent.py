import re
import fiona
import geopandas as gpd
import pandas as pd
from fiona import errors
from pandas import errors
from shapely.geometry import Point
from bounds import RasterBounds, VectorBounds


# Sample files
herd_shp_file = "test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
CA_raster = "test_data/NE1_50M_SR_W_tenth_CA.tif"
csv_geo = "https://raw.githubusercontent.com/mariejohnson/spatial_introspect/master/test_data/SitiosMuestreoPasto.csv"
csv_no_geo = "https://raw.githubusercontent.com/mariejohnson/spatial_introspect/master/test_data/no_geo.csv"


def get_extent_vector(shapefile):
    """ Get geographic extent (WSEN) from shapefile

    Parameters
    ----------
    shapefile : str
        Filepath to a shapefile

    Returns
    -------
    Bounding box of vector in geographic coordinates

    """
    vb = VectorBounds(shapefile)
    bounds = list((vb.west, vb.south, vb.east, vb.north))
    return bounds

def get_extent_raster(raster):
    """ Get geographic extent (WSEN) from raster

    Parameters
    ----------
    raster : str
        Filepath to a raster

    Returns
    -------
    Bounding box of raster in geographic coordinates

    """
    rbnds = RasterBounds(raster)
    bounds = list((rbnds.west, rbnds.south, rbnds.east, rbnds.north))

    return bounds


def get_extent_csv(csv):
    """ Get geographic extent (WSEN) from CSV

    Parameters
    ----------
    csv : str
        Filepath to a csv

    Returns
    -------
    Bounding box of csv if lat and lon exist in column names

    """
    csv_df = pd.read_csv(csv)

    class ExtentFailedCSV(Exception):
        pass

    def check_cols(csv_df, col_string):
        results = []
        pat = re.compile(col_string, flags=re.IGNORECASE)
        for col_name in csv_df.columns:
            if pat.match(col_name) is not None:
                results.append(col_name)
        if len(results) != 1:
            raise ExtentFailedCSV
        return results

    def check_lat(csv_df):
        return check_cols(csv_df, "lat")

    def check_lon(csv_df):
        return check_cols(csv_df, "lon")

    try:
        lat_name = check_lat(csv_df)
        lon_name = check_lon(csv_df)
    except ExtentFailedCSV:
        raise ExtentFailedCSV('Latitude or longitude cannot be guessed.')

    csv_df['geometry'] = csv_df.apply(lambda r: Point(r[lon_name], r[lat_name]), axis=1)
    pnt_gdf = gpd.GeoDataFrame(csv_df)

    return pnt_gdf.total_bounds.tolist()


def get_extent(file_path):
    """ Get geographic extent (WSEN) from a shapefile, raster or CSV

    Parameters
    ----------
    vector, raster or csv : str
        Filepath to vector, raster or csv

    Returns
    -------
    Bounding box of vector, raster or csv
    """
    try:
        extent = get_extent_csv(file_path)
    except pd.errors.ParserError:
        try:
            extent = get_extent_vector(file_path)
        except fiona.errors.FionaValueError:
            extent = get_extent_raster(file_path)
    return extent


