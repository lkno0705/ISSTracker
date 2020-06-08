import redis
from time import time
import datetime
from Backend.Core.dataStructs import parseTimeToTimestamp, ISSDBKey


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


    def _getISS(self, requestData):
        # TODO: Change to StartTime and EndTime Range

        startTime = parseTimeToTimestamp(requestData["params"]["startTime"])
        endTime = parseTimeToTimestamp(requestData["params"]["endTime"])

        keyset = set()
        with self.__redisDB__ as DB:
            searchPattern = "ISSpos" + ":" + requestData["params"]["startTime"].split(" ")[0] + "*"
            startTimeKeys = DB.keys(pattern=searchPattern)
            for key in startTimeKeys:
                splitted = str(key).split(':')
                currKeyObject = ISSDBKey(timeValue=splitted[1], key=splitted[2])
                if currKeyObject.timestamp >= startTime and currKeyObject.timestamp <= endTime:
                    keyset.add(currKeyObject)

            searchPattern = "ISSpos" + ":" + requestData["params"]["endTime"].split(" ")[0] + "*"
            endTimeKeys = DB.keys(pattern=searchPattern)
            for key in endTimeKeys:
                splitted = str(key).split(':')  # [0] = requestName; [1] = timestamp; [2] = param
                currKeyObject = ISSDBKey(timeValue=splitted[1], key=splitted[2])
                if currKeyObject.timestamp >= startTime and currKeyObject.timestamp <= endTime:
                    keyset.add(currKeyObject)

            keylist = sorted(keyset, key=lambda x: x.timestamp)
            print(keylist)





    def setData(self, data):
        # TODO: parse data to python Object
        topLevel = {
            "ISSpos": self._setIsspos,
            "RSS-Feed": "_setRSS"
        }
        topLevel.get(data["requestname"])(data)

    def getData(self, requestData, requestName):
        functions = {
            "ISSpos": self._getISS(requestData)
        }
        return functions.get(requestName)







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
        "params": {
            "startTime": "2020-06-07 13-22-41",
            "endTime": "2020-06-08 13-28-06",
        }
    }
    DB.getData(requestData=datar, requestName="ISSpos")
