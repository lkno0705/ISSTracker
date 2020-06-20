from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from Backend.Core.dataStructs import ISSDBKey


# XML-Structure for RSSFeed
# <Request>
#   <requestName>RssFeed</requestName>
#   <data>
#       <RSSFeed>
#          <title></title>
#          <summary></summary>
#          <published></published>
#          <link></link>
#       </RSSFeed>
#       <RSSFeed>
#          <title></title>
#          <summary></summary>
#          <published></published>
#          <link></link>
#       </RSSFeed>
#   </data>
# </Request>

def convertAstrosToXML(requestData):
    elem = Element('Request')
    requestChild = Element("requestName")
    requestChild.text = "RSSFeed"
    elem.append(requestChild)
    dataChild = Element("data")
    for feed in requestData:
        RSSFeedChild = Element("RSSFeed")
        title = Element("title")
        summary = Element("summary")
        published = Element("published")
        link = Element("link")
        title.text = feed['title']
        summary.text = feed['summary']
        published.text = feed['published']
        link.text = feed['link']
        RSSFeedChild.append(title)
        RSSFeedChild.append(summary)
        RSSFeedChild.append(published)
        RSSFeedChild.append(link)
        dataChild.append(RSSFeedChild)
    elem.append(dataChild)
    return tostring(elem)