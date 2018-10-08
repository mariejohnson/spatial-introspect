# This is code that was taken out because I either found a better way to write it or didn't need it anymore


shp_fn = "/Users/datateam/repos/spatial_introspect/test_data/HerdSpatialDistribution/HerdSpatialDistribution.shp"

def get_extent_for_vector(shapefile):
    lats = []
    lons = []
    with fiona.open(shapefile, 'r') as src:
        for feat in src:
            # if ['geometry'] is not type Point:
            #     raise MyException('Point data') look at formatting here: https://github.com/Toblerity/Fiona/blob/master/fiona/transform.py
            # work on this later, work on transforming first
            coords = feat['geometry']['coordinates'][0] # stop the debugger on this line, and see what's inside `feat` to see the values I'm after
            [(lons.append(x), lats.append(y)) for x, y in coords] # this will make it so that it only shows the bounding box vs the whole list (.append) - or something like that
            # transform('EPSG:4326', 'EPSG:4326', xs=lons, ys=lats) # this might need to be x, y
            #print(lats, lons)

    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)
    print('South extent: {}\nNorth extent: {}\nWest extent: {}\nEast extent: {}'.format(min_lat,
                                                                                        max_lat,
                                                                                        min_lon,
                                                                                        max_lon))
get_extent_for_vector(shp_fn)


bounds1 = RasterBounds(raster=CA_rast)
print(bounds1)



# this also needs to be RasterBounds
def get_extent_raster(raster):
    with rasterio.open(raster, 'r') as ds:
        #ds.features.bounds(geometry = polygon, north_up = True, transform = None)
        print(ds.bounds) # need to transform and probably do return here instead of print
        print(ds.meta) #gets more info about the raster

get_extent_for_raster(NM_rast)



def check_ext_2(file_name):
    class MyException(Exception):
        pass
    pat = re.compile(r'lat')
    for file in file_name:
        if pat.findall(file) is True:
            print(file)
        else:
            raise MyException("incorrect format")
    #return results

csv_string = "lat"

check_ext_2(csv_string)

