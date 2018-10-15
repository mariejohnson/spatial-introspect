'''

https://www.youtube.com/watch?v=N_dmiQI1s24&t=2s
his blog: https://medium.com/@robsimmon
- has more examples

General notes:
- geotif is just a normal tif but has a header ont with with information so we can precisely place every single pixel on an image to a precise coordinate on the earth's surface
- GDAL is working with things that are directly tied to real positions on a 3D surface
- GDAL is a great tool for moving between different projections
- spatialreference.org
- Proj4 is a convenient, reliable format.
- proj4 = +proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs which can be found here: http://spatialreference.org/ref/sr-org/7099/proj4/


Terminal
# get info about the geotiff
gdalinfo /Users/datateam/Desktop/test_data/NE1_50M_SR/NE1_50M_SR.tif -mm

# Change formats and resize imagines with gdal_translate
- goes from hundreds of different data formats into whatever data format you want
gdal_translate -of JPEG -co QUALITY=90 -outsize 1920 0 -r bilinear CANYrelief1-geo.tif CANYrelief1.jpg
-of = output format (ex: JPEG)
-co = creation option: specific to each individual file format
QUALITY = jpeg quality from 0-100
outsize = in this case is in pixels (1920 great for HD display) didn't specify height (0) GDAL will keep aspect ration if you set either height or width
-r = resampling method (biliear is a nice way to do smooth, nearest neighbor which gives stair steps and looks terrible)
input file
output file

# Change Map Projection with gdalwarp
gdalwarp -t_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS4 +units=m +no_defs'
-r lanczos -dstalpha
-wo SOURCE_EXTRA=1000 -co COMPRESS=LZW NE1_50M_SR_W_tenth.tif NE1_50M_SR_W_tenth_mollweide.tif
Note: mollweide is a projection and I think it is WGS84

-t_srs = target spatial reference system
"proj = moll" = projection
+lon_0=0 +x_0=0 +y_0=0 = the center of the map (I'm not actually sure if the x and y also do that)

Need both -s_srs and -t_srs to reproject:
Dave says this has a lot of flags in it like -t_srs and -wo each adds more complexity
gdalwarp -s_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS4 +units=m
+no_defs' -t_srs '+proj=utm +zone=12 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' -r lanczos -dstalpha
-wo SOURCE_EXTRA=1000 -co COMPRESS=LZW NE1_50M_SR_W_tenth.tif NE1_50M_SR_W_tenth_mollweide.tif

Simpler example:
documentation:
gdalwarp -s_srs [proj4] -t_srs [proj4] [input file] [output file]
Example
gdalwarp -s_srs '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS4 +units=m +no_defs' t_srs
'+proj=utm +zone=12 +ellps=WGS84 +datum=WGS84 +units=m +no_defs' NE1_50M_SR_W_tenth.tif NE1_50M_SR_W_tenth_mollweide.tif

Simpler gdal_translate
example:
gdal_translate -of VRT -projwin -180 -60 180 -90 NE1_50M_SR_W_tenth.tif NE1_50M_SR_W_SH60.vrt
my attempt:
gdal_translate -projwin -180 -60 180 -90 /Users/datateam/Desktop/test_data/NE1_50M_SR/NE1_50M_SR.tif /Users/datateam/Desktop/test_data/NE1_50M_SR/NE1_50M_SR_clipped.tif
worked!

gdal_translate -projwin -109.248047 31.203405 -102.810059 37.212832 /Users/datateam/Desktop/test_data/NE1_50M_SR/NE1_50M_SR.tif /Users/datateam/Desktop/test_data/NE1_50M_SR/NE1_50M_SR_NM.tif
did not work

'''

'''
https://medium.com/planet-stories/a-gentle-introduction-to-gdal-part-2-map-projections-gdalwarp-e05173bd710a
Another example using the shapefile he uses
Shrinking file:
gdal_translate -r lanczos -tr 0.1 0.1  -co COMPRESS=LZW /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W.tif /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_tenth.tif
-tr 0.1 0.1 sets target resolution in real world units

Mercator
gdalwarp -t_srs EPSG:3395 -r lanczos -wo SOURCE_EXTRA=1000 -co COMPRESS=LZW /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_tenth.tif /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_tenth_mercator.tif
gdalwarp invokes the command
while -t_srs EPSG:3395 sets the target source reference system to EPSG:3395, which is the catalog number for Mercator (spatialreference.org)
- r lanczos defines resampling method: lanczos is slow but high quality
-wo SOURCE_EXTRA=1000 is the warp option: advanced parameters that determine how the reporjection is caculated. It adds a buffer of pixels around the map as it is projected, helps prevent gaps in the output, not all projectiosn require it be on safe side
-co COMPRESS-LZW image is saved with LZW a type of lossless compression
input
output

Mollweide


'''

'''
My attempt on resizing
BB CA (I think)
-126 43 -113 31

gdal_translate -projwin -126 43 -113 31 /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_tenth.tif /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_tenth_CA.tif
worked

gdal_translate -projwin -126 43 -113 31 /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W.tif /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_CA.tif
worked

gdal_translate -r lanczos -co COMPRESS=LZW -projwin -126 43 -113 31 /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W.tif /Users/datateam/Desktop/test_data/NE1_50M_SR_W/NE1_50M_SR_W_CA_2.tif
woohoo!
'''