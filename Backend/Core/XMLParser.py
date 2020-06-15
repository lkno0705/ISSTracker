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


# TODO: def convertByteToFloat(byteString):

# XML
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

    for key in requestData:
    
        if dataChild.find("timeValue"):
            for time in dataChild.iterfind("data/timeValue[@time='" + key.timeValue + "']"):
                if key.timeValue == time.get("time"):
                    keyElem = Element(key.key)
                    keyElem.text = str(struct.unpack('f', key.value)[0])
                    time.append(keyElem)
                    break
#                else:

            timeValueElem = Element("timeValue")
            timeValueElem.attrib = {"time": key.timeValue}

            keyElem = Element(key.key)
            keyElem.text = str(struct.unpack('f', key.value)[0])

            timeValueElem.append(keyElem)
            dataChild.append(timeValueElem)
        else:
            timeValueElem = Element("timeValue")
            timeValueElem.attrib = {"time": key.timeValue}

            keyElem = Element(key.key)
            keyElem.text = str(struct.unpack('f', key.value)[0])

            timeValueElem.append(keyElem)
            dataChild.append(timeValueElem)    

    elem.append(dataChild)
    tostring(elem)
    return elem

#def createDictISSDBKey(requestData):

    listOfDicts = []
    for k in requestData:
        # Handling duplicates with lists as values in dictionary
        if not listOfDicts:
            dictionary = {}
            dictionary["timeValue"] = k.timeValue
            dictionary["key"] = [k.key]
            dictionary["value"] = [k.value]
            dictionary["timeStamp"] = k.timestamp
            listOfDicts.append(dictionary)
        # Append keys and values of same timestamp
        elif k.timestamp == listOfDicts[len(listOfDicts)-1]["timeStamp"]:
            listOfDicts[len(listOfDicts)-1]["key"].append(k.key)
            listOfDicts[len(listOfDicts)-1]["value"].append(k.value)
        else:
            dictionary = {}
            dictionary["timeValue"] = k.timeValue
            dictionary["key"] = [k.key]
            dictionary["value"] = [k.value]
            dictionary["timeStamp"] = k.timestamp
            listOfDicts.append(dictionary)     

    return convertISSDBKeyToXML(listOfDicts)

def createDictISSPos(requestData):
    return 10

def reformatData(requestData, requestName):
    functions = {
        'ISSpos': createDictISSPos,
        'ISSDB': convertISSDBKeyToXML
        # List of Requests
    }

    return functions.get(requestName)(requestData)

print(tostring(reformatData(l, "ISSDB")))
