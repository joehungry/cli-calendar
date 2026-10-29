import datetime
#try:
from funcs import breakup
#except:
#    import breakup

def fromDate(date, time):
    year, month, day = breakup.date(date)
    hour, minute = breakup.time(time)
#    epochFirstTime = datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0)
    datetimeTime = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return datetimeTime.timestamp()

if __name__ == '__main__':
    print(fromDate('2024/1/29', '23:59'))
    print(datetime.datetime.fromtimestamp(fromDate('2024/1/29', '23:59')))