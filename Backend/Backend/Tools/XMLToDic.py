import xmltodict
import json


# for only one country
def parseXMLTODic(countryInXML):
    country = xmltodict.parse(countryInXML)
    country = json.dumps(country)
    country = json.loads(country)
    country = country['country']
    countryDic = {}
    countryDic['countryname'] = country['@countryname']
    for i in range(len(country['point'])):
        countryDic[i] = country['point'][i]
    return countryDic