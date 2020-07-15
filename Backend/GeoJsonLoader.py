import json
from time import sleep
from os import getenv
import redis
from Backend.Tools.DicToXML4DB import GeoJsonToXML

__redisHost__ = getenv('REDISHOST')  # "ISS-Trackr-API.redis.cache.windows.net"
__redisPW__ = getenv('REDISPW')
__redisDB__ = redis.Redis(host=__redisHost__, port=6379, db=0, password=__redisPW__)


# enter path of your json File for "path"
def getPath():
    path = r"./custom.geo_lowres.json"
    return path


def process():
    path = getPath()
    file = open(path)
    data = json.load(file)
    loadGeoJsonsToDB(data)
    file.close()


# def process():
#     path = getPath()
#     file = open(path)
#     data = json.load(file)
#     loadGeoJsonsToDB(data)
#     file.close()


# def loadGeoJsonsToDB(data):
#     data = data
#     countries = data['features']
#     for e in range(len(countries)):
#         countryname = data['features'][e]['properties']['sovereignt']
#         coordinates = data['features'][e]['geometry']['coordinates']
#         checkTuples(coordinates, countryname)
#
#
# def checkTuples(list, countryname):
#     # if list[0] has to elements, list's elements are tuples of coordinates
#     if (len(list[0]) == 2):
#         pushIntoDB(countryname, list)
#     else:
#         # for every element of list, check if list's elements are tuples of coordinates or tuples of States/Regions/etc.
#         for i in range(len(list)):
#             checkTuples(list[i], countryname)


# awaits tuples of longitude and latitude for elements of "coordinates"
# def pushIntoDB(countryname, coordinates):
#     for i in range(len(coordinates)):
#         print("GeoJson:" + countryname + ":" + str(i) + ":latitude")
#         # loads every tuple's longitude and latitude into DB
#         __redisDB__.set(name="GeoJson:" + countryname + ":" + str(i) + ":latitude", value=coordinates[i][0])
#         __redisDB__.set(name="GeoJson:" + countryname + ":" + str(i) + ":longitude", value=coordinates[i][1])
#         sleep(0.01)
#

def loadGeoJsonsToDB(geoJson):
    countryList = GeoJsonToXML(geoJson)
    for country in countryList:
        # loads every xml string of countries coordinates into DB
        __redisDB__.set(name="GeoJson:" + country['countryname'], value=country['xml'])
        # print(country['countryname']+"\n")
        # print(country['xml']+"\n"+"\n"+"\n")
        sleep(0.01)

process()
