from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from Backend.Core.dataStructs import ISSDBKey
import struct

d = { "requestName": "ISSpos", "data": {"timestamp": "2012-12-15 01-21-05", "latitude":"-17.0617","longitude":"162.6117"}}
l = [
    ISSDBKey(timeValue='2020-06-05 14-25-04', key='longitude', value=b'1234'),
    ISSDBKey(timeValue='2020-06-05 14-25-04', key='latitude', value=b'5678'),
    ISSDBKey(timeValue='2020-06-05 14-26-04', key='latitude', value=b'5555'),
    ISSDBKey(timeValue="2020-06-05 14-26-04", key="longitude", value=b"1111"),
    ISSDBKey(timeValue="2020-06-05 14-27-04", key="longitude", value=b"1212"),
    ISSDBKey(timeValue='2020-06-05 14-27-04', key='latitude', value=b'5555'),
]

# Create XML out of dictionary with specific tag- and requestname
def genericDictToXML(d):
    
    elem = Element("Request")
    for key,val in d.items():
        if isinstance(val,dict):
            subelem = Element(key)
            for k,v in val.items():
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
def convertISSDBKeyToXML(requestData):

    elem = Element("Request")
    requestChild = Element("requestName")
    requestChild.text = "ISSDB"
    elem.append(requestChild)

    dataChild = Element("data")

    timeValueElem = Element("timeValue")

    for key in requestData:

        if 'time' in timeValueElem.attrib:
            if timeValueElem.attrib["time"] == key.timeValue:
                if key.key == 'longitude':
                    keyElem = Element(key.key)
                    keyElem.text = str(struct.unpack('f', key.value)[0])
                    timeValueElem.append(keyElem)
                    if len(timeValueElem) == 2:
                        dataChild.append(timeValueElem)
                        timeValueElem = Element("timeValue")
                else:
                    keyElem = Element(key.key)
                    keyElem.text = str(struct.unpack('f', key.value)[0])
                    timeValueElem.append(keyElem)
                    if len(timeValueElem) == 2:
                        dataChild.append(timeValueElem)
                        timeValueElem = Element("timeValue")

        else:
            timeValueElem.attrib = {"time": key.timeValue}
            if key.key == 'longitude':
                keyElem = Element(key.key)
                keyElem.text = str(struct.unpack('f', key.value)[0])
                timeValueElem.append(keyElem)
                if len(timeValueElem) == 2:
                    dataChild.append(timeValueElem)
                    timeValueElem = Element("timeValue")
            else:
                keyElem = Element(key.key)
                keyElem.text = str(struct.unpack('f', key.value)[0])
                timeValueElem.append(keyElem)
                if len(timeValueElem) == 2:
                    dataChild.append(timeValueElem)
                    timeValueElem = Element("timeValue")

    elem.append(dataChild)
    tostring(elem)
    return elem

def convertISSPosToXML(requestData):
    return 10

def reformatData(requestData, requestName):
    functions = {
        'ISSpos': convertISSPosToXML,
        'ISSDB': convertISSDBKeyToXML
        # List of Requests
    }

    return functions.get(requestName)(requestData)

print(tostring(reformatData(l, "ISSDB")))
