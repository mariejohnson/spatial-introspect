# spatial-introspect
 
The ultimate goal of this project is to provide users of [dataone](https://www.dataone.org/) with a streamlined method of uploading spatial data. Currently users have to specify the coordinates of their data's bounding box corners. To do this accurately, users generally need to open up the dataset in a GIS package and manually copy over the corner coordinates of window. This is a time consuming process that probably makes people mutter oaths under their breath.

So, in order to make life easier for data uploaders, we'd like to look at files that have been uploaded and do the following:

1. Check if it's a spatial data type. If it is:
  1. See if it's vector or raster. Handle it with fiona if it's a vector and get it's bounding coordinates. Handle with rasterio if it's a raster and get it's bounding coordinates.
2. If it's not a spatial type but it is a csv, try to figure out if it represents point data.
3. If none of the above raise an exception.

The first step of development will just be to write a function that takes a single file path as input and runs through the steps outlined above. We'll worry about integrating it with dataone later.
