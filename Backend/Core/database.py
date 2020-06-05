import redis
from time import time
import datetime

class redisDB:
    __redisHost__ = "localhost"
    __redisDB__ = redis.Redis(host=__redisHost__, port=6379, db=0)

    def _setIsspos(self, data):
        # IssPos object (data):
        # {
        #   "requestname": "ISSpos",
        #   "data":{
        #       "timestamp":"2012-12-15 01:21:05",
        #       "latitude": "-17.9617",
        #       "longitude": "162.6117"
        #   }
        # }
        with self.__redisDB__ as DB:
            DB.set(name="ISSpos:" + data["data"]["timestamp"] + ":latitude", value=data["data"]["latitude"])
            DB.set(name="ISSpos:" + data["data"]["timestamp"] + ":longitude", value=data["data"]["longitude"])
            DB.set(name="ISSpos:" + data["data"]["timestamp"] + ":timestamp", value=data["data"]["timestamp"])
            DB.expire(name="ISSpos:" + data["data"]["timestamp"], time=86400)  # key expires after 24h

    def setData(self, data):
        # TODO: parse data to python Object
        topLevel = {
            "ISSpos": self._setIsspos,
            "RSS-Feed": "_setRSS"
        }
        topLevel.get(data["requestname"])(data)

    def getData(self, data, n=1):
        # data has to be an correctly formatted XML with an empty data Tag:
        # <?xml version="1.0" encoding="UTF-8"?>
        # <Request>
        #    <requestName>ISS-Pos</requestName>
        #    <data>
        #    </data>
        # </Request>
        #
        # TODO: parse data to python Object
        with self.__redisDB__ as DB:
            keys = DB.keys(pattern="ISSpos:*")
        print(keys)


if __name__ == '__main__':
    data = {
        "requestname": "ISSpos",
        "data": {
            "latitude": 1234,
            "longitude": 1234,
            "timestamp": datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H-%M-%S')
        }
    }
    DB = redisDB()
    DB.setData(data=data)

    datar = {
        "requestname": "ISSpos",
    }
    DB.getData(datar, n=2)
