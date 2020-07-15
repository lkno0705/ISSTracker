import redis
from os import getenv
# establishing connection to redisDB
__redisHost__ = getenv('REDISHOST')  # "ISS-Trackr-API.redis.cache.windows.net"
__redisPW__ = getenv('REDISPW')
__redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True, password=__redisPW__)

with __redisDB__ as DB:
    keys = DB.keys("ISSpos*")

    for key in keys:
        DB.delete(key)
        print("deleted: ", key)

    print("\n\n Finished Keys Remaining: ", len(DB.keys("ISSpos*")))