import redis

from Backend.Requests import rssFeed
from Backend.Requests import stationReportFeed
from Backend.Tools import rssFeedTimeConverter as timeConverter

__redisHost__ = "localhost"
__redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True)


def setRssFeed(data):
    feedName = data['rssFeedName']
    feedItems = data['items']
    for i in range(len(feedItems)):
        time = feedItems[i]['published']
        time = timeConverter.convert(time)
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":title", value=feedItems[i]['title'], ex=3600)
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":summary", value=feedItems[i]['summary'], ex=3600)
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":published", value=time, ex=3600)
        __redisDB__.set(name="RSS-Feed:" + feedName + ":" + time + ":link", value=feedItems[i]['link'], ex=3600)
        # print("RSS-Feed:" + feedName + ":" + time + ":title:" + str(feedItems[i]['title']))
        # print("RSS-Feed:" + feedName + ":" + time + ":summary:" + str(feedItems[i]['summary']))
        # print("RSS-Feed:" + feedName + ":" + time + ":published:" + time)
        # print("RSS-Feed:" + feedName + ":" + time + ":link:" + str(feedItems[i]['link']))


# set spacetoground rssFeed
data = rssFeed.rssFeed()
setRssFeed(data)
# set stationreport rssFeed
data = stationReportFeed.stationReportFeed()
setRssFeed(data)


# awaits utc time in format yyyy-mm-dd HH-MM-SS!!
def getRssFeed(time, numbOfItems):
    keys = __redisDB__.keys("RSS-Feed:*")
    timeKeys = []
    # get keys(datetime in 'published') of rssFeeds
    for key in keys:
        if str(key).endswith('published'):
            timeKeys.append(str(key).replace(':published', ''))
    items = []
    for key in timeKeys:
        # check if number of rssfeeds wished is not exceeded and this rssFeed published before the getRequest was done
        if len(items) < numbOfItems and str(__redisDB__.get(key + ':published')) <= time:
            items.append({'title': __redisDB__.get(key + ':title'), 'summary': __redisDB__.get(key + ':summary'),
                          'published': __redisDB__.get(key + ':published'), 'link': __redisDB__.get(key + ':link')})

    return sorted(items, key=lambda i: (i['published']),reverse=True)


print(*getRssFeed('2018-07-05 16-36-00', 40), sep='\n')
