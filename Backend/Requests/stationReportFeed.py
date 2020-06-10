import rssUtility

def stationReportFeed():
    # Feed URL
    url = "http://blogs.nasa.gov/stationreport/feed/"

    # Read Feed
    entry = rssUtility.getRssFeed(url)

    list = []

    #create return values
    for en in entry:
        dict = {'title': en.title,
                'summary': en.summary,
                'published': en.published,
                'link': en.link}
        list.append(dict)

    # Return dictionary with RSS list
    return { 'items': list }
