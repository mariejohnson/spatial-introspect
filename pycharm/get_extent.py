import fiona
import rasterio
from rasterio import RasterioIOError
import os

# practicing pushing via pycharm

shp_fn = "/home/shares/scientist/sasap-biophys/HabitatMetrics/glaciers/Glaciers_RAP.shp"

def get_extent_for_raster(file_path):
    ds = rasterio.open(file_path)
    # do stuff with ds (data source) to get extent
    # then return extent
    
def get_extent_for_vector(file_path):
    ds = fiona.open(file_path)
    # do stuff with ds (data source) to get extent
    # maybe like this: https://gis.stackexchange.com/questions/90553/fiona-get-each-feature-extent-bounds
    # then return extent
    
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

def get_extent_if_possible(file_path):
    try:
        extent = get_extent_for_vector(file_path)
    except RasterioIOError:
        extent = get_extent_for_raster(file_path)
        
    return extent
    
get_extent_if_possible(shp_fn)