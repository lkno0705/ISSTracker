from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from Backend.Core.dataStructs import ISSDBKey


# XML for ISSFlyBys
# # <Request>
# #	<requestName>ISSFlyBys</requestName>
# #	<data>
# #		<numberOfPasses>
# #			3
# #		</numberOfPasses>
# #		<passes>
# #			<pass>
# #             <startTime>
# #             </startTime>
# #             <endTime>
# #             </endTime>
# #         </pass>
# #			<pass>
# #             <startTime>
# #             </startTime>
# #             <endTime>
# #             </endTime>
# #         </pass>
# #		</passes>
# #	</data>
# # </Request>


def convertFlyBystoXML(requestData):
    elem = Element("Request")
    requestChild = Element("requestName")
    requestChild.text = "ISSFlyBys"
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
