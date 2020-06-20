from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

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
def convertISSFuturePassesToXML(requestData):
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
    return elem

test = [{'futurePassDatetime': '2020-06-20 21-30-15', 'duration': 602}, {'futurePassDatetime': '2020-06-20 23-06-23', 'duration': 652}, {'futurePassDatetime': '2020-06-21 00-43-49', 'duration': 625}, {'futurePassDatetime': '2020-06-21 02-21-08', 'duration': 635}, {'futurePassDatetime': '2020-06-21 03-57-59', 'duration': 651}]
print(tostring((convertISSFuturePassesToXML(test))))
