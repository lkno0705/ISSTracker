from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

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
def convertGeoJSONToXML(requestData):

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
    return elem
