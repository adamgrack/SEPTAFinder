import zipfile
import os
import fiona
import pandas as pd
import geopandas as gpd
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt


# setup file path for kmz file extraction
kmz_file_path = "C:/Users/grayh/NETCoreApps/SEPTAFinder/Data/SEPTARegionalRailStations2016.kmz"
extraction_dir = os.path.dirname("C:/Users/grayh/NETCoreApps/SEPTAFinder/Data/SEPTARegionalRailStations2016.kmz")

with zipfile.ZipFile(kmz_file_path, "r") as kmz:
    kmz.extractall(extraction_dir)

# setup fiona reading permissions
fiona.drvsupport.supported_drivers['libkml'] = 'rw' 
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

# grab kml filepath and hold as a global for use in getting the locations of septa stops
fp = "C:/Users/grayh/NETCoreApps/SEPTAFinder/Data/doc.kml"

# use file reader to read each septa location and save to an array
def getSeptaLocations()->gpd.GeoDataFrame:
    for layer in fiona.listlayers(fp):
        gdf = gpd.read_file(fp, driver='LIBKML', layer=layer)
  
    return gdf

# using haversine formula for finding the distance between points
def distance(lat1, long1, lat2, long2)->float:
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    dlong = long2-long1
    dlat = lat2-lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlong/2)**2
    c = 2 * asin(sqrt(a)) 

    km = 6371 * c
    return km

# return the location of the closest septa station
def determineClosestStation(listOfLocations: gpd.GeoDataFrame, location = []):
    closestLocation = []
    listOfLocations.value
    for septaStops in listOfLocations['geometry']:
        closestLocation = septaStops if distance(septaStops[0], septaStops[1], location[0], location[1]) < distance(closestLocation[0], closestLocation[1], location[0], location[1]) else closestLocation

    return closestLocation

def FindClosestSepta (location = []):
    septaList: gpd.GeoDataFrame 
    septaList = getSeptaLocations()
    print(septaList.loc[0])

    #return determineClosestStation(septaList, location)

latLong = ["41.205", "24.202"]

location = FindClosestSepta(latLong)