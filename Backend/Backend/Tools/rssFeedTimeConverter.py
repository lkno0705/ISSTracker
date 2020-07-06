import datetime


# awaits time in format Tue, 16 Jun 2020 16:00:04 +0000 or Tue, 16 Jun 2020 16:00 EDT
# time[1]=day(16), time[2]=month(Jun), time[3]=year(2020), time[4]=Hour:Minute(16:00) and time[5]=timezone(EDT)
def convert(time):
    time = time.split(" ")
    if time[5] == 'EDT':
        time[5] = '-0400'
    elif time[5] == 'EST':
        time[5] = '-0500'
    if time[4].count("") == 6:
        time[4] = time[4] + ':00'
    date = time[1] + '-' + time[2] + '-' + time[3] + " " + time[4] + " " + time[5]
    timestamp = datetime.datetime.strptime(date, '%d-%b-%Y %H:%M:%S %z').timestamp()
    date = datetime.datetime.utcfromtimestamp(timestamp)
    date = date.strftime('%Y-%m-%d %H-%M-%S')
    return date


# print(convert('Tue, 16 Jun 2020 16:00 EDT'))
