import fiona
from fiona import errors
import rasterio
from rasterio import RasterioIOError
import os
import pandas as pd
import numpy as np
import geopandas
from geopandas import GeoDataFrame
import shapely
from shapely.geometry import Point
import sys
import matplotlib
import matplotlib.cbook


shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
CA_rast = "/Users/datateam/repos/spatial-introspect/NE1_50M_SR_W_tenth_CA.tif"
csv_ex = "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv"
NM_rast = "/Users/datateam/Desktop/test_data/soil_color_NM/NM_125cm.tif"
# my scratch paper or things I didn't want to just delete (some of it might be useful at some point)

shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"

# practice
# this doesn't work because 'SHAPE_Area' is a float and not a list of any sort
def get_area(shape_file):
    a = []
    with fiona.open(shape_file, 'r') as src:
        for feat in src:
            area = feat['properties']['SHAPE_Area'] #not sure I understand why debugger isn't work here
            [(a.append(x)) for x in area]
    print(area)

# this does print the last value in 'SHAPE_Area'. I guess that's confusing because it must be a list of some sort
shp_fn = "/Users/datateam/repos/spatial-introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"
def get_area(shape_file):
    with fiona.open(shape_file, 'r') as src:
        for feat in src:
            area = feat['properties']['SHAPE_Area']
    print(area)

get_area(shp_fn)


rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
def get_extent_for_raster(raster):
    l = []
    b = []
    r = []
    t = []
    with rasterio.open(raster, 'r') as src:
        for feat in src:
            bb = feat['bounds']
            print(bb['bottom'], bb['left'])

get_extent_for_raster(rast_ex)

rast_ex = "/Users/datateam/repos/spatial-introspect/test_data/NE1_50M_SR/NE1_50M_SR.tif"
def get_extent_for_raster(raster):
    with rasterio.open(raster, 'r') as src:
        for feat in src:
            bb = raster.bounds
            print(bb)

get_extent_for_raster(rast_ex)

abc = dataset.read(1)
print(abc)

def get_extent_for_raster(raster):
    bb = rasterio.open(raster, 'r')
    bbox = bb.bounds.left(raster)
    return bbox
get_extent_for_raster(rast_ex)



l, b, r, t = (dataset.bounds.left, dataset.bounds.bottom, dataset.bounds.right, dataset.bounds.top)
print(l, b, r, t)


# PANDAS SCRATCH

csv_ex = "/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv"

def get_coords(file_path):
    df = pd.read_csv(file_path)
    x = df['Lat']
    y = df['Long']
    #df2 = pd.DataFrame([x,y])
    df3 = pd.DataFrame([df['Lat'], df['Long']])
    print(df3)
get_coords(csv_ex)


def get_coords(file_path):
    df = pd.read_csv(file_path)
    x = df['Lat']
    y = df['Long']
    df2 = pd.DataFrame([x,y])
    print(df2)
get_coords(csv_ex)


#figure out how to iterate
def get_extent_csv(file_path):
    df = pd.read_csv(file_path)
    for col in df.iterrows(): #hmm I think I need it to skip the first row, possibly by setting index, I think this is already default?
        coords = col['Lat']['Long']
        print(coords)

get_extent_csv(csv_ex)

#Transform coordinates
from pyproj import Proj, transform

inProj = Proj(init='epsg:3857')
outProj = Proj(init='epsg:4326')
x1,y1 = -11705274.6374,4826473.6922
x2,y2 = transform(inProj,outProj,x1,y1)
print x2,y2


# Now I need to turn this into a function and make it into a bounding box
df = pd.read_csv("/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv")
geometry = [Point(xy) for xy in zip(df.Lat, df.Long)]
df = df.drop(['Lat', 'Long'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)
print(gdf)


#Start over with directions from website: http://geopandas.org/gallery/create_geopandas_from_pandas.html#sphx-glr-gallery-create-geopandas-from-pandas-py

df2 = pd.read_csv("/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv")

df2['coordinates'] = list(zip(df2.Long, df2.Lat))

df2['coordinates'] = df2['coordinates'].apply(Point)

gdf2 = geopandas.GeoDataFrame(df2, geometry='coordinates')


bounds1 = gdf2.bounds
#bounds1 is a dataframe
print(bounds1)
# Not exactly what I want but maybe. I think I want (out of the entire list) (minx, miny) and (maxx, maxy)
# actually that'd be fairly easy to convert here I think.

#Just goofing around with pandas.
minx = bounds1['minx']
print(minx)

min_minx = minx.min
print(min_minx)

bounds1.min['minx']

#This: http://geopandas.org/gallery/create_geopandas_from_pandas.html#sphx-glr-gallery-create-geopandas-from-pandas-py

#To find the name of the geometry which is the geoseries
#gdf.geometry.name

#This worked but I'm not sure that it is actually a geoseries
gs = gdf.geometry
print(gs)


bnds = geopandas.gs.bounds

gs1 = geopandas.GeoSeries(gdf)


# this is unsuccessful
def get_extent_csv(file_path):
    df = pd.read_csv(file_path)
    for col in df: #hmm I think I need it to skip the first row, possibly by setting index, I think this is already default?
        coords = df.iterrows()
        print(coords)

get_extent_csv(csv_ex)

def get_bounds_csv(filepath):
    df = pd.read_csv(filepath)
    df['coordinates'] = list(zip(df.Long, df.Lat))
    df['coordinates'] = df['coordinates'].apply(Point)
    gdf = geopandas.GeoDataFrame(df, geometry='coordinates')
    bnds = gdf.bounds
    print(bnds)


df = pd.read_csv("/Users/datateam/repos/spatial-introspect/test_data/sample_d1_files/urn_uuid_5bb3f86b_ef85_447f_a026_6d8eb6306ea4/data/huayhuash.5.5-2010-11_Huayhuash_SitiosMuestreoPasto.csv.csv")

df['coordinates'] = list(zip(df.Long, df.Lat))

df['coordinates'] = df['coordinates'].apply(Point)

gdf = geopandas.GeoDataFrame(df, geometry='coordinates')


bnds = gdf.bounds
#bnds is a dataframe
print(bnds)
# Not exactly what I want but maybe. I think I want (out of the entire list) (minx, miny) and (maxx, maxy)
# actually that'd be fairly easy to convert here I think.

total_bnds = gdf.total_bounds
print(total_bnds)

'''
This: https://gis.stackexchange.com/questions/174159/convert-a-pandas-dataframe-to-a-geodataframe
from geopandas import GeoDataFrame
from shapely.geometry import Point

geometry = [Point(xy) for xy in zip(df.Lon, df.Lat)]
df = df.drop(['Lon', 'Lat'], axis=1)
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df, crs=crs, geometry=geometry)

Maybe this: https://gis.stackexchange.com/questions/114066/handling-kml-csv-with-geopandas-drivererror-unsupported-driver-ucsv

import pandas as pd
import geopandas as gp
from shapely.geometry import Point

stations = pd.read_csv('../data/stations.csv')
stations['geometry'] = stations.apply(lambda z: Point(z.X, z.Y), axis=1)
stations = gp.GeoDataFrame(stations)

Maybe this: https://gist.github.com/tchajed/93c347aeb2b24f034ea3

'''