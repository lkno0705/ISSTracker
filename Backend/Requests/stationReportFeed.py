import rssUtility

def stationReportFeed():
    # Feed URL
    url = "http://blogs.nasa.gov/stationreport/feed/"

    # Read Feed
    return rssUtility.getRssFeed(url)
