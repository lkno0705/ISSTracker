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

    def _parseTimeToTimestamp(self, time):
        date, time = time.split(" ")
        date = date.split("-")
        time = time.split("-")
        timeTupel = (int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
        timestamp = datetime.datetime(year=timeTupel[0],
                                      month=timeTupel[1],
                                      day=timeTupel[2],
                                      hour=timeTupel[3],
                                      minute=timeTupel[4],
                                      second=timeTupel[5]).timestamp()
        return timestamp

    def _getISS(self, requestData):
        # TODO: Change to StartTime and EndTime Range

        startTime = self._parseTimeToTimestamp(requestData["params"]["startTime"])
        endTime = self._parseTimeToTimestamp(requestData["params"]["endTime"])

        with self.__redisDB__ as DB:

            searchPattern = "ISSpos" + ":" + requestData["params"]["startTime"].split(" ")[0] + "*"
            startTimeKeys = DB.keys(pattern=searchPattern)
            for i in range(len(startTimeKeys)):
                startTimeKeys[i] = str(startTimeKeys[i]).split(':')  # [0] = requestName; [1] = timestamp; [2] = param
                del startTimeKeys[i][0]

            searchPattern = "ISSpos" + ":" + requestData["params"]["endTime"].split(" ")[0] + "*"
            endTimeKeys = DB.keys(pattern=searchPattern)
            for i in range(len(endTimeKeys)):
                endTimeKeys[i] = str(endTimeKeys[i]).split(':')  # [0] = requestName; [1] = timestamp; [2] = param
                del endTimeKeys[i][0]

            for i in range(len(startTimeKeys)):
                offset = 0
                startTimeKeys[i].append(self._parseTimeToTimestamp(startTimeKeys[i][0]))
                for x in range(len(endTimeKeys)):
                    if startTimeKeys[i][0] == endTimeKeys[x-offset][0]:
                        del endTimeKeys[x-offset]
                        offset += 1
                    elif len(endTimeKeys[x-offset]) < 3:
                        endTimeKeys[x-offset].append(self._parseTimeToTimestamp(endTimeKeys[x-offset][0]))
                        startTimeKeys.append(endTimeKeys[x-offset])

            print(startTimeKeys)






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
