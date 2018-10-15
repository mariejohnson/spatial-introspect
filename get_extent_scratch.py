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

def generic_check_for_cols(df, col_string):
    results = []
    pat = re.compile(col_string, flags=re.IGNORECASE)
    for col_name in df.columns:
        if pat.match(col_name) is not None:
            results.append(col_name)

    return results

def check_lat(df):
    return generic_check_for_cols(df, "lat")

lat_name = check_lat(sites_df)
# How to I extract the column name so I don't have to label it below

# # # Once you obtain Lat/Lon Column Names

from shapely.geometry import Point

csv_file = "some/file/that/is/not/really/here.csv"

# determined above
lat_name = "Latitude"
lon_name = "Long"

pnt_df = pd.read_csv(csv_file)
# should probably check that the column name 'geometry' does not already exist
# maybe doesn't matter because we're just trying to get extent. ...not saving these results
# create geometry column
pnt_df['geometry'] = pnt_df.apply(lambda r: Point(r[lon_name], r[lat_name]), axis=1)
pnt_gdf = gpd.GeoDataFrame(pnt_df)

# get the total bounds
pnt_gdf.total_bounds

# This is a not generic but good practice for me
results = []
pat = re.compile("lat", flags=re.IGNORECASE)
# add more to lat pattern
for col_name in sites_df.columns:
    if pat.match(col_name) is not None:
        results.append(col_name)

print(results)

# # # Check lat lon in column names functions
def check_for_lat_cols(df):
    results = []
    pat = re.compile("lat", flags=re.IGNORECASE)
    #needs to be broader? to exclude things like "plate"
    for col_name in df.columns:
        if pat.match(col_name) is not None:
            results.append(col_name)

    return results
check_for_lat_cols(sites_df)

regions_fp = "https://knb.ecoinformatics.org/knb/d1/mn/v2/object/urn%3Auuid%3Af6ab206b-312c-4caf-89c8-89eb9d031aac"
# should actually be pd.read_csv
regions = gpd.read_file(regions_fp).to_crs(epsg=3338)
print(regions.columns)

results = []
pat = re.compile("REG", flags=re.IGNORECASE)
for col_name in regions.columns:
    if pat.match(col_name) is not None:
        results.append(col_name)

print(results)

# example of some things you can do with re
foo = pat.match("region")
print(foo)
foo_string = foo.string
print(foo_string)
# I think something is supposed to go in () or something, not really working here
foo_groups = foo.groups()
print(foo_groups)


# # # Once you obtain Lat/Lon Column Names

lat_name = check_lat(sites_df)
lon_name = check_lon(sites_df)

# pnt_df = pd.read_csv(csv_file)

sites_df['geometry'] = sites_df.apply(lambda r: Point(r[lon_name], r[lat_name]), axis=1)
pnt_gdf = gpd.GeoDataFrame(sites_df)

# get the total bounds
pnt_gdf.total_bounds


def generic_check_for_cols(df, col_string):
    results = []
    pat = re.compile(col_string, flags=re.IGNORECASE)
    for col_name in df.columns:
        if pat.match(col_name) is not None:
            results.append(col_name)

    return results

def check_lat(df):
    return generic_check_for_cols(df, "lat")


def check_lon(df):
    return generic_check_for_cols(df, "lon")


# # # Once you obtain Lat/Lon Column Names


def the_actual_whole_function(csv_file_path):
    csv_df = pd.read_csv(csv_file_path)

    try:
        lat_name = check_lat(csv_df)
        lon_name = check_lon(csv_df)
    except MyException:
        raise MyException('Lat or lon column can not be guessed.')

    csv_df['geometry'] = csv_df.apply(lambda r: Point(r[lon_name], r[lat_name]), axis=1)
    pnt_gdf = gpd.GeoDataFrame(csv_df)

    return pnt_gdf.total_bounds

the_actual_whole_function(sampling_sites)


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


#documentation: http://geopandas.org/gallery/create_geopandas_from_pandas.html#sphx-glr-gallery-create-geopandas-from-pandas-py

#Needs to be applied more broadly, find some way not to just use "Long" "Lat"
def get_extent_csv(filepath):
    df = pd.read_csv(filepath)
    df['coordinates'] = list(zip(df.Long, df.Lat))
    df['coordinates'] = df['coordinates'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='coordinates')
    bnds = gdf.total_bounds
    print(bnds)

get_extent_csv(csv_ex)


class MissingLongitude(Exception):
    pass

class MissingLatitude(Exception):
    pass

def get_lon(csv_file):
    df = pd.read_csv(csv_file)
    cols = df.columns
    if "lon" in cols:
        lon_ix = cols.index('lon')
        print(lon_ix)
    elif "x" in cols:
        lon_ix = cols.index('x')
    else:
        raise MissingLongitude('This csv appears to be missing a longitude field')

get_lon(csv_ex)


def get_lat(csv_file):
    df = pd.read_csv(csv_file)
    cols = df.columns
    if "lat" in cols:
        lon_ix = cols.index('lon')
    elif "y" in cols:
        lon_ix = cols.index('x')
    else:
        raise MissingLatitude('This csv appears to be missing a latitude field')


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

#lon = x lat = y
# xMin yMin, xMax, yMax
shp_file = fiona.open(shp_fn, 'r')
# this is all you need to do to get info about shape file, you can inspect it in the window, or probably print it
shp_file.crs
# {'init': 'epsg:3857'}

shp_file.bounds
# (9085047.3347, 11971301.884999998, 10104624.212199999, 12228183.776099999)

_transform('EPSG:3857', 'EPSG:3576', [9085047.3347, 10104624.212199999], [11971301.884999998, 12228183.776099999])
_transform({'proj': 'lcc', 'lat_0': 18.0, 'lat_1': 18.0, 'lon_0': -77.0}, {'proj': 'lcc', 'lat_0': 18.0, 'lat_1': 18.0, 'lon_0': -77.0}, [9085047.3347, 10104624.212199999], [11971301.884999998, 12228183.776099999])

p = Proj(proj='merc',zone=10,ellps='WGS84') # use kwargs
x,y = p(9085047.3347, 11971301.884999998)

lons, lats = p(x, y, inverse=True)

print(lons)

lats = [90, 89, 23, 86, 94, 74]
lons = [78, 73, 44, 65, 78, 74]
[(lons.append(x), lats.append(y)) for x, y in coords]

foo = lons.append()
print(foo)
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



coords = ['coordinates'][0] # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
[(lons.append(x), lats.append(y)) for x, y in coords]
transform('EPSG:4326', 'EPSG:26953', lons, lats)


from shapely.geometry import shape
c = fiona.open("/Users/datateam/repos/spatial_introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp")
# first record
country = c.next()
print(country)
print(c)
c.bounds
c.next

shapely.geometry.shape(c)


'''rightm but that's probably what you're going to want. if you want to find it's bounds in geographic coordinates you need to 
'reproject' the coordinates you have, or reproject the entire raster. 
rasterio will reproject the raster, if you want to do that programmatically. 
or you can use `pyproj` to convert the coordinates directly'''

shp_file = fiona.open(shp_fn, 'r')
fiona_bb = shp_file.bounds
print(fiona_bb) # Need to turn this into w, s, e, n

with fiona.open(shapefile, 'r') as src:
    for bbox in src:
        fiona_bb = shp_file.bounds

NM_shp_file = fiona.open(shp_NM, 'r')
fiona_bb = shp_file.bounds
print(fiona_bb) # Need to turn this into w, s, e, n

# Likely all garbage

def check_format(file_name):
    pat = re.compile(r'\.shp|\.csv')
    matches = pat.findall(file_name)  # was abc before
    for x in matches:
        if x is False:
            print("bad")
        else:
            print("good")
check_format(csv_ex)

def check_format(file_name):
    class MyException(Exception):
        pass
    pat = re.compile(r'\.shp|\.csv')
    matches = pat.findall(file_name)
    if matches is False:
        print("Good") #just a test for the time being
    else:
        raise MyException("incompatible format ")
check_format(CA_rast)

#this works I think ... but maybe not
abc = ".csv"
pat = re.compile(r'\.shp|\.csv')
matches = pat.findall(csv_ex) # was abc before
for x in matches:
    if matches is False:
        print("bad")
    else:
        print("good")

# I don't know that any of this works

def generic_check_for_cols2(csv, col_string):
    csv_df = pd.read_csv(csv)
    class MyException(Exception):
        pass
    results = []
    pat = re.compile(col_string, flags=re.IGNORECASE)
    for col_name in csv_df.columns:
        if pat.match(col_name) is not None:
            results.append(col_name)
    if len(results) != 1:
        raise MyException
    return results

generic_check_for_cols2(csv_ex, "lat")

def generic_check_for_cols3(df, col_string):
    results = []
    pat = re.compile(col_string, flags=re.IGNORECASE)
    for col_name in df.columns:
        if pat.match(col_name) is not None:
            results.append(col_name)

    return results



# so this doesn't give me the correct error when I enter a non-raster or non-vector file, it
def get_extent(file_path):
    class MyException(Exception):
        pass
    ext = [".csv", ".shp"] # this doesn't really work
    # if file_path != file_path.endswith(tuple(ext)): # works
    #     raise MyException('Incorrect format')
    # try:
    #     file_path != file_path.endswith(tuple(ext))
    #         raise MyException('Incorrect format')
    # for i in ext:
    #     if i.endswith(tuple(ext)) is False:
    #         raise MyException("Incorrect format")
    try:
        extent = get_extent_vector(file_path)
    except errors.FionaValueError:
        extent = get_extent_raster(file_path)
    # if file extention doesn't equal .shp or .tif (hmm, there's probably a better way) raise exception "Unable to get coordinates from this type of file format"
    # maybe start off with if does not equal .shp or .tif raise exception
    print(extent)

    return extent

get_extent(CA_rast)


def check_extension(file_name):
    class MyException(Exception):
        pass
    results = []
    pat = re.compile(r'\.shp|\.csv')
    for ext in pat:
        if pat.match(ext) is False:
            raise MyException('Incorrect format')
    print()


# this is a working function (maybe?)
def check_extension(file_name):
    class MyException(Exception):
        pass
    pat = re.compile(r'\.shp|\.csv')
    matches = pat.findall(file_name)
    print(matches) # ['.csv', '.csv']
    for x in matches:
        print(x) # .csv .csv
        if x :
            print(x)
        # else:
        #     raise MyException("incorrect format")

check_extension(csv_ex)

# This doesn't actually work
def get_extent(file_path):
    class MyException(Exception):
        pass
    try:
        if name.endswith(('.csv', '.txt',)):
            extent = get_extent_csv(file_path)
            return extent
        elif:
            try:
                extent = get_extent_vector(file_path)
            except errors.FionaValueError:
                extent = get_extent_raster(file_path)
            return extent
        else:
            raise MyException("Incompatible format")

crs_int = int(src.crs['init'].split(":")[1])

prof = rst.profile['transform']

# Good stuff
# So I need to put this in vector bounds
shp_epsg = shp.crs['init'].split(":")[1] # "[1] accesses the number, if it was [0] I would get "epsg"
epsg_integer = int(shp_epsg)
print(shp_epsg)

shp_epsg = int(shp.crs['init'].split(":")[1]) # "[1] accesses the number, if it was [0] I would get "epsg"
print(shp_epsg)


v = VectorBounds(shp_fn)
v.to_geographic()
v.to_epsg(3857)

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


# So I can use this if I can get the output from to go into the s,w,e,n arguments in GeoBounds
bbox = bounds.GeoBounds(west=9085047, south=11971301, east=10104624, north=12228183)
geo_bounds = bbox.to_geographic(epsg=3857)
print(geo_bounds)

def get_extent(file_path):
    class MyException(Exception):
        pass
    try:
        extent = get_extent_csv(file_path)
    except Exception as e: # no idea?
        extent = get_extent_vector(file_path)
    except errors.FionaValueError:
        extent = get_extent_raster(file_path)
      # None of these things it raises an exception to tell me if it's not compatible
    return extent

shp = fiona.open(shp_fn, 'r')
rst = rasterio.open(CA_rast, 'r')


v = VectorBounds(shp_fn)
v.to_geographic()
v.to_epsg(3857)