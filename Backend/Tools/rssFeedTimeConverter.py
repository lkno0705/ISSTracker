import datetime


def convert(time):
    time = time.split(" ")
    day = time[1]
    month = time[2]
    year = time[3]
    hourMinute = time[4]
    timezone = time[5]
    if timezone == 'EDT':
        timezone = '-0400'
    elif timezone == 'EST':
        timezone = '-0500'
    if hourMinute.count("") == 6:
        hourMinute = hourMinute + ':00'
    date = day + '-' + month + '-' + year + " " + hourMinute + " " + timezone
    timestamp = datetime.datetime.strptime(date, '%d-%b-%Y %H:%M:%S %z').timestamp()
    date = datetime.datetime.utcfromtimestamp(timestamp)
    date = str(date).replace(':', '-')
    return date
