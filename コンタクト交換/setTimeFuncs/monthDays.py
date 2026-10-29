monthDayList = [31, None, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isLeapYear(year):
    leapYear = False
    if not year % 4 == 0:
        pass
    elif year % 100 == 0 and not year % 400 == 0:
        pass
    else:
        leapYear = True
    return leapYear

def checkDays(month, monthyear):
    if month > 12:
        return False
    if not monthDayList[month-1] == None:
        return monthDayList[month-1]
    elif isLeapYear(int(monthyear)) == True:
        return 29
    else:
        return 28