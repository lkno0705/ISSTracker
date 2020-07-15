import json
from xml.etree.ElementTree import Element, ElementTree
from xml.etree.ElementTree import tostring


# preprocessing for parsing GeoJsons
def processJson(data):
    countries = data['features']
    list = []
    for e in range(len(countries)):
        countryname = data['features'][e]['properties']['sovereignt']
        coordinates = data['features'][e]['geometry']['coordinates']
        country = {'countryname': countryname}
        if len(coordinates[0][0]) == 2:
            for i in range(len(coordinates[0])):
                country[i] = {'longitude': coordinates[0][i][0], 'latitude': coordinates[0][i][1]}
            list.append(country)
        else:
            regionslist = []
            for f in range(len(coordinates)):
                region = {}
                for i in range(len(coordinates[f])):
                    for j in range(len(coordinates[f][i])):
                        region[j] = {'longitude': coordinates[f][i][j][0], 'latitude': coordinates[f][i][j][1]}
                regionslist.append(region)
                country["regions"] = regionslist
            list.append(country)
    return list


def GeoJsonToXML(requestData):
    countryList = processJson(requestData)
    countriesinXMLList = []
    for country in countryList:
        countryChild = Element('country')
        countryChild.attrib = {'countryname': country['countryname']}

        if "regions" in country:
            for region in country["regions"]:
                for coord in region:
                    pointChild = Element("point")
                    latChild = Element("latitude")
                    latChild.text = str(region[coord]['latitude'])
                    longChild = Element("longitude")
                    longChild.text = str(region[coord]['longitude'])
                    pointChild.append(longChild)
                    pointChild.append(latChild)
                    countryChild.append(pointChild)
            countriesinXMLList.append(
                {'countryname': country['countryname'], 'xml': tostring(countryChild).decode(encoding="utf-8")})
        else:
            for coord in country:
                if coord == "countryname":
                    continue;
                pointChild = Element("point")
                latChild = Element("latitude")
                latChild.text = str(country[coord]['latitude'])
                longChild = Element("longitude")
                longChild.text = str(country[coord]['longitude'])
                pointChild.append(longChild)
                pointChild.append(latChild)
                countryChild.append(pointChild)
            countriesinXMLList.append(
                {'countryname': country['countryname'], 'xml': tostring(countryChild).decode(encoding="utf-8")})

    return countriesinXMLList


# awaits list of longitude and latitude for "Position"
def ISSPosISSDBKeyToXML(Positions):
    elem = Element('Request')
    requestChild = Element('requestName')
    requestChild.text = 'ISSPos'
    dataChild = Element('data')
    for i in range(0, len(Positions), 2):
        positionChild = Element('isspos')
        timeChild = Element('time')
        timeChild.text = Positions[i].timeValue
        positionChild.append(timeChild)
        if Positions[i].key == 'longitude':
            longChild = Element(Positions[i].key)
            longChild.text = str(Positions[i].value)
            latChild = Element(Positions[i + 1].key)
            latChild.text = str(Positions[i + 1].value)
        else:
            latChild = Element(Positions[i].key)
            latChild.text = str(Positions[i].value)
            longChild = Element(Positions[i + 1].key)
            longChild.text = str(Positions[i + 1].value)
        positionChild.append(longChild)
        positionChild.append(latChild)
        dataChild.append(positionChild)
    elem.append(requestChild)
    elem.append(dataChild)

    return tostring(elem)


def DicToXMLForCounties(requestData):
    elem = Element('Request')
    requestChild = Element('requestName')
    requestChild.text = 'GeoJson'

    dataChild = Element('data')
    countriesElem = Element('countries')

    for country in requestData:
        countryChild = Element('country')
        countryChild.attrib = {'countryname': country['countryname']}

        if "regions" in country:
            for region in country["regions"]:
                regionChild = Element("region")
                for coord in region:
                    pointChild = Element("point")
                    latChild = Element("latitude")
                    latChild.text = str(region[coord]['latitude'])
                    longChild = Element("longitude")
                    longChild.text = str(region[coord]['longitude'])
                    pointChild.append(longChild)
                    pointChild.append(latChild)
                    regionChild.append(pointChild)
                countryChild.append(regionChild)
            countriesElem.append(countryChild)
        else:
            regionChild = Element("region")
            for coord in country:
                if coord == "countryname":
                    continue;
                pointChild = Element("point")
                latChild = Element("latitude")
                latChild.text = str(country[coord]['latitude'])
                longChild = Element("longitude")
                longChild.text = str(country[coord]['longitude'])
                pointChild.append(longChild)
                pointChild.append(latChild)
                regionChild.append(pointChild)
            countryChild.append(regionChild)
            countriesElem.append(countryChild)

    dataChild.append(countriesElem)
    elem.append(requestChild)
    elem.append(dataChild)
    return tostring(elem)

# #for generating xmlForCounties.xml. After generating xmlForCounties should be moved to ISSTrackerFE>static>xml
# file = open(r"../../../ISSTrackerBE/custom.geo_lowres.json")
# data = json.load(file)
# xml = DicToXMLForCounties(processJson(data))
# xml = "<?xml version='1.0' encoding='UTF-8'?>" + str(xml, 'utf-8')
# newFile = open(r"xmlForCounties.xml", "w+")
# newFile.write(xml)
# file.close()
