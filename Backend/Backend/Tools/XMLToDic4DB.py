import xmltodict
import json
from Backend.Core.dataStructs import ISSDBKey


# for only one country
def GeoJsonXMLToDic(countryInXML):
    country = xmltodict.parse(countryInXML)
    country = json.dumps(country)
    country = json.loads(country)
    country = country['country']
    countryDic = {'countryname': country['@countryname']}
    for i in range(len(country['point'])):
        countryDic[i] = country['point'][i]
    return countryDic


def ISSPosXMLToISSDBKey(posXML):
    if posXML == "":
        return []
    else:
        positions = xmltodict.parse(posXML)
        positions = json.dumps(positions)
        positions = json.loads(positions)['Request']['data']['isspos']
        if not isinstance(positions, list):
            positions = [positions]
        DBkeys = []
        for position in positions:
            try:
                longitude = ISSDBKey(timeValue=position['time'], key='longitude', value=position['longitude'])
                latitude = ISSDBKey(timeValue=position['time'], key='latitude', value=position['latitude'])
                DBkeys.append(longitude)
                DBkeys.append(latitude)
            except:  # If the current position is incomplete and missing one of the needed tags, then continue with next position
                continue
        return DBkeys
