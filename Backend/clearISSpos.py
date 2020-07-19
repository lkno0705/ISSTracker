import redis
from os import getenv
from Backend.Tools.XMLToDic4DB import GeoJsonXMLToDic, ISSPosXMLToISSDBKey
from Backend.Core.dataStructs import parseTimeToTimestamp, ISSDBKey, Astronaut
__redisHost__ = getenv('REDISHOST')  # "ISS-Trackr-API.redis.cache.windows.net"
__redisPW__ = getenv('REDISPW')
__redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True, password=__redisPW__)
import datetime


with __redisDB__ as DB:
    # set Key and Value
    # get list of all ISSPositions
    DB.set(name="ISSpos", value="")