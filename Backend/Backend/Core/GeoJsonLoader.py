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

def loadGeoJsonsToDB(geoJson):
    countryList = GeoJsonToXML(geoJson)
    for country in countryList:
        # loads every xml string of countries coordinates into DB
        __redisDB__.set(name="GeoJson:" + country['countryname'], value=country['xml'])
        # print(country['countryname']+"\n")
        # print(country['xml']+"\n"+"\n"+"\n")
        sleep(0.01)

process()
