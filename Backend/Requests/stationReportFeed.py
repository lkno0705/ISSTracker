from Backend.Requests import rssUtility


def stationReportFeed():
    # Feed URL
    url = "http://blogs.nasa.gov/stationreport/feed/"

    # set rssFeedName
    data = rssUtility.getRssFeed(url)
    data['rssFeedName'] = 'stationreport'
    # Read Feed
    return data