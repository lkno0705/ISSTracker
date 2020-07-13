from xml.etree.ElementTree import Element, ElementTree
from xml.etree.ElementTree import tostring
from Backend.Core import database
from lxml import etree

# Create XML out of dictionary with specific tag- and requestname
def _genericDictToXML(d):
    elem = Element("Request")
    for key, val in d.items():
        if isinstance(val, dict):
            subelem = Element(key)
            for k, v in val.items():
                dictChild = Element(k)
                dictChild.text = str(v)
                subelem.append(dictChild)
        else:
            child = Element(key)
            child.text = str(val)
            elem.append(child)
    elem.append(subelem)
    return elem


# XML for ISSDBKey
# <Request>
#	<requestName>ISSDB</requestName>
#	<data>
#		<timeValue time="2020-06-05 14-25-04">
#			<longitude>b\'1234\'</longitude>
#			<latitude>b\'5678\'</latitude>
#		</timeValue>
#		<timeValue time="2020-06-05 14-15-04">
#			<latitude>b\'5555\'</latitude>
#			<longitude>b\'1111\'</longitude>
#		</timeValue>
#	</data>
# </Request>
def _convertISSDBKeyToXML(requestData):
    data = []
    # take only 10% of the positions. Goal: less XMLData to send to Frontend, faster drawing of ISS route.
    # lower resolution of ISS route is no problem.
    # take 2 ISSDBKeys (pair of longitude and latitude) and leave 18
    for x in range(0, len(requestData), 20):
        data.append(requestData[x])
        data.append(requestData[x + 1])
    requestData = data
    elem = Element("Request")
    requestChild = Element("requestName")
    requestChild.text = "ISSDB"
    elem.append(requestChild)

    dataChild = Element("data")

    roundChild = Element("round")
    timeValueElem = Element("timeValue")

    longNow = 0
    LongLast = 0

    longindex = 0
    latindex = 0

    for x in range(0, len(requestData), 2):
        timeValueElem.attrib = {"time": requestData[x].timeValue}

        if requestData[x].key == "longitude":
            longindex = x
            latindex = x + 1
        else:
            longindex = x + 1
            latindex = x
        longNow = float(requestData[longindex].value)
        LatElem = Element(requestData[latindex].key)
        LatElem.text = str(requestData[latindex].value)
        LongElem = Element(requestData[longindex].key)
        LongElem.text = requestData[longindex].value
        timeValueElem.append(LatElem)
        timeValueElem.append(LongElem)

        if longNow < LongLast != 0:
            dataChild.append(roundChild)
            roundChild = Element("round")
            test = False
        LongLast = longNow
        roundChild.append(timeValueElem)
        timeValueElem = Element("timeValue")
    dataChild.append(roundChild)
    elem.append(dataChild)
    return tostring(elem)


# XML-Structure for AstrosOnISS
# <Request>
#   <requestName>AstrosOnISS</requestName>
#   <data>
#       <Astro name="max muster">
#          <picture>link</picture>
#          <flag>link</flag>
#          <nation>link</nation>
#       </Astro>
#       <Astro name="max muster">
#          <picture>link</picture>
#          <flag>link</flag>
#          <nation>link</nation>
#       </Astro>
#   </data>
# </Request>'

def _convertAstrosToXML(requestData):
    elem = Element('Request')
    requestChild = Element("requestName")
    requestChild.text = "AstrosOnISS"
    elem.append(requestChild)
    dataChild = Element("data")
    for astro in requestData:
        AstroChild = Element("Astro")
        AstroChild.attrib = {"name": astro.name}
        picture = Element("picture")
        flag = Element("flag")
        nation = Element("nation")
        picture.text = astro.pic
        flag.text = astro.flag
        nation.text = astro.nation
        AstroChild.append(picture)
        AstroChild.append(flag)
        AstroChild.append(nation)
        dataChild.append(AstroChild)
    elem.append(dataChild)
    return tostring(elem)


'''
<Request>
	<requestName> GeoJson </requestName>
	<data>
		<countries>
			<country name="Uruguay">
				<1>
					<latitute>-57.62513342958296</latitude>
					<longitude>-30.216294854454258</longitude>
				</1>
			</country>
		</countries>
	</data>
</Request>
'''


# create XML according to structure above
def _convertGeoJSONToXML(requestData):
    # for requests for a single country only a single object is returned
    if not isinstance(requestData, list):
        requestData = [requestData]
    elem = Element('Request')
    requestChild = Element('requestName')
    requestChild.text = 'GeoJson'
    elem.append(requestChild)

    dataChild = Element('data')
    countriesElem = Element('countries')

    for country in requestData:
        countryChild = Element('country')
        countryChild.attrib = {'countryname': country['countryname']}
        countriesElem.append(countryChild)

        count = 0
        while count in country:
            pointElem = Element("point")

            latElem = Element('latitude')
            latElem.text = country[count]['latitude']
            pointElem.append(latElem)

            lonElem = Element('longitude')
            lonElem.text = country[count]['longitude']
            pointElem.append(lonElem)

            countryChild.append(pointElem)
            count = count + 1

    dataChild.append(countriesElem)
    elem.append(dataChild)
    return tostring(elem)


'''
<Request>
	<requestName> ISSfuturePasses </requestName>
	<data>
        <timeValue>
            <time index=1>
                <futurePassDatetime> 2020-06-05 14-15-04 </futurePassDatetime>
                <duration> 635 </duration>
            </time>
            <time index=2>
                <futurePassDatetime> 2020-06-05 18-15-04 </futurePassDatetime>
                <duration> 500 </duration>
            </time>
        </timeValue>
	</data>
</Request>
'''


# create XML according to structure above
def _convertISSFuturePassesToXML(requestData):
    elem = Element('Request')
    requestChild = Element('requestName')
    requestChild.text = 'ISSfuturePasses'
    elem.append(requestChild)
    dataChild = Element('data')
    timeValueElem = Element('timeValue')

    # create tuples for time values
    for index, r in enumerate(requestData):
        timeElem = Element('time')
        timeElem.attrib = {'index': str(index)}
        passDateElem = Element('futurePassDatetime')
        passDateElem.text = r['futurePassDatetime']
        durationElem = Element('duration')
        durationElem.text = str(r['duration'])

        timeElem.append(passDateElem)
        timeElem.append(durationElem)
        timeValueElem.append(timeElem)

    dataChild.append(timeValueElem)
    elem.append(dataChild)
    return tostring(elem)


# XML for ISSFlyBys
# <Request>
# 	<requestName>ISSFlyBys</requestName>
# 	<data>
# 		<numberOfPasses>
# 			3
# 		</numberOfPasses>
# 		<passes>
# 			<pass>
#             <startTime>
#             </startTime>
#             <endTime>
#             </endTime>
#         </pass>
# 			<pass>
#             <startTime>
#             </startTime>
#             <endTime>
#             </endTime>
#         </pass>
# 		</passes>
# 	</data>
# </Request>


def _convertFlyBystoXML(requestData, requestname):
    elem = Element("Request")
    requestChild = Element("requestName")
    requestChild.text = requestname
    elem.append(requestChild)
    dataChild = Element("data")
    numbOfPassesChild = Element("numberOfPasses")
    numbOfPassesChild.text = str(requestData['numberOfPasses'])
    passesChild = Element("passes")

    for x in requestData['passes']:
        passChild = Element("pass")
        startChild = Element("startTime")
        startChild.text = x['startTime']
        endChild = Element("endTime")
        endChild.text = x['endTime']
        passChild.append(startChild)
        passChild.append(endChild)
        passesChild.append(passChild)

    dataChild.append(numbOfPassesChild)
    dataChild.append(passesChild)
    elem.append(dataChild)
    return tostring(elem)


def _convertISSpastPasses(requestData):
    return _convertFlyBystoXML(requestData, 'ISSpastPasses')


def _convertISSCountryPasses(requestData):
    return _convertFlyBystoXML(requestData, 'ISSCountryPasses')


'''
XML-Structure for RSS-Feed
<Request>
  <requestName>RSS-Feed</requestName>
  <data>
      <RSS-Feed>
         <title></title>
         <summary></summary>
         <published></published>
         <link></link>
      </RSS-Feed>
      <RSS-Feed>
         <title></title>
         <summary></summary>
         <published></published>
         <link></link>
      </RSS-Feed>
  </data>
</Request>
'''


def _convertRSSFeedToXML(requestData):
    elem = Element('Request')
    requestChild = Element("requestName")
    requestChild.text = "RSS-Feed"
    elem.append(requestChild)
    dataChild = Element("data")
    for feed in requestData:
        RSSFeedChild = Element("RSS-Feed")
        title = Element("title")
        summary = Element("summary")
        published = Element("published")
        link = Element("link")
        title.text = feed['title']
        summary.text = feed['summary']
        published.text = feed['published']
        link.text = feed['link']
        RSSFeedChild.append(title)
        RSSFeedChild.append(summary)
        RSSFeedChild.append(published)
        RSSFeedChild.append(link)
        dataChild.append(RSSFeedChild)
    elem.append(dataChild)
    return tostring(elem)


'''
<Request>
   <requestName>ISSpos</requestName>
   <data>
       <longitude>1.6688</longitude>
       <latitude>4.3681</latitude>
   </data>
</Request>
'''


def _convertISSPosToXML(requestData):
    elem = Element('Request')
    requestChild = Element("requestName")
    requestChild.text = "ISSpos"
    elem.append(requestChild)
    dataChild = Element("data")
    latitudeChild = Element("latitude")
    longitudeChild = Element("longitude")
    timestampChild = Element("timestamp")
    latitudeChild.text = str(requestData['latitude'])
    longitudeChild.text = str(requestData['longitude'])
    timestampChild.text = str(requestData['timestamp'])
    dataChild.append(latitudeChild)
    dataChild.append(longitudeChild)
    dataChild.append(timestampChild)
    elem.append(dataChild)
    return tostring(elem)


# <Request>
#    <requestName> Geocoding </requestName>
#    <data>
#       <latitude>-57.62513342958296</latitude>
#       <longitude>-30.216294854454258</longitude>
#    </data>
# </Request>


def _convertGeocodingToXML(requestData):
    elem = Element('Request')
    requestChild = Element('requestName')
    requestChild.text = 'Geocoding'
    elem.append(requestChild)
    dataChild = Element('data')
    latElem = Element('latitude')
    latElem.text = str(requestData['latitude'])
    dataChild.append(latElem)
    lonElem = Element('longitude')
    lonElem.text = str(requestData['longitude'])
    dataChild.append(lonElem)

    elem.append(dataChild)
    return tostring(elem)


def _convertCountryList(requestData):
    elem = Element('Request')
    requestChild = Element('requestName')
    requestChild.text = 'CountryList'
    elem.append(requestChild)
    dataChild = Element('data')
    countrylistchild = Element('CountryList')
    for country in requestData:
        countrychild = Element('country')
        countrychild.text = str(country)
        countrylistchild.append(countrychild)
    dataChild.append(countrylistchild)
    elem.append(dataChild)
    return tostring(elem)


def reformatData(requestData, requestName):
    functions = {
        'ISSDB': _convertISSDBKeyToXML,
        'ISSpos': _convertISSPosToXML,
        "ISSCountryPasses": _convertISSCountryPasses,
        "ISSpastPasses": _convertISSpastPasses,
        "ISSfuturePasses": _convertISSFuturePassesToXML,
        'GeoJson': _convertGeoJSONToXML,
        'AstrosOnISS': _convertAstrosToXML,
        "RSS-Feed": _convertRSSFeedToXML,
        "GeocodingAddress": _convertGeocodingToXML,
        "CountryList": _convertCountryList
        # List of Requests
    }
    # get xml
    xmlData = functions.get(requestName)(requestData)
    # add header and convert from bytestring to normal string
    xmlData = "<?xml version='1.0' encoding='UTF-8'?><!DOCTYPE Request SYSTEM \'./DTD/" + requestName + ".dtd\'>" + str(xmlData, 'utf-8')
    return xmlData

'''
Example
#
<Request>
   <requestName>ISS-Pos</requestName>
   <params>
        <timestamp>2012-12-15 01-21-05</timestamp>
        <latitude>-17.9617</latitude>
        <longitude>162.6117</longitude>
   </params>
</Request>

to

{
   "requestname": "ISSpos",
   "params":{
       "timestamp":"2012-12-15 01-21-05",
       "latitude": "-17.9617",
       "longitude": "162.6117"
    }
}

'''


def parseRequestParamsXMLToDic(xml):

    try:
        parser = etree.XMLParser(dtd_validation=True, encoding="utf-8")
        etree.fromstring(xml, parser)
    except etree.XMLSyntaxError:

        return "INVALID XML"

    xml = xml.decode(encoding="utf-8")
    requestDic = {}
    if xml.__contains__("requestName"):
        request = xml.split("<Request>", 1)[1]
        requestName = request.split("<requestName>")[1]
        requestName = requestName.split("<")[0]
        requestDic['requestName'] = requestName
    if xml.__contains__("params"):
        requestData = xml.split("<params>")[1]
        requestData = requestData.split("</params>")[0]
        paramsDic = {}
        count = 0
        for i in requestData:
            if i == '<':
                count = count + 1
        for i in range(0, count, 2):
            xparam = requestData.split("<")[i + 1]
            xparam = xparam.split(">")[0]
            yparamValue = requestData.split("<" + xparam + ">")[1]
            yparamValue = yparamValue.split("</")[0]
            paramsDic[xparam] = yparamValue
        requestDic['params'] = paramsDic
        return requestDic


# # for debugging purposes
# ISSPOS = {"requestname": "ISSpos",
#         "data": {"timestamp": "2012-12-15 01-21-05", "latitude": "-17.9617", "longitude": "162.6117"}}
# Isspast={'numberOfPasses': 1, 'passes': [{'startTime': '2020-06-19 22-55-21', 'endTime': '2020-06-19 22-55-26'}]}
# isscountry={'numberOfPasses': 1, 'passes': [{'startTime': '2020-06-19 22-55-21', 'endTime': '2020-06-19 22-55-26'}]}
# issfurute=[{'futurePassDatetime': '2020-06-20 21-30-15', 'duration': 602}, {'futurePassDatetime': '2020-06-20 23-06-23', 'duration': 652}, {'futurePassDatetime': '2020-06-21 00-43-49', 'duration': 625}, {'futurePassDatetime': '2020-06-21 02-21-08', 'duration': 635}, {'futurePassDatetime': '2020-06-21 03-57-59', 'duration': 651}]
# rssfeed={'rssFeedName':'spacetoground',
# 'items':
# [
# {'title': 'Space to Ground: Round Three: 12/6/2019', 'summary': 'There is never a dull moment onboard the orbiting laboratory. There were three spacewalks to fix a cosmic particle detector and now two space cargo ships are on their way to the station.', 'published': 'Fri, 06 Dec 2019 11:19 EST', 'link': 'http://www.nasa.gov/mediacast/space-to-ground-round-three-1262019'},
# {'title': 'Space to Ground: Keeping it Cool: 11/29/2019', 'summary': 'The Expedition 61 crew enjoyed a Thanksgiving feast ahead of another spacewalk set for this Monday. A European experiment also tests controlling a rover on Earth from the station.', 'published': 'Fri, 29 Nov 2019 08:00 EST', 'link': 'http://www.nasa.gov/mediacast/space-to-ground-keeping-it-cool-11292019'}
# ]
# }
# astros=database.redisDB._getAstros(database.redisDB,None)
# issdbkey = database.redisDB._getISS(database.redisDB, {
#     "requestname": "ISSDB",
#     "params": {
#         "startTime": "2020-06-15 16-16-32",
#         "endTime": "2020-06-29 16-16-33"
#     }
# })
#
# print(reformatData(ISSPOS['data'], 'ISSpos'))
# print("\n")
# print(reformatData(Isspast, 'ISSpastPasses'))
# print("\n")
# print(reformatData(isscountry, 'ISSCountryPasses'))
# print("\n")
# print(reformatData(issfurute, 'ISSfuturePasses'))
# print("\n")
# print(reformatData(rssfeed['items'], 'RSS-Feed'))
# print("\n")
# print(reformatData(astros, 'AstrosOnISS'))
# print("\n")
# reformatData(issdbkey, 'ISSDB')
# print("\n")
