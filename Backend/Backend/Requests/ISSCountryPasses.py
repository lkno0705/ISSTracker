from Backend.Core.database import redisDB

def _pointOnPolygon(latitude, longitude, polygon):
    # check if point is inside of polygon
    counter = 0  # counts the points of intersections with the polygon
    for i in range(len(polygon)):  # corresponds to for every corner do
        # generate point pairs
        if i+1 == len(polygon):  # checks if we reached the last corner of the polygon
            pointA, pointB = polygon[i], polygon[0]
        else:
            pointA, pointB = polygon[i], polygon[i + 1]

        # Assigning point attributes latitude and longitude
        pointA["longitude"], pointA["latitude"] = float(pointA["longitude"]), float(pointA["latitude"])
        pointB["longitude"], pointB["latitude"] = float(pointB["longitude"]), float(pointB["latitude"])

        # check if the beam of the current coordinate has a point of intersection with the path between pointA and pointB
        if pointA["longitude"] <= longitude or pointB["longitude"] <= longitude:
            if (pointA["latitude"] >= latitude and pointB["latitude"] <= latitude) or (
                    pointB["latitude"] >= latitude and pointA["latitude"] <= latitude):
                counter += 1
    # If the counter is even or if no point of intersection is found then the coordinate is not inside of the polygon
    return False if counter == 0 else counter % 2 != 0


def ISScountryPasses(requestData):

    # get data from DB
    DB = redisDB()
    geoJson = DB.getData(requestData={
        "params": {
            "country": requestData["params"]["country"]
        }
    }, requestName="GeoJson")
    del geoJson["countryname"]
    issCoordinates = DB.getData(requestData={
        "params": {
            "startTime": requestData["params"]["startTime"],
            "endTime": requestData["params"]["endTime"]
        }
    }, requestName="ISSDB")

    # initialize vars
    lastPointOnPolygon = False
    lastTimeValue = ""
    returnValue = {
        "numberOfPasses": 0,
        "passes": []
    }
    returnIndex = -1

    # for every isscoordinate check if its inside the country borders and calculate ISSpasses based upon that information
    for x in range(0, len(issCoordinates), 2):
        # reformat isscoordinates
        if issCoordinates[x].key == "longitude":
            longitude = float(issCoordinates[x].value)
            latitude = float(issCoordinates[x+1].value)
        else:
            latitude = float(issCoordinates[x].value)
            longitude = float(issCoordinates[x+1].value)

        # Count passes and save start- and endTime of every pass
        if not lastPointOnPolygon:
            thisPointOnPolygon = _pointOnPolygon(latitude, longitude, geoJson)  # check if point is on polygon
            if thisPointOnPolygon:
                returnValue["passes"].append({"startTime": issCoordinates[x].timeValue, "endTime": ""})
                returnValue["numberOfPasses"] += 1
                returnIndex += 1
                lastTimeValue = issCoordinates[x].timeValue
        else:
            thisPointOnPolygon = _pointOnPolygon(latitude, longitude, geoJson)
            if not thisPointOnPolygon:
                returnValue["passes"][returnIndex]["endTime"] = lastTimeValue
            else:
                returnValue["passes"][returnIndex]["endTime"] = issCoordinates[x].timeValue
            lastTimeValue = issCoordinates[x].timeValue
        lastPointOnPolygon = thisPointOnPolygon
    return returnValue

# Uncomment for Debugging purposes
# if __name__ == '__main__':
#     print(ISScountryPasses(requestData={
#         "params": {
#             "startTime": "2020-06-15 12-00-00",
#             "endTime": "2020-06-15 23-38-16",
#             "country": "Kazakhstan"
#         }
#     }))