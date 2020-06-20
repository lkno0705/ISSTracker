from Backend.Requests import rssUtility
from Backend.Core.database import redisDB

def rssFeed():
    db = redisDB()
    # Feed URL
    url = "https://www.nasa.gov/rss/dyn/spacetoground_vodcast.rss"
    # set rssFeedName and read Feed into items
    data = {'rssFeedName': 'spacetoground', 'items': rssUtility.getRssFeed(url)}
    db.setData(data=data, requestname="RSS-Feed")

    # Feed URL
    url = "http://blogs.nasa.gov/stationreport/feed/"
    # set rssFeedName and read Feed
    data = {'rssFeedName': 'stationreport', 'items': rssUtility.getRssFeed(url)}
    db.setData(data=data, requestname="RSS-Feed")