import redis
from os import getenv
import time
import datetime
from Backend.Core.dataStructs import parseTimeToTimestamp, ISSDBKey, Astronaut
from Backend.Requests import astrosOnISS
from Backend.Tools.XMLToDic4DB import GeoJsonXMLToDic, ISSPosXMLToISSDBKey
from Backend.Tools.DicToXML4DB import ISSPosISSDBKeyToXML
from Backend.Tools import rssFeedTimeConverter as dateConverter


class redisDB:
    # establishing connection to redisDB
    __redisHost__ = getenv('REDISHOST')  # "ISS-Trackr-API.redis.cache.windows.net"
    __redisPW__ = getenv('REDISPW')
    __redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True, password=__redisPW__)

    # push current ISS postition to DB
    def _setIsspos(self, data):
        # IssPos object (data):
        # {'latitude': -45.4742, 'longitude': 150.3883, 'timestamp': '2020-06-09 20-50-01'}

        with self.__redisDB__ as DB:
            # set Key and Value
            # get list of all ISSPositions
            try:
                oldISSPositions = ISSPosXMLToISSDBKey(DB.get(name="ISSpos"))
            except:
                oldISSPositions = []
            # push current ISSpos into list of all ISSPositions
            oldISSPositions.append(ISSDBKey(timeValue=data["timestamp"], key="longitude", value=data["longitude"]))
            oldISSPositions.append(ISSDBKey(timeValue=data["timestamp"], key="latitude", value=data["latitude"]))

            issPositions = sorted(oldISSPositions, key=lambda x: x.timestamp)

            if datetime.datetime.now().timestamp() - issPositions[0].timestamp > 43200:  # vergleiche timestamps
                del issPositions[0]
                del issPositions[1]

            # push all ISSPositions including the new position into DB as XML
            DB.set(name="ISSpos", value=ISSPosISSDBKeyToXML(issPositions))

    def _getISS(self, requestData):

        # converting Timestamps from requests to actual Timestamps
        startTime = parseTimeToTimestamp(requestData["params"]["startTime"])
        endTime = parseTimeToTimestamp(requestData["params"]["endTime"])

        # define empty Key set (mathematische Menge)
        keyset = set()

        with self.__redisDB__ as DB:

            # Generating search pattern from request parameters
            searchPattern = "ISSpos" + ":" + requestData["params"]["startTime"].split(" ")[0] + "*"

            # Get all keys from DB which match previously defined keyset
            Data = DB.get("ISSpos")

            Data = ISSPosXMLToISSDBKey(Data)

            # add keys to keyset
            for key in Data:

                # only add keys which are in the range of [startTime, endTime]
                if key.timestamp >= startTime and key.timestamp <= endTime:
                    # adding key to keyset
                    keyset.add(key)

            # # same code as for startTime -> see comments above for explanations
            # searchPattern = "ISSpos" + ":" + requestData["params"]["endTime"].split(" ")[0] + "*"
            # endTimeKeys = DB.keys(pattern=searchPattern)
            # for key in endTimeKeys:
            #     splitted = str(key).split(':')  # [0] = requestName; [1] = timestamp; [2] = param
            #     currKeyObject = ISSDBKey(timeValue=splitted[1], key=splitted[2].strip("'"), value=None)
            #     if currKeyObject.timestamp >= startTime and currKeyObject.timestamp <= endTime:
            #         keyset.add(currKeyObject)

            # convert keyset into a sorted list, sorted by timestamps
            keylist = sorted(keyset, key=lambda x: x.timestamp)
            return keylist

    def _getGeoJsonSingel(self, countryname):
        with self.__redisDB__ as DB:
            # get keys
            xml = DB.get("GeoJson:" + countryname)

            returnValue = GeoJsonXMLToDic(xml)
            return returnValue

    def _getGeoJson(self, requestdata):
        with self.__redisDB__ as DB:

            if not requestdata["params"]["country"] == "all":
                return self._getGeoJsonSingel(countryname=requestdata["params"]["country"])
            else:
                # initialize return dict
                returnValue = []

                # get all countrys from DB
                startTime = time.time()
                print("Getting Data from DB")
                keys = DB.keys("GeoJson:*")
                countryset = set()
                for i in range(len(keys)):
                    countryset.add(str(keys[i]).split(":")[1])

                # get GeoJson for every country
                lastTime = startTime
                for country in countryset:
                    returnValue.append(self._getGeoJsonSingel(countryname=country))
                    print("Got Value in: ", time.time() - lastTime, " seconds")
                    lastTime = time.time()

                print("Done in: ", time.time() - startTime, " seconds")
                return returnValue

    def _getAstros(self, requestData):
        astros = astrosOnISS.getAstrosOnISS()
        astrosWithItems = []
        with self.__redisDB__ as DB:
            for i in range(len(astros)):
                # get picture,flag and nation of current astro
                picture = DB.get("Astronaut:" + astros[i] + ":" + 'picture')
                flag = DB.get("Astronaut:" + astros[i] + ":" + 'flag')
                nation = DB.get("Astronaut:" + astros[i] + ":" + 'nation')
                # assign these items to current astronaut
                astrosWithItems.append(Astronaut(name=astros[i], pic=picture, flag=flag, nation=nation))
            return astrosWithItems

    def _setRssFeed(self, data):
        feedItems = data['items']
        id = 0
        for i in range(len(feedItems)):
            expireTime = 3600  # expiration time in seconds: 3600sec = 1H
            firstKeyPart = "RSS-Feed:" + str(id)
            self.__redisDB__.set(name=firstKeyPart + ":title", value=feedItems[i]['title'])
            self.__redisDB__.set(name=firstKeyPart + ":summary", value=feedItems[i]['summary'])
            self.__redisDB__.set(name=firstKeyPart + ":published", value=feedItems[i]['published'])
            self.__redisDB__.set(name=firstKeyPart + ":link", value=feedItems[i]['link'])
            id += 1

    def _getRssFeed(self, requestData):
        requestIds = (requestData['params']['startID'], requestData['params']['endID'])
        keys = self.__redisDB__.keys("RSS-Feed:*")
        items = []
        idset = set()
        for key in keys:
            keyElements = key.split(':')
            # read publishing date out of key
            id = keyElements[1]
            # check if number of rssfeeds wished is not exceeded and this rssFeed published before the getRequest was done
            if len(items) < (int(requestIds[1]) - int(requestIds[0])) and int(requestIds[0]) <= int(id) < int(
                    requestIds[1]):
                idset.add(id)

        for ids in idset:
            items.append({'title': self.__redisDB__.get("RSS-Feed:" + ids + ':title'),
                          'summary': self.__redisDB__.get("RSS-Feed:" + ids + ':summary'),
                          'published': self.__redisDB__.get("RSS-Feed:" + ids + ':published'),
                          'link': self.__redisDB__.get("RSS-Feed:" + ids + ':link')})

        items = sorted(items, key=lambda i: (i['published']), reverse=True)
        return items

    def getCountryList(self, requestData):
        with self.__redisDB__ as DB:
            # get all countrys from DB
            keys = DB.keys("GeoJson:*")
            countryset = set()
            for i in range(len(keys)):
                countryset.add(str(keys[i]).split(":")[1])

            return countryset

    def setData(self, data, requestname):
        # switch case for requestnames -> call correct function for every request
        topLevel = {
            "ISSpos": self._setIsspos,
            "RSS-Feed": self._setRssFeed
        }
        topLevel.get(requestname)(data)

    def getData(self, requestData, requestName):
        # switch case for requestnames -> call correct function for every request
        functions = {
            "ISSDB": self._getISS,
            "GeoJson": self._getGeoJson,
            "AstrosOnISS": self._getAstros,
            "RSS-Feed": self._getRssFeed,
            "CountryList": self.getCountryList
        }
        return functions.get(requestName)(requestData)

# Comment out for Debugging purposes
# if __name__ == '__main__':
#     data = {
#         'latitude': -45.4742,
#         'longitude': 150.3883,
#         'timestamp': '2020-06-09 20-50-01'
#     }
#     DB = redisDB()
#     DB.setData(data=data, requestname="ISSpos")
#
#     datar = {
#         "params": {
#             "startTime": "2020-06-09 20-50-01",
#             "endTime": "2020-06-09 21-50-10",
#         }
#     }
#     print(DB.getData(requestData=datar, requestName="ISSDB"))

# if __name__ == '__main__':
#     DB = redisDB()
#     data = {
#         "params": {
#             "country": "all"
#         }
#     }
#     print(DB.getData(data, "GeoJson"))

# if __name__ == '__main__':
#     DB = redisDB()
#     data = {}
#     print(DB.getData(requestData=data, requestName="AstrosOnISS"))
