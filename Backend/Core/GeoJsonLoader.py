import json
from time import sleep

import redis

__redisHost__ = "localhost"
__redisDB__ = redis.Redis(host=__redisHost__, port=6379, db=0)


# enter path of your json File for "path"
def getPath():
    path = r"/mnt/c/users/lkno0/Documents/ISSTracker/Frontend/json/word_low_res.json"
    return path


def process():
    path = getPath()
    file = open(path)
    data = json.load(file)
    loadGeoJsonsToDB(data)
    file.close()


def loadGeoJsonsToDB(data):
    data = data
    countries = data['features']
    for e in range(len(countries)):
        countryName = data['features'][e]['properties']['sovereignt']
        coordinates = data['features'][e]['geometry']['coordinates']
        checkTuples(coordinates, countryName)


def checkTuples(list, countryName):
    # if list[0] has to elements, list's elements are tuples of coordinates
    if (len(list[0]) == 2):
        pushIntoDB(countryName, list)
    else:
        # for every element of list, check if list's elements are tuples of coordinates or tuples of States/Regions/etc.
        for i in range(len(list)):
            checkTuples(list[i], countryName)


# awaits tuples of longitude and latitude for elements of "coordinates"
def pushIntoDB(countryName, coordinates):
    for i in range(len(coordinates)):
        print("GeoJson:" + countryName + ":" + str(i) + ":latitude")
        # loads every tuple's longitude and latitude into DB
        __redisDB__.set(name="GeoJson:" + countryName + ":" + str(i) + ":latitude", value=coordinates[i][0])
        __redisDB__.set(name="GeoJson:" + countryName + ":" + str(i) + ":longitude", value=coordinates[i][1])
        sleep(0.01)


process()
