from Backend.Requests import rssUtility


def stationReportFeed():
    # Feed URL
    url = "http://blogs.nasa.gov/stationreport/feed/"
    # set rssFeedName and read Feed
    data = {'rssFeedName': 'stationreport', 'items': rssUtility.getRssFeed(url)}
    return data
