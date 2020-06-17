import redis
from datetime import datetime
from Backend.Requests import rssFeed
from Backend.Requests import stationReportFeed
from Backend.Tools import rssFeedTimeConverter as dateConverter

__redisHost__ = "localhost"
__redisDB__ = redis.StrictRedis(host=__redisHost__, port=6379, db=0, decode_responses=True)


def setRssFeed(data):
    feedName = data['rssFeedName']
    feedItems = data['items']
    for i in range(len(feedItems)):
        # convert date into utc and format yyyy-mm-dd HH-MM-S
        publishDate = dateConverter.convert(feedItems[i]['published'])
        expireTime = 3600  # expiration time in seconds: 3600sec = 1H
        firstKeyPart = "RSS-Feed:" + feedName + ":" + publishDate
        __redisDB__.set(name=firstKeyPart + ":title", value=feedItems[i]['title'], ex=expireTime)
        __redisDB__.set(name=firstKeyPart + ":summary", value=feedItems[i]['summary'], ex=expireTime)
        __redisDB__.set(name=firstKeyPart + ":published", value=publishDate, ex=expireTime)
        __redisDB__.set(name=firstKeyPart + ":link", value=feedItems[i]['link'], ex=expireTime)
        # print(firstKeyPart + ":title:" + str(feedItems[i]['title']))
        # print(firstKeyPart + ":summary:" + str(feedItems[i]['summary']))
        # print(firstKeyPart + ":published:" + publishDate)
        # print(firstKeyPart + ":link:" + str(feedItems[i]['link']))


# # set spacetoground rssFeed
# data = rssFeed.rssFeed()
# setRssFeed(data)
# # set stationreport rssFeed
# data = stationReportFeed.stationReportFeed()
# setRssFeed(data)


def getRssFeed(requestData):
    requestTime = requestData['params']['time']
    numbOfItems = requestData['params']['numberOfItems']
    keys = __redisDB__.keys("RSS-Feed:*")
    timeKeys = []
    # get keys(datetime in 'published') of rssFeeds
    for key in keys:
        if str(key).endswith('published'):
            # get key in format: RSS-Feed:spacetoground/stationreport:'%Y-%m-%d %H-%M-%S'
            timeKeys.append(str(key).replace(':published', ''))
    items = []
    for key in timeKeys:
        keyElements = key.split(':')
        # read publishing date out of key
        publishDate = keyElements[2]
        publishTimestamp = datetime.strptime(publishDate, '%Y-%m-%d %H-%M-%S').timestamp()
        requestTimestamp = datetime.strptime(requestTime, '%Y-%m-%d %H-%M-%S').timestamp()
        # check if number of rssfeeds wished is not exceeded and this rssFeed published before the getRequest was done
        if len(items) < numbOfItems and publishTimestamp <= requestTimestamp:
            items.append({'title': __redisDB__.get(key + ':title'), 'summary': __redisDB__.get(key + ':summary'),
                          'published': publishDate, 'link': __redisDB__.get(key + ':link')})
    items = sorted(items, key=lambda i: (i['published']), reverse=True)
    return items


# requestParams = {'params': {'time': '2018-07-05 16-36-00', 'numberOfItems': 4}}
# print(*getRssFeed(requestParams), sep='\n')
