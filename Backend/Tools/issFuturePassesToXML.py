from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

'''
<Request>
	<requestName> ISS Future Passes </requestName>
	<data>
        <timeValue>
            <time index=1> 2020-06-05 14-15-04 </time>
            <time index=2> 2020-06-05 18-15-04 </time>
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
    for index, time in enumerate(requestData):
        timeElem = Element('time')
        timeElem.attrib = {'index': str(index)}
        timeElem.text = time
        timeValueElem.append(timeElem)

    dataChild.append(timeValueElem)
    elem.append(dataChild)
    return elem
