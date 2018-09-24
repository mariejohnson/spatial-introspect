import fiona
import rasterio
from rasterio import RasterioIOError
import os


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