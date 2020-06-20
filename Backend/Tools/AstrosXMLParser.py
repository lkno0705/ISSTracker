from xml.etree.ElementTree import Element
from Backend.Core import database
from xml.etree.ElementTree import tostring


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

def convertAstrosToXML(requestData):
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

# print(convertAstrosToXML(database.redisDB._getAstros(database.redisDB, None)))
