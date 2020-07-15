import math
import pytz
from datetime import datetime, timedelta
from Backend.Core.database import redisDB


class pastPasses():

    def _degreesToRadians(self, degrees):
        return degrees * math.pi / 180

    def _distanceInKmBetweenEarthCoordinates(self, coord1, coord2):
        earthRadiusKm = 6371

        dLat = self._degreesToRadians(coord2[0] - coord1[0])
        dLon = self._degreesToRadians(coord2[1] - coord1[1])

        lat1 = self._degreesToRadians(coord1[0])
        lat2 = self._degreesToRadians(coord2[0])

        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(
            lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return earthRadiusKm * c

    def pastPasses(self, requestData):
        location = (float(requestData["params"]['latitude']), float(requestData["params"]['longitude']))

        tzUTC = pytz.timezone('UTC')
        currentTime = datetime.now(tz=tzUTC)
        endTime = currentTime - timedelta(hours=24)

        db = redisDB()

        issCoordinates = db.getData(
            {"params": {
                "endTime": currentTime.strftime("%Y-%m-%d %H-%M-%S"),
                "startTime": endTime.strftime("%Y-%m-%d %H-%M-%S")
            }
            }, "ISSDB")

        lastPointInCircle = False
        lastTimeValue = ""
        returnValue = {
            "numberOfPasses": 0,
            "passes": []
        }
        returnIndex = -1

        for x in range(0, len(issCoordinates), 2):
            # reformat isscoordinates
            if issCoordinates[x].key == "longitude":
                coord1 = (float(issCoordinates[x + 1].value), float(issCoordinates[x].value))
            else:
                coord1 = (float(issCoordinates[x].value), float(issCoordinates[x + 1].value))

            thisPointInCircle = self._distanceInKmBetweenEarthCoordinates(coord1=coord1, coord2=location) <= int(requestData["params"]["radius"])
            if not lastPointInCircle and thisPointInCircle:
                returnValue["passes"].append({"startTime": issCoordinates[x].timeValue, "endTime": ""})
                returnValue["numberOfPasses"] += 1
                returnIndex += 1
                lastTimeValue = issCoordinates[x].timeValue
                if len(issCoordinates) - 1 == x or len(issCoordinates) - 2 == x:
                    returnValue["passes"][returnIndex]["endTime"] = issCoordinates[x].timeValue
            elif lastPointInCircle:
                if not thisPointInCircle:
                    returnValue["passes"][returnIndex]["endTime"] = lastTimeValue
                else:
                    returnValue["passes"][returnIndex]["endTime"] = issCoordinates[x].timeValue
                lastTimeValue = issCoordinates[x].timeValue
            lastPointInCircle = thisPointInCircle
        return returnValue


# data = {
#     "params": {
#         "latitude": -2.1496,
#         "longitude": -96.0077,
#         "radius": 50
#     }
# }
# print(pastPasses().pastPasses(data))