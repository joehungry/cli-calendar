import os, datetime
from funcs import file, cli, prints, splice, num
from setTimeFuncs import monthDays

untilContactChange = 14 # days until contact change

today = datetime.date.today()
contactDateFile = file.content('contactFolder', 'contactDate.txt')

contactWornDateD = {
    "rightContact": "None",
    "leftContact": "None",
}

def strToDate(dateStr):
    """Convert a date string in 'YYYY/MM/DD' format to a datetime.date object."""
    if not '/' in dateStr:
        return today
    else:
        date = splice.toList(dateStr, '/', 'int')
        return datetime.date(int(date[0]), int(date[1]), int(date[2]))

def determine_year(month_str, date_str) -> int:
    import datetime
    this_year = True
    next_year = True

    if num.dataType(month_str) != 'int':
        return None
    if num.dataType(date_str) != 'int':
        return None
    month = int(month_str)
    date = int(date_str)
    today = datetime.datetime.now()
    month_days_this_year = monthDays.checkDays(month, today.year)
    month_days_next_year = monthDays.checkDays(month, today.year + 1)
    if date > month_days_this_year:
        this_year = False
    if date > month_days_next_year:
        next_year =False

    if this_year == True and next_year == False:
        return today.year
    elif next_year == True and this_year == False:
        return today.year + 1
    elif this_year == False and next_year == False:
        return None

    plan_datetime = datetime.datetime(today.year, month, date)
    if plan_datetime >= today:
        return today.year
    plan_datetime = datetime.datetime(today.year+1, month, date)
    date_difference = (plan_datetime - today).days
    if date_difference < 183: #今年のその日程と来年のその日程を比べて、近い方に設定
        return today.year + 1
    return today.year


def checkDate(date):
    today = datetime.date.today()
    if not '/' in date:
        return False, False, False
    year, monthAndDate = splice.splice(date, '/', "str")
    monthofPlan, dateofPlan = splice.splice(monthAndDate, "/", "int")#年が書いてある場合のプログラム
    if num.isNum(year) == False:
        return False, False, False
    if monthofPlan > 12:
        return False, False, False

    if dateofPlan == False:#年が書いてない場合のプログラム
        monthofPlan = int(year)
        dateofPlan = int(monthAndDate)
        year = determine_year(monthofPlan, dateofPlan)
    daysInMonth = monthDays.checkDays(monthofPlan, year)
    if dateofPlan <= daysInMonth:
        return int(year), monthofPlan, dateofPlan

    return False, False, False

def changeContactDate(contactDict):
    changeContactD = {
    '右目コンタクト着用日': 'rightContact',
    '左目コンタクト着用日': 'leftContact',
    '両目コンタクト着用日': 'bothContact'
    }
    while True:
        os.system('cls')
        print('コンタクト着用日変更')
        print()
        cli.chooseScreen(changeContactD)
        settingNum = prints.ask('変更する設定を選択してください')
        settingKey = cli.choosing(settingNum, changeContactD)
        year, month, date = checkDate(prints.ask('新しいコンタクト着用日を入力してください (YYYY/MM/DD)'))
        if not year == False:
            newDate = f'{year}/{month:02d}/{date:02d}'
        if settingKey == 'bothContact':
            for i in contactDict:
                contactDict[i] = newDate
            break
        else:
            contactDict[settingKey] = newDate
            break


contactDateContent = contactDateFile.fetch()
for i in contactDateContent:
    contactDateKey, contactDateValue = i.split(':')
    if contactDateKey in contactWornDateD:
        contactWornDateD[contactDateKey] = contactDateValue

while True:
    os.system('cls')
    contactChangeDateD = {}
    for i in contactWornDateD:
        contactChangeDateD[i] = strToDate(contactWornDateD[i])

    untilRightContactChange = contactChangeDateD['rightContact'] + datetime.timedelta(days=untilContactChange)
    untilLeftContactChange = contactChangeDateD['leftContact'] + datetime.timedelta(days=untilContactChange)

    print('コンタクト着用マデ')
    print()
    print('右目:')
    print(f'  {(untilRightContactChange - today).days}日後 ({contactChangeDateD['rightContact']})')
    print('左目:')
    print(f'  {(untilLeftContactChange - today).days}日後 ({contactChangeDateD['leftContact']})')
    print()
    print('変更があれば、Enerキーを押してください')
    input()


    os.system('cls')
    settingD = {
        "右目コンタクト交換": "rightContact",
        "左目コンタクト交換": "leftContact",
        "コンタクト着用日変更": "changeContactDate",
        "戻る": "back"
    }

    while True:
        print('コンタクト交換設定')
        print()
        cli.chooseScreen(settingD)
        settingNum = prints.ask('変更する設定を選択してください')
        settingKey = cli.choosing(settingNum, settingD)
        if settingKey == 'changeContactDate':
            changeContactDate(contactWornDateD)
            break
        elif settingKey == "back":
            break
        elif not settingKey == None:
            contactWornDateD[settingKey] = today.strftime('%Y/%m/%d')
            break
        else:
            prints.err('設定が選択されていません')
            input()
        os.system('cls')

    saveContactDateStr = ''
    for ilen, i in enumerate(contactWornDateD):
        saveStr  = f'{i}:{contactWornDateD[i]}'
        if ilen == 0:
            saveContactDateStr += saveStr
        else:
            saveContactDateStr += f'\n{saveStr}'

    contactDateFile.save(saveContactDateStr, '*overwrite*')