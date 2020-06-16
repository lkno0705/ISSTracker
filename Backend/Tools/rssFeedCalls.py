import redis
from dateutil import parser as dateParser

from Backend.Requests import rssFeed
from Backend.Requests import stationReportFeed


def setRssFeed(data):
    __redisHost__ = "localhost"
    __redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True)
    feedName = data['rssFeedName']
    feedItems = data['items']
    for i in range(len(feedItems)):
        timestamp = feedItems[i]['published']
        # get timezone on position 23 from string of timestamp
        timezone = timestamp[23:]
        # parse timestamp to format: 2014-07-17 17:08:00 EDT
        timestamp = dateParser.parse(timestamp, ignoretz=True)
        timestamp = str(timestamp) + " " + str(timezone)
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + str(timestamp) + ":title:", value=feedItems[i]['title'])
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + str(timestamp) + ":summary:", value=feedItems[i]['summary'])
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + str(timestamp) + ":published:", value=feedItems[i]['published'])
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + str(timestamp) + ":link:", value=feedItems[i]['link'])
        print("RSS-Feed:" + feedName + ":" + str(timestamp) + ":title:" + str(feedItems[i]['title']))
        print("RSS-Feed:" + feedName + ":" + str(timestamp) + ":summary:" + str(feedItems[i]['summary']))
        print("RSS-Feed:" + feedName + ":" + str(timestamp) + ":published:" + str(feedItems[i]['published']))
        print("RSS-Feed:" + feedName + ":" + str(timestamp) + ":link:" + str(feedItems[i]['link']))


# set spacetoground rssFeed
data = rssFeed.rssFeed()
setRssFeed(data)
# set stationreport rssFeed
data = stationReportFeed.stationReportFeed()
setRssFeed(data)
