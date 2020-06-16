import redis

from Backend.Requests import rssFeed
from Backend.Requests import stationReportFeed
from Backend.Tools import rssFeedTimeConverter as timeConverter


def setRssFeed(data):
    __redisHost__ = "localhost"
    __redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True)
    feedName = data['rssFeedName']
    feedItems = data['items']
    for i in range(len(feedItems)):
        time = feedItems[i]['published']
        time = timeConverter.convert(time)
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":title:", value=feedItems[i]['title'])
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":summary:", value=feedItems[i]['summary'])
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":published:", value=feedItems[i]['published'])
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":link:", value=feedItems[i]['link'])
        print("RSS-Feed:" + feedName + ":" + str(time) + ":title:" + str(feedItems[i]['title']))
        print("RSS-Feed:" + feedName + ":" + str(time) + ":summary:" + str(feedItems[i]['summary']))
        print("RSS-Feed:" + feedName + ":" + str(time) + ":published:" + str(feedItems[i]['published']))
        print("RSS-Feed:" + feedName + ":" + str(time) + ":link:" + str(feedItems[i]['link']))


# set spacetoground rssFeed
data = rssFeed.rssFeed()
setRssFeed(data)
# set stationreport rssFeed
data = stationReportFeed.stationReportFeed()
setRssFeed(data)
