import os
import calendar
import datetime
from funcs import splice, num, prints
from setTimeFuncs  import monthDays


dateInWeek = ['月', '火', '水', '木', '金', '土', '日']
timeStart = '00:00'
timeEnd = '23:59'


def checkDate(date):
    if not '/' in date:
        return False, False, False
    year, monthAndDate = splice.splice(date, '/', "str")
    monthofPlan, dateofPlan = splice.splice(monthAndDate, "/", "int")#年が書いてある場合のプログラム
    if num.isNum(year) == False:
        return False, False, False
    if dateofPlan == False:#年が書いてない場合のプログラム
        monthofPlan = int(year)
        dateofPlan = int(monthAndDate)
        if num.create(datetime.date.today().year,year,monthAndDate)<num.create(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day):
            year = datetime.date.today().year + 1#年が書いてなくて、日にちがもう過ぎてしまっている場合、予定日が来年に割り振られる。
        else:
            year = datetime.date.today().year#年が書いてなくて、日にちが過ぎていない場合、予定日に今年に割り振られる。
    if monthofPlan > 12:
        return False, False, False
    daysInMonth = monthDays.checkDays(monthofPlan, year)
    if dateofPlan <= daysInMonth:
        return int(year), monthofPlan, dateofPlan
    return False, False, False


def findNumInListList(List, num):
        for listList in List:
            if listList[len(listList)-1] >= num:
                return List.index(listList)
        return len(List)-1
            

def extractFromListList(index, listList):
    extractedList = []
    for list in listList:
        extractedList.append(list[index])
    return extractedList

def makeIntoDict(keyList, valueList):
    dictionary = {}
    for key, value in zip(keyList, valueList):
        if key in dictionary.keys():
            dictionary[key] = f'{dictionary[key]},{value}'
        else:
            dictionary[key] = value
    return dictionary


def askplanDate(text):
    dayList = []
    while True:
        date = prints.ask(text)
        if '-' in date:####日にちを連続させるプログラムを書かないと
            date1, date2 = splice.splice(date, '-', 'str')
            if date1 == '':
                firstYear, firstMonth, firstDay = True, True, True
            else:
                firstYear, firstMonth, firstDay = checkDate(date1)

            if date2 == '':
                pass
            elif not '/' in date2:
                date2 = f'{firstMonth}/{date2}'
            if not date2 == '':
                lastYear, lastMonth, lastDay = checkDate(date2)
            else:
                lastYear, lastMonth, lastDay = True, True, True
            if num.create(firstYear,firstMonth,firstDay)>num.create(lastYear,lastMonth,lastDay):
                lastYear += 1

            if lastYear == True and firstYear == True:
                pass
            elif not firstYear == False or not lastYear == False:
                dayList = firstYear, firstMonth, firstDay, lastYear, lastMonth, lastDay
                
                return dayList
        else:
            dayList = checkDate(date)
            dayList += None, None, None
            if not False in dayList:
                return dayList
        os.system("cls")
        prints.err("正しく入力してください")


while True:
    os.system('cls')
    strtyear, strtmonth, strtday, endyear, endmonth, endday = askplanDate('入力したいシフトを教えてください(Eg. 10/29-11/8):')
    if not strtyear == None:
        break
monthDayList = []
monthDayDict = {}

shiftDate = datetime.datetime(strtyear, strtmonth, strtday)

shiftRange = 14
if not endyear == None:
    endshiftDate = datetime.datetime(endyear, endmonth, endday)
    shiftRange = (endshiftDate-shiftDate).days+1

cal = calendar.monthcalendar(int(strtyear), int(strtmonth))
dateIndex = findNumInListList(cal, strtday)
date = cal[dateIndex].index(strtday) -1

for i in range(shiftRange):
    if len(str(strtmonth)) == 2:
        whiteSpace = '     '
    else:
        whiteSpace = '   '
    if shiftDate.day == 1 or i == 0:
        monthDayDict[f'{shiftDate}'] = f'{int(shiftDate.strftime("%m"))}/{int(shiftDate.strftime("%d"))}'
    else:
        monthDayDict[f'{shiftDate}'] = f'{whiteSpace}{int(shiftDate.strftime("%d"))}'
    shiftDate = shiftDate + datetime.timedelta(days=1)

os.system('cls')

while True:
    for ikey, ivalue in monthDayDict.items():
        date += 1
        if date == 7:
            date = 0
        print(f'{ivalue} #{dateInWeek[date]}')
    input()
    os.system('cls')