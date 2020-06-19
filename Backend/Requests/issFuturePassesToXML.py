from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring

'''
<Request>
	<requestName> ISS Future Passes </requestName>
	<data>
        <timeValue>
            <time>2020-06-05 14-15-04 </time>
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

    for time in requestData:



    elem.append(dataChild)
    return elem

Test = ['2020-06-18 21-31-17', '2020-06-18 23-04-25', '2020-06-19 00-40-54', '2020-06-19 02-18-24', '2020-06-19 03-55-37', '2020-06-19 05-32-27', '2020-06-19 07-10-10', '2020-06-19 22-16-59', '2020-06-19 23-52-57', '2020-06-20 01-30-21']

print(tostring(convertISSFuturePassesToXML(Test)))
