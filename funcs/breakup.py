try:
    from funcs import splice
except:
    import splice

def time(time):
     timehour, timeminute = splice.splice(time, ":", "int")
     return timehour, timeminute

def timeplan(WholeTime):
    try:
        timeStart, timeEnd = splice.splice(WholeTime, "-", "str")

        if timeStart == "":
            timeStart = "00:00"
        elif timeEnd == "":
            timeEnd = "23:59"

        timeStartHour, timeStartMinute = time(timeStart)
        timeEndHour, timeEndMinute = time(timeEnd)
        return timeStartHour, timeStartMinute, timeEndHour, timeEndMinute
    except TypeError:
        return False, False, False, False
    

def date(date):
    year, monthday = splice.splice(date, '/', "str")
    month, day = splice.splice(monthday, '/', 'int')
    return int(year), month, day
