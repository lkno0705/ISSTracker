from Backend.Requests import rssUtility
from Backend.Core.database import redisDB

def rssFeed():
    db = redisDB()
    # Feed URL
    urls = ("https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss", "http://blogs.nasa.gov/stationreport/feed/")
    # set rssFeedName and read Feed into items
    data = {'items': rssUtility.getRssFeed(urls)}
    db.setData(data=data, requestname="RSS-Feed")