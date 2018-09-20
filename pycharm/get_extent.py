import fiona
from fiona import errors
import rasterio
from rasterio import RasterioIOError
import os


shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"

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
#get_extent_for_vector(shp_fn)


def get_extent_for_raster(raster):
    ds = rasterio.open(raster, 'r')
    print(ds.bounds)

#get_extent_for_raster(rast_ex)



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
#need to put fiona error
# def get_extent_if_possible(file_path):
#     try:
#         extent = get_extent_for_vector(file_path)
#     except RasterioIOError:
#         extent = get_extent_for_raster(file_path)
#
#     return extent


def get_extent_if_possible(file_path):
    try:
        extent = get_extent_for_vector(file_path)
    except errors.FionaValueError:
        extent = get_extent_for_raster(file_path)

    return extent


get_extent_if_possible(shp_fn)
get_extent_if_possible(rast_ex)