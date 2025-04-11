import zipfile
import os
import json
import fiona
import shapely
import pandas as pd
import geopandas as gpd
from bs4 import BeautifulSoup
from math import radians, cos, sin, asin, sqrt


# setup file path for kmz file extraction
kmz_file_path = "./Data/SEPTARegionalRailStations2016.kmz"
extraction_dir = os.path.dirname("./Data/SEPTARegionalRailStations2016.kmz")

with zipfile.ZipFile(kmz_file_path, "r") as kmz:
    kmz.extractall(extraction_dir)

# setup fiona reading permissions
fiona.drvsupport.supported_drivers['libkml'] = 'rw' 
fiona.drvsupport.supported_drivers['LIBKML'] = 'rw'

# grab kml filepath and hold as a global for use in getting the locations of septa stops
fp = "./Data/doc.kml"

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

# take geodataframe and comparative point
# return dictionary of the closest point
def determineClosestStation(listOfLocations: gpd.GeoDataFrame, location: shapely.Point):
    # defaulting values to the first in list so there is not a chance of a default that isn't on the list being closest to the input point
    closestLocation = {
        "Name": listOfLocations.loc[0, 'Name'],
        "Description": listOfLocations.loc[0, 'Description'],
        "geometry": listOfLocations.loc[0, 'geometry']
    }
    locationPoint: shapely.Point
    
    for septaStops in listOfLocations.iterrows():
        locationPoint = septaStops[1]['geometry']
        closestLocation = ({"Name": septaStops[1]['Name'], "Description": septaStops[1]['Description'], "geometry": septaStops[1]['geometry']} if distance(locationPoint.x, locationPoint.y, location.x, location.y) <
            distance(closestLocation["geometry"].x, closestLocation["geometry"].y, location.x, location.y) else closestLocation)
    
    return closestLocation

def main (location: shapely.Point):
    septaList: gpd.GeoDataFrame 
    septaList = getSeptaLocations()

    return determineClosestStation(septaList, location)

latLong = shapely.Point(-74.205, 44.202)

location = main(latLong)