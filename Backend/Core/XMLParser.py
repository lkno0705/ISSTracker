from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

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
    elem = Element("Request")
    requestChild = Element("requestName")
    requestChild.text = "ISSDB"
    elem.append(requestChild)

    dataChild = Element("data")

    timeValueElem = Element("timeValue")

    for x in range(0, len(requestData), 2):

        timeValueElem.attrib = {"time": requestData[x].timeValue}

        for i in range(0, 2):
            keyElem = Element(requestData[x + i].key)
            keyElem.text = str(requestData[x + i].value)
            timeValueElem.append(keyElem)

        dataChild.append(timeValueElem)
        timeValueElem = Element("timeValue")

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
        while str(count) in country:
            countElem = Element(str(count))

            latElem = Element('latitude')
            latElem.text = country[str(count)]['latitude']
            countElem.append(latElem)

            lonElem = Element('longitude')
            lonElem.text = country[str(count)]['longitude']
            countElem.append(lonElem)

            countryChild.append(countElem)
            count = count + 1

    dataChild.append(countriesElem)
    elem.append(dataChild)
    return tostring(elem)


'''
<Request>
	<requestName> ISS Future Passes </requestName>
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
    requestChild.text = 'ISS Future Passes'
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
    _convertFlyBystoXML(requestData, 'ISSpastPasses')


def _convertISSCountryPasses(requestData):
    _convertFlyBystoXML(requestData, 'ISSCountryPasses')


'''
XML-Structure for RSSFeed
<Request>
  <requestName>RssFeed</requestName>
  <data>
      <RSSFeed>
         <title></title>
         <summary></summary>
         <published></published>
         <link></link>
      </RSSFeed>
      <RSSFeed>
         <title></title>
         <summary></summary>
         <published></published>
         <link></link>
      </RSSFeed>
  </data>
</Request>
'''


def _convertRSSFeedToXML(requestData):
    elem = Element('Request')
    requestChild = Element("requestName")
    requestChild.text = "RSSFeed"
    elem.append(requestChild)
    dataChild = Element("data")
    for feed in requestData:
        RSSFeedChild = Element("RSSFeed")
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


def reformatData(requestData, requestName):
    functions = {
        'ISSDB': _convertISSDBKeyToXML,
        'ISSpos': _convertISSPosToXML,
        "ISSCountryPasses": _convertISSCountryPasses,
        "ISSpastPasses": _convertISSpastPasses,
        "ISSFuturePasses": _convertISSFuturePassesToXML,
        'GeoJSON': _convertGeoJSONToXML,
        'AstrosOnISS': _convertAstrosToXML,
        "RSSFeed": _convertRSSFeedToXML
        # List of Requests
    }
    return functions.get(requestName)(requestData)

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
    requestDic = {}
    request = xml.split("<Request>", 1)[1]
    requestName = request.split("<requestName>")[1]
    requestName = requestName.split("<")[0]
    requestDic['requestName'] = requestName
    requestData = request.split("<params>")[1]
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
