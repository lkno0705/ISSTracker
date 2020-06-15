from Backend.Core.database import redisDB

def _pointOnPolygon(latitude, longitude, polygon):
    # check if point is inside of polygon
    counter = 0
    for i in range(len(polygon)):
        if i+1 == len(polygon):
            pointA, pointB = polygon[str(i)], polygon[str(0)]
        else:
            pointA, pointB = polygon[str(i)], polygon[str(i + 1)]
        pointA["longitude"], pointA["latitude"] = float(pointA["longitude"]), float(pointA["latitude"])
        pointB["longitude"], pointB["latitude"] = float(pointB["longitude"]), float(pointB["latitude"])
        if pointA["longitude"] <= longitude or pointB["longitude"] <= longitude:
            if (pointA["latitude"] >= latitude and pointB["latitude"] <= latitude) or (
                    pointB["latitude"] >= latitude and pointA["latitude"] <= latitude):
                counter += 1
    return False if counter == 0 else counter % 2 == 0

def ISScountryPasses(requestData):
    DB = redisDB()
    geoJson = DB.getData(requestData={
        "params": {
            "country": requestData["params"]["country"]
        }
    }, requestName="GeoJson")
    del geoJson["countryname"]
    print(geoJson)
    issCoordinates = DB.getData(requestData={
        "params": {
            "startTime": requestData["params"]["startTime"],
            "endTime": requestData["params"]["endTime"]
        }
    }, requestName="ISSDB")



    for x in range(0, len(issCoordinates), 2):
        if issCoordinates[x].key == "longitude":
            longitude = float(issCoordinates[x].value)
            latitude = float(issCoordinates[x+1].value)
            # print("ISS: ", issCoordinates[x].key, longitude, issCoordinates[x + 1].key, latitude)
        else:
            latitude = float(issCoordinates[x].value)
            longitude = float(issCoordinates[x+1].value)
            # print("ISS: ",issCoordinates[x].key, latitude, issCoordinates[x+1].key, longitude)
        print(_pointOnPolygon(latitude, longitude, geoJson))






ISScountryPasses(requestData={
    "params": {
        "startTime": "2020-06-15 12-00-00",
        "endTime": "2020-06-15 13-00-00",
        "country": "Kazakhstan"
    }
})