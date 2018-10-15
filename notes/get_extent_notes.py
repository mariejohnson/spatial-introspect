def get_extent_for_vector(shapefile):
    lats = []
    lons = []
    with fiona.open(shapefile, 'r') as src:
        for feat in src:
            coords = feat['geometry']['coordinates'][
                0]  # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
            [(lons.append(x), lats.append(y)) for x, y in coords]

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    print('South extent: {}\nNorth extent: {}\nWest extent: {}\nEast extent: {}'.format(min_lat,
                                                                                        max_lat,
                                                                                        min_lon,
                                                                                        max_lon))


get_extent_for_vector(shp_fn)

# Need to convert when using files like NM_raster that are in meters
'''rightm but that's probably what you're going to want. if you want to find it's bounds in geographic coordinates you need to 
'reproject' the coordinates you have, or reproject the entire raster. 
rasterio will reproject the raster, if you want to do that programmatically. 
or you can use `pyproj` to convert the coordinates directly'''


def get_extent_for_raster(raster):
    with rasterio.open(raster, 'r') as ds:
        print(ds.bounds)
        print(ds.meta)  # gets more info about the raster


get_extent_for_raster(CA_rast)
# get_extent_for_raster(NM_rast)


'''
Notes on get_extent_for_raster()
From Dave
you want a context manager for that, so it closes automatically, that way when the function is done, the file gets closed, 
not a big deal in this situation, but the convention keeps you from serious bugs later on.
"with" is the context manager: when the code returns to the same indentation level as `with`, the file is automatically closed, +1 for python

To potentially add later:
when the code returns to the same indentation level as `with`, the file is automatically closed, +1 for python
a lot of times, I'll get what I need and return to lower indentation level, so if it's a large raster, that memory is freed for other processes:

def get_extent_for_raster(raster):
    with rasterio.open(raster, 'r') as ds:
        bounds = ds.bounds
        meta = ds.meta
		arr = ds.read()

	modified = arr.do_something_with_numpy_array()  # raster closes here

'''

'''

# Old pandas code
for row, col in df1.iterrows():
    if col['Circumference'] > 0.0:
        dense = missbark(bk_mass=col['DryMassBark'], ba=col['bark_area'], circ=col['Circumference'], cnb=col['CircNoBark'], thick=col['avg_thickness'])
    else:
        dense = bark(bk_mass=col['DryMassBark'], ba=col['bark_area'], thick=col['avg_thickness'])

    df1['bark_density'][row] = dense

'''

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

'''rightm but that's probably what you're going to want. if you want to find it's bounds in geographic coordinates you need to 
'reproject' the coordinates you have, or reproject the entire raster. 
rasterio will reproject the raster, if you want to do that programmatically. 
or you can use `pyproj` to convert the coordinates directly'''

def get_extent_for_raster(raster):
    with rasterio.open(raster, 'r') as ds:
        #ds.features.bounds(geometry = polygon, north_up = True, transform = None)
        print(ds.bounds) # need to transform and probably do return here instead of print
        print(ds.meta) #gets more info about the raster
get_extent_for_raster(NM_rast)
# Output
# BoundingBox(left=-1233765.0836359565, bottom=883320.4870200155, right=-616761.8164309527, top=1688461.6052094982)
# {'driver': 'GTiff', 'dtype': 'uint8', 'nodata': 255.0, 'width': 2499, 'height': 3261, 'count': 3, 'crs': CRS({'proj': 'aea', 'lat_1': 29.3, 'lat_2': 45.5, 'lat_0': 23, 'lon_0': -96, 'x_0': 0, 'y_0': 0, 'datum': 'NAD83', 'units': 'm', 'no_defs': True}), 'transform': Affine(246.900066908765, 0.0, -1233765.0836359565,
#        0.0, -246.900066908765, 1688461.6052094982)}

# Affine(246.900066908765, 0.0, -1233765.0836359565,
#        0.0, -246.900066908765, 1688461.6052094982)}

# Affine Transformation: https://support.esri.com/en/other-resources/gis-dictionary/term/3526be0c-e296-4c90-bb07-8a8cb121f693
# A geometric transformation that scales, rotates, skews, and/or translates images or coordinates between any two Euclidean spaces.
# It is commonly used in GIS to transform maps between coordinate systems. In an affine transformation, parallel lines remain parallel,
# the midpoint of a line segment remains a midpoint, and all points on a straight line remain on a straight line.
# # # Seems like it just means to transform maps between coordinate systems, I just don't understand how it works

# More on spatial transformations: http://desktop.arcgis.com/en/arcmap/10.3/manage-data/editing-existing-features/about-spatial-adjustment-transformations.htm
