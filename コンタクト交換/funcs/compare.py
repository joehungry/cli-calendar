try:
    from funcs import breakup, num

except:
    import breakup, num

def isSandwitchNum(nowDate, startPlan, endPlan):
    if int(startPlan) <= int(nowDate) and int(nowDate) <= int(endPlan):
        return True
    return False

def time(startTime, endTime):
    startTimeHour, startTimeMinute, endTimeHour, endTimeMinute = breakup.timeplan(f'{startTime}-{endTime}')
    if startTimeHour > 24 or endTimeHour > 24:
        return 'timeUnitErr', False, False, False
    if startTimeMinute >= 60 or endTimeMinute >= 60:
        return 'timeUnitErr', False, False, False
    if startTimeHour == endTimeHour and endTimeMinute <= startTimeMinute:
        return 'endExceedsStartErr', False, False, False
    if not startTimeHour <= endTimeHour:
        return 'endExceedsStartErr', False, False, False
    else:
        return startTimeHour, startTimeMinute, endTimeHour, endTimeMinute

def addTimePlan(timeplanlist):
    newList = []
    newList = num.numify(timeplanlist)
    print(f'{newList=}')
    p2 = '1'
    for i in newList.values():
        p2 += str(i)
    return p2

def add0(num):
    numStr = str(num)
    if len(numStr) == 1:
        return (f'0{numStr}')
    else:
        return numStr

def timeNum(timeplan):
    startTimeHour1, startTimeMinute1, endTimeHour1, endTimeMinute1 = breakup.timeplan(timeplan) 
    returnValue1 = add0(startTimeHour1) + add0(startTimeMinute1)
    returnValue2 = add0(endTimeHour1) + add0(endTimeMinute1)
    return int('1' + returnValue1), int('1' + returnValue2)


def timePlan(timeplan1, timeplan2):
    startTimeNum1, endTimeNum1 = timeNum(timeplan1)
    startTimeNum2, endTimeNum2 = timeNum(timeplan2)
    if startTimeNum1 <= startTimeNum2 and endTimeNum2 <= endTimeNum1:
        return timeplan1, None
    elif startTimeNum1 >= startTimeNum2 and endTimeNum2 >= endTimeNum1:
        return timeplan2, None
    elif startTimeNum1 < endTimeNum1 and endTimeNum1 < startTimeNum2:
        return timeplan1, timeplan2 #the smaller One is first
    elif startTimeNum1 > endTimeNum1 and endTimeNum1 > startTimeNum2:
        return timeplan2, timeplan1 #the Larger One is first
    elif endTimeNum1 >= startTimeNum2:
        return f'{str(startTimeNum1)[1:3]}:{str(startTimeNum1)[3:5]}-{str(endTimeNum2)[1:3]}:{str(endTimeNum2)[3:5]}', None
    elif endTimeNum2 >= startTimeNum1:
        return f'{str(startTimeNum2)[1:3]}:{str(startTimeNum2)[3:5]}-{str(endTimeNum1)[1:3]}:{str(endTimeNum1)[3:5]}', None
    else:
        print(f'huh? {timeplan1=} : {timeplan2=}')
theTime = ['10:00-20:00','10:00-18:00','11:00-17:00']


if __name__ == '__main__':
    print(isSandwitchNum(1, 1, 10))
    print(isSandwitchNum(5, 1, 10))
    print(isSandwitchNum(10, 1, 10))
    print(isSandwitchNum(0, 1, 10))
    print(isSandwitchNum(11, 1, 10))