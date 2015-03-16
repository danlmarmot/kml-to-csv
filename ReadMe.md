# KML to POI

Written for Python 3.4 or greater
Designed to be used with Garmin POI Loader and custom POI icons
Read up at icon requirements at http://www8.garmin.com/products/poiloader/creating_custom_poi_files.jsp

Custom BMP icons should be placed in the /bmp folder, and will be copied to the appropriate output folder if present

To create a custom POI file, run the POI Loader application, and point it at the "output" folder.   POI Loader will
scan all folders and subfolders to create its single POI file, which will have a gpi extension.