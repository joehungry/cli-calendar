timestamp = 0
dateTypLoc = 1
dateNAMELoc = 2
dateSTARTSHOWINGLoc = 3
dateDATELoc = 4
dateTIMELoc = 5
dateTIMEENDLoc = 6
dateEXPIRESTARTLoc = 7
dateEXPIREENDLoc = 8
dateDAYLoc = 9
dateREMINDERLoc = 10
dateDONELoc = 11

import os

os.system('cls')
print()
print("空いてない・空いてないかもしれない日を設定してください : ")
print()
settingsDict = {"予定設定": 0, "タスク設定": 2, "予定なしタスク": 1, "設定変更": 4}#これは、設定とその変数（数）を一つに入れたdictionaaryです。
for lenI, i in enumerate(settingsDict):
    print(f'{lenI+1}. {i}')
print()


days = ["月", "火", "水", "木", "金", "土", "日"]

import easyfileio
from funcs import breakup, splice, num, opdict, cli, prints
from setTimeFuncs import monthDays
import dotenv
import asyncio
import sync

folder = 'calendar'
planDateS = easyfileio.content(folder, 'planDateSettings.txt', encode='cp932')



def getPlan(varName):
    setting = varName.fetch()
    fetchedSetting = []
    for i in setting:
        fetchedSetting.append(easyfileio.de_stringify_list(i, ","))
    return fetchedSetting

def planTimeLength(planTime):
    timeHour, timeMinute = breakup.time(planTime)
    if str(timeHour) == 'False':
        return '入力形式にエラーがあります', None
    elif num.isNum(timeHour) == False or num.isNum(timeMinute) == False:
        return '時間を入力してください', None
    elif timeHour >= 24 or timeHour < 0:
        return '入力された時間にエラーがあります', None
    elif timeMinute >= 60 or timeMinute < 0:
        return '入力された分数にエラーがあります', None
    return None, f'{timeHour}:{timeMinute:02d}'

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
    if not '/' in date:
        return False, False, False
    year, monthAndDate = splice.splice(date, '/', "str")
    monthofPlan, dateofPlan = splice.splice(monthAndDate, "/", "int")#年が書いてある場合のプログラム
    if num.dataType(year) != 'int':
        return False, False, False
    if monthofPlan > 12:
        return False, False, False
    if dateofPlan == False:#年が書いてない場合のプログラム
        monthofPlan = year
        dateofPlan = monthAndDate
        year = determine_year(monthofPlan, dateofPlan)
    elif num.dataType(monthofPlan) != 'int' or num.dataType(dateofPlan) != 'int':
        pass
    elif monthDays.checkDays(monthofPlan, year) >= dateofPlan:
        return int(year), monthofPlan, dateofPlan
    if year != None:
        return year, monthofPlan, dateofPlan
    return False, False, False

def askplanDate(date):
    dayList = []
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
        if firstYear == True:
            pass
        elif num.create(firstYear,firstMonth,firstDay)>num.create(lastYear,lastMonth,lastDay):
            lastYear += 1

        if lastYear == True and firstYear == True:
            pass
        elif not firstYear == False or not lastYear == False:
            dayList = firstYear, firstMonth, firstDay, lastYear, lastMonth, lastDay
            return dayList
    else:
        dayList = None, None, None
        dayList += checkDate(date)
        if not False in dayList:
            return dayList
    return None

async def askMultipleDates(text):
    while True:
        print(text)
        date = await asyncio.to_thread(input, '>> ')
        dateList = []
        tempDateList = []
        multipleDates = True
        firstYearList = []
        firstMonthList = []
        firstDayList = []
        lastYearList = []
        lastMonthList = []
        lastDayList = []

        error = False
        if ',' in date:
            tempDateList = date.split(',')
        else:
            tempDateList.append(date)

        for i in tempDateList:
            dateList.append(i.strip())
        
        returnedDateList = []
        for ilen, i in enumerate(dateList):
            returnedDateList = askplanDate(i)
            if returnedDateList == None:
                error = True
            elif returnedDateList[0] != None: #the first date must be none bc, i dont want 2/5-2/6 to have multiple dates(too complicated)
                multipleDates = False

            if ilen != 0 and multipleDates == False:
                error = True
            if error == False:
                firstYearList.append(returnedDateList[0])
                firstMonthList.append(returnedDateList[1])
                firstDayList.append(returnedDateList[2])
                lastYearList.append(returnedDateList[3])
                lastMonthList.append(returnedDateList[4])
                lastDayList.append(returnedDateList[5])
        if error == False:
            return firstYearList, firstMonthList, firstDayList, lastYearList, lastMonthList, lastDayList
        os.system("cls")
        prints.err("正しく入力してください")


def askOneDate(text): #for settings
    date = prints.ask(text)
    
    while True:
        returnDate = askplanDate(date)
        if returnDate != None:
            return askplanDate(date)
        os.system("cls")
        prints.err("正しく入力してください")

def checkSingleTime(time):
    error, outputTime = planTimeLength(time)
    if error != None:
        prints.err(outputTime)
    return outputTime, error
    
def checkStartToFinishTime(time):
    inputStartTime, inputEndTime = splice.splice(time, '-', 'str')
    error, startTime = planTimeLength(inputStartTime)
    if error == None:
        error, endTime = planTimeLength(inputEndTime)
    if error != None:
        return None, None, error
    return startTime, endTime, error


async def getTime(text):
    while True:
        print(text)
        time = await asyncio.to_thread(input, '>> ')
        if '-' in time:
            startTime, endTime, error = checkStartToFinishTime(time)
        else:
            startTime, error = checkSingleTime(time)
            endTime = None
        
        if error == None:
            break
        os.system('cls')
        prints.err(error)
    return startTime, endTime
        


        
def planExists(plan2, mainplan, plantyp):
    if not mainplan[0] == plan2[0] and plantyp == 'weekly':
        return False
    
    mainplantimeStartHour, mainplantimeStartMinute, mainplantimeEndHour, mainplantimeEndMinute = breakup.timeplan(mainplan)
    subplantimeStrtHour, subplantimeStartMinute, subplantimeEndHour, subplantimeEndMinute = breakup.timeplan(plan2)
    planTimeHour = mainplantimeStartHour-1
    planTimeMinute = 0
    while not mainplantimeEndHour < planTimeHour and not mainplantimeEndMinute > planTimeMinute:
        planTimeHour += 1
        for planTimeMinute in range(mainplantimeStartMinute, 61):
            if planTimeHour == subplantimeStrtHour and planTimeMinute == subplantimeStartMinute:
                return True
            if planTimeHour == subplantimeEndHour and planTimeMinute == subplantimeEndMinute:
                return True

def showPlans():
    planforDay = getPlan(planDateS)

    plandate = []
    plandateL = []
    plandateinfo = []
    plandatenumL = []
    for i in planforDay:
        dateSTARTSHOWINGLoc = 3
        dateDATELoc = 4
        dateTIMELoc = 5
        plandate = f'{i[dateNAMELoc]}（'
        if i[dateREMINDERLoc] == True:
            plandate += 'リマインダーあり'
        else:
            plandate += 'リマインダーなし'
        
        plandate += '）: '

        if i[dateDAYLoc] == None:
            pass
        else:
            plandate += f'毎{days[i[dateDAYLoc]]}曜日 {i[dateTIMELoc]} '

        if i[dateDATELoc] == True:
            pass
        elif i[dateDATELoc] == None:
            pass
        elif i[dateSTARTSHOWINGLoc] == None or i[dateSTARTSHOWINGLoc] == True:
            plandate += f' {i[dateDATELoc]}'
        else:
            plandate += i[dateSTARTSHOWINGLoc]

        if i[dateDATELoc] == None:
            pass
        elif i[dateDATELoc] == True:
            pass
        elif i[dateSTARTSHOWINGLoc] == None:
            pass
        elif type(i[dateSTARTSHOWINGLoc]) == str and type(i[dateDATELoc]) == str:
            plandate += f'から{i[dateDATELoc]}'
        else:
            plandate += 'まで'
        

        if i[dateSTARTSHOWINGLoc] == None:
            pass
        elif i[dateSTARTSHOWINGLoc] == True:
            pass
        elif type(i[dateSTARTSHOWINGLoc]) == str and type(i[dateDATELoc]) == str:
            pass
        else:
            plandate += f'{i[dateSTARTSHOWINGLoc]}'
        
        if i[dateDATELoc] == True:
            plandate += 'から'

        if not i[dateDAYLoc] == None:
            pass
        elif not i[dateTIMELoc] == None:
            plandate += f' {i[dateTIMELoc]}'

        plandateL.append(plandate)
        addToPlanDateInfo = ''
        for ilen,element in enumerate(i):
            if not ilen == 0:
                addToPlanDateInfo += ','
            addToPlanDateInfo += str(element)
        plandateinfo.append(addToPlanDateInfo)
        plandatenum = num.numify(f'{i[dateDATELoc]}{i[dateTIMELoc]}{i[timestamp]}')
        plandatenumL.append(plandatenum)
    planD = opdict.create(plandatenumL, plandateinfo)
    forSortingD = opdict.create(plandateL, plandatenumL)

    sortedplanD = opdict.sort(forSortingD, 'value')

    excludeSettings = []
    for i in sortedplanD:
        name, nothing = splice.splice(i, ':', 'str')
        if num.isNum(name) == True:
            print(i)
        for i2 in sortedplanD:
            nothing, createdTime = splice.splice(i2, ',', 'str')
            #print(bool(str(createdTime) == str(name)), name, createdTime)
            if num.isNum(name) == False:
                pass
            elif int(createdTime) == int(name):
                excludeSettings.append(i)

    for i in excludeSettings:
        del sortedplanD[i]

    cli.chooseScreen(sortedplanD)
    return planD, plandateinfo, sortedplanD

class EnterSchedule:
    def __init__(self):
        self.varNameToJapanese = {}

    async def check(self, indicator):
        while True:
            os.system('cls')
            print("入力した内容はこれでよろしいですか? y/n")
            print()
            outputL = []
            orderL = []
            for varValue, varName in self.varNameToJapanese.items():
                varOrder, varOutput = splice.splice(varValue, ".", "str")

                stringBeforeValue, stringAfterValue = splice.splice(varOutput, indicator, "str")

                orderL.append(varOrder)
                outputL.append(f'{stringBeforeValue}{varName}{stringAfterValue}')
            outputD = opdict.create(outputL, orderL)
            sOutputD = opdict.sort(outputD, 'value')
            for i in sOutputD:
                print(i)

            print()
            inputConfirmation = await asyncio.to_thread(input, ">> ")
            if inputConfirmation == 'n':
                return False
            elif inputConfirmation == 'y':
                return True
        
    async def enterDate(self, qString, stringForChecking):
        plan = []
        planshowStart = []
        plantoJ = ''
        firstYearList, firstMonthList, firstDateList, lastYearList, lastMonthList, lastDateList = await askMultipleDates(qString)
        for firstYear, firstMonth, firstDate, lastYear, lastMonth, lastDate in zip(firstYearList, firstMonthList, firstDateList, lastYearList, lastMonthList, lastDateList):
            if lastDate != lastDateList[0]: #the first three can be none, and if its none, than its the same so it doesnt work
                plantoJ += ', '
            if lastYear == True:
                plan.append(True)
            else:
                plan.append(f'{lastYear}/{lastMonth}/{lastDate}')

            if plan == True: #10/5-　みたいな入力
                planshowStart.append(f'{firstYear}/{firstMonth}/{firstDate}')
                plantoJ += f'{planshowStart}から'
            elif firstYear == True: #-10/5　みたいな出力
                planshowStart.append(True)
                plantoJ += f'{plan}まで'

            elif not firstYear == None: #10/5-10/6みたいな入力
                planshowStart.append(f'{firstYear}/{firstMonth}/{firstDate}')
                plantoJ += f'{planshowStart}から{plan}'
            else: #10/5 みたいな入力
                planshowStart.append(None)
                plantoJ += plan[len(plan)-1] #the last index of plan
            self.varNameToJapanese[stringForChecking] = plantoJ
        return planshowStart, plan

    async def enterTime(self, qString, stringForChecking):
        startTime, endTime = await getTime(qString)
        if endTime == None:
            self.varNameToJapanese[stringForChecking] = startTime
        else:
            self.varNameToJapanese[stringForChecking] = f'{startTime}から{endTime}'
        return startTime, endTime
        
    async def enterWeekDays(self, qString, stringForChecking):
        while True:
            os.system('cls')
            print(qString)
            cli.chooseScreen(days)
            try:
                chosenDays = int(await asyncio.to_thread(input, ">> "))-1
                self.varNameToJapanese[stringForChecking] = days[chosenDays]
                return chosenDays
            except:
                pass

    async def enterName(self, qString, stringForChecking):
        while True:
            print(qString)
            planName = await asyncio.to_thread(input, '>> ')
            if not planName == None:
                self.varNameToJapanese[stringForChecking] = planName
                return planName
            
    async def enterPlan(self, qString, stringForChecking):
        while True:
            print(qString)
            planD, plandateinfo, sortedplanD = showPlans()
            print(f'{len(sortedplanD)+1}.全部')
            rawPlanNum = await asyncio.to_thread(input, '>> ')
            if rawPlanNum == len(sortedplanD)+1:
                self.varNameToJapanese[stringForChecking] = '全て'
                return 2, None
            rawplan = cli.choosing(rawPlanNum, sortedplanD)
            plan = planD[rawplan]
            planlist = easyfileio.de_stringify_list(plan, ',')
            planNum = planlist[timestamp]
            if not plan == None:
                self.varNameToJapanese[stringForChecking] = planlist[dateNAMELoc]
                return planlist[dateTypLoc], planNum
            
    async def setReminder(self, qString, stringForChecking):
        while True:
            print(qString)
            askReminder = await asyncio.to_thread(input, '>> ')
            if askReminder == 'y':
                self.varNameToJapanese[stringForChecking] = 'あり'
                return True
            elif askReminder == 'n':
                self.varNameToJapanese[stringForChecking] = 'なし'
                return False

def show_temp_date(plan_date):
    temp_plan = '\033[1m'
    for ilen, i in enumerate(plan_date):
        temp_plan += i
        if ilen != len(plan_date)-1:
            temp_plan += '、'
        else:
            temp_plan += '\033[0m'
    return temp_plan


async def main():
    dotenv.load_dotenv('supabaseLoginInfo/cloudLoginInfo.env')
    supabaseURL = os.getenv("SUPABASE_URL")
    supabaseKey = os.getenv("SUPABASE_KEY")
    sync_plans = sync.get_cloud(supabaseURL, supabaseKey)
    asyncio.create_task(sync_plans.main())
    
    cloud_plan_var = 'plansTable'
    chooseSetting = None
    timeTypToSet = None

    while True:
        if chooseSetting == None:
            newPlan = False
            
            planName = None
            planshowStart = None
            plan = None
            dayPlanLen = None
            chosenDays = None
            expireStart = None
            expireEnd = None
            endTime = None
            planIsDone = 0
            os.system('cls')
            print()
            print("空いてない・空いてないかもしれない日を設定してください : ")
            print()

            for lenI, i in enumerate(settingsDict):
                print(f'{lenI+1}. {i}')
            print()
            try:
                chooseSetting = settingsDict[list(settingsDict)[int(await asyncio.to_thread(input, ">> "))-1]]#これは、settingsDictと、inputを照らし合わせ、設定の変数を取得するプログラムです
            except:
                    pass
            
        if chooseSetting != 4 and timeTypToSet == None:
            os.system('cls')
            timeSettingD = {'日にち設定': 0, '曜日設定': 1, '除外日程設定': 2, '期限付き設定': 3, '戻る': 4}
            cli.chooseScreen(timeSettingD)
            print()
            timeTypInput = await asyncio.to_thread(input, '>> ')
            timeTypToSet = cli.choosing(timeTypInput, timeSettingD)
        
        if timeTypToSet == 4:
            timeTypToSet = None
            chooseSetting = None

        elif timeTypToSet == 0:
            dateSettings = EnterSchedule()
            os.system("cls")
            planshowStart, plan = await dateSettings.enterDate("予定日の日にちを入力してください (Ex. 10/5, 10/6-12/2)", '1.予定のある日 : a')
            if not (not planshowStart[0] == None and chooseSetting == 0):
                os.system('cls')
                dayPlanLen, endTime = await dateSettings.enterTime(f'{show_temp_date(plan)}\n期限を教えてください（Ex. 01:00, end）', '2.期限時間 : a')
            os.system('cls')
            planName = await dateSettings.enterName('予定名を入力してください', '0.予定名 : a')
            haveReminder = await dateSettings.setReminder('リマインダを設定しますか y/n', '3.リマインダーa')
            newPlan = await dateSettings.check('a')

        elif timeTypToSet == 1:
            weekdaySetting = EnterSchedule()
            os.system('cls')
            chosenDays = await weekdaySetting.enterWeekDays('曜日を教えてください', '0.a曜日\n')
            os.system('cls')
            dayPlanLen, endTime = await weekdaySetting.enterTime(f'期限を教えてください（Ex. 01:00, end）', '2.期限時間 : a')
            os.system("cls")
            while True:
                planshowStart, plan = await weekdaySetting.enterDate("期間を教えてください (Ex. 10/6-12/2)", '3.期間 : a')
                if planshowStart[0] == None:
                    os.system('cls')
                    prints.err('期間を正しく入力してください (Ex.-10/6, 10/6-)')
                else:
                    break
            os.system('cls')
            planName = await weekdaySetting.enterName('予定名を入力してください', '1.予定名 : a')
            haveReminder = await weekdaySetting.setReminder('リマインダを設定しますか y/n', '3.リマインダーa')
            newPlan = await weekdaySetting.check('a')
        
        elif timeTypToSet == 2:
            weekdayExcludedSetting = EnterSchedule()
            planIsDone = None
            os.system('cls')
            chooseSetting, planName = await weekdayExcludedSetting.enterPlan('除外設定を設定する日程を設定してください', '0.除外に該当する予定：a')
            os.system('cls')
            planshowStart, plan = await weekdayExcludedSetting.enterDate("除外する期間を教えてください (Ex. 10/5, 10/6-12/2)", '1.期間 : a')
            os.system('cls')
            haveReminder = await weekdayExcludedSetting.setReminder('リマインダを設定しますか y/n', '3.リマインダーa')
            newPlan = await weekdayExcludedSetting.check('a')

        elif timeTypToSet == 3:
            expireSetting = EnterSchedule()
            os.system("cls")
            planshowStart, plan = await expireSetting.enterDate("予定日の日にちを入力してください (Ex. 10/5, 10/6-12/2)", '1.予定のある日 : a')
            if not (not planshowStart[0] == None and chooseSetting == 0):
                os.system('cls')
                dayPlanLen, endTime = await expireSetting.enterTime(f'{show_temp_date(plan)}\n時間を教えてください（Ex. 01:00, end）', '2.時間 : a')
            os.system('cls')
            expireStart, expireEnd = await expireSetting.enterDate(f'{show_temp_date(plan)}\n期限を教えてください(Ex. 10/5, 10/6-12/2)"', '3.期限 : a')
            os.system('cls')
            planName = await expireSetting.enterName('予定名を入力してください', '0.予定名 : a')
            haveReminder = await expireSetting.setReminder('リマインダを設定しますか y/n', '3.リマインダーa')
            newPlan = await expireSetting.check('a')


        if chooseSetting == 4:
            os.system('cls')
            loading_num = 1
            while True:
                update_instance = sync_plans.return_instance()
                if update_instance != 'updating online plans' and update_instance != 'finished':
                    prints.loading(loading_num)
                    print(f'{update_instance}...')
                else:
                    break
                loading_num += 1
                await asyncio.sleep(0.5)
                os.system('cls')
            os.system('cls')

            planforDay = getPlan(planDateS)
            
            planD, plandateinfo, sortedplanD  = showPlans()

            chooseNum = None
            chooseNum = input('>> ')
            dateToChange = cli.choosing(chooseNum, sortedplanD)

            if not dateToChange == None:
                import supabase
                cloud_func: supabase.AsyncClient = await supabase.acreate_client(supabaseURL, supabaseKey)
                while True:
                    os.system('cls')
                    change = 0
                    planDateLoc = plandateinfo.index(planD[dateToChange])
                    planDateOriginal = planforDay[planDateLoc]
                    chooseNum = None
                    print(planDateOriginal[dateNAMELoc])
                    print()
                    print('何を変更しますか')
                    thingsToChnangeD = {'予定名': 0, '予定日時': 1, '予定時刻': 2, 'リマインダー設定': 5, '除外日程': 4, '削除': 3}
                    cli.chooseScreen(thingsToChnangeD)
                    chooseNum = input('>> ')
                    delete = 0
                    settingToChange = cli.choosing(chooseNum, thingsToChnangeD)
                    if settingToChange == 0:
                        while True:
                            changedName = prints.ask('予定名を何に変更しますか？')
                            if not changedName == None:
                                planDateOriginal[dateNAMELoc] = changedName
                                print('saving...')
                                await cloud_func.table(cloud_plan_var).update({"dateNAME": planDateOriginal[dateNAMELoc]}).eq('timestamp', planDateOriginal[timestamp]).execute()
                                change = 1
                                break
                    elif settingToChange == 1:
                        firstYear, firstMonth, firstDate, lastYear, lastMonth, lastDate = askOneDate('変更日時')
                        if firstYear == None:
                            planDateOriginal[dateSTARTSHOWINGLoc] = None
                        elif firstYear == True:
                            planDateOriginal[dateSTARTSHOWINGLoc] = True
                        else:
                            planDateOriginal[dateSTARTSHOWINGLoc] = f'{firstYear}/{firstMonth}/{firstDate}'
                        
                        if lastYear == True:
                            planDateOriginal[dateDATELoc] = True
                        else:
                            planDateOriginal[dateDATELoc] = f'{lastYear}/{lastMonth}/{lastDate}'
                        print('saving...')
                        await cloud_func.table(cloud_plan_var).update({'dateSTARTSHOWING': planDateOriginal[dateSTARTSHOWINGLoc], 'dateDATE': planDateOriginal[dateDATELoc]}).eq('timestamp', planDateOriginal[timestamp]).execute()
                        change = 1
                    elif settingToChange == 2:
                        planDateOriginal[dateTIMELoc], planDateOriginal[dateTIMEENDLoc] = await getTime("予定時刻を教えてください")
                        hour, minute = planDateOriginal[dateTIMELoc].split(':')
                        planTime = f'{int(hour):02d}:{int(minute):02d}:00'
                        if planDateOriginal[dateTIMEENDLoc] == None:
                            endtime = None
                        else:
                            hour, minute = planDateOriginal[dateTIMEENDLoc].split(':')
                            endTime = f'{int(hour):02d}:{int(minute):02d}:00'
                        await cloud_func.table(cloud_plan_var).update({'dateTIME': planTime, 'dateTIMEEND': endTime}).eq('timestamp', planDateOriginal[timestamp]).execute()
                        change = 1
                    elif settingToChange == 3:
                        delete = prints.ask('本当に削除しますか？ y/n')
                        if planDateOriginal[dateREMINDERLoc] == True:
                            print('saving...')
                            await cloud_func.table(cloud_plan_var).delete().eq('timestamp', planDateOriginal[timestamp]).execute()
                        change = 1

                    elif settingToChange == 5:
                        
                        if planDateOriginal[dateREMINDERLoc] == True:
                            reminderSetttingStr = 'off'
                            changeREMINDERto = False
                        else:
                            reminderSetttingStr = 'on'
                            changeREMINDERto = True

                        while True:
                            changeReminderSetting = prints.ask(f'リマインダーを{reminderSetttingStr}に設定しますか y/n')
                            if changeReminderSetting == 'n':
                                pass
                            elif changeREMINDERto == True:
                                print('saving...')
                                saveDict = {'timestamp': planDateOriginal[timestamp], 'dateSTARTSHOWING': planDateOriginal[dateSTARTSHOWINGLoc], 'dateDATE': planDateOriginal[dateDATELoc], 'dateTIME': planDateOriginal[dateTIMELoc], 'dateDAY': planDateOriginal[dateDAYLoc], 'dateNAME': planDateOriginal[dateNAMELoc]}
                                await cloud_func.table(cloud_plan_var).insert(saveDict).execute()
                            elif changeREMINDERto == False:
                                print('saving...')
                                await cloud_func.table(cloud_plan_var).delete().eq('timestamp', planDateOriginal[timestamp]).execute()

                            if changeReminderSetting == 'y':
                                planDateOriginal[dateREMINDERLoc] = changeREMINDERto
                                change = 1
                                break
                            elif changeReminderSetting == 'n':
                                change = 1
                                break
                            else:
                                pass
                                

                    if change == 0:
                        pass
                    elif change == 1:
                        break
                if delete == 'y':
                    planDateS.delete(planDateLoc)
                else:
                    planDateS.change(planDateLoc, easyfileio.stringify_list(planDateOriginal, ','))
                chooseSetting = None

        if newPlan == True:
            import time
            import supabase
            cloud_func: supabase.AsyncClient = await supabase.acreate_client(supabaseURL, supabaseKey)
            os.system('cls')
            loading_num = 1
            while True:
                update_instance = sync_plans.return_instance()
                if update_instance != 'updating online plans' and update_instance != 'finished':
                    prints.loading(loading_num)
                    print(f'{update_instance}...')
                else:
                    break
                loading_num += 1
                await asyncio.sleep(0.5)
                os.system('cls')
            os.system('cls')

            plantyp = chooseSetting
            timeCreated = int(time.time())
            save_string = ''
            saveDict = []
            ilen = -1
            for istart, iend in zip(planshowStart, plan):
                ilen += 1
                if ilen > 0:
                    save_string += '\n'
                save_string += easyfileio.stringify_list([timeCreated+ilen, plantyp, planName, istart, iend, dayPlanLen, endTime, expireStart, expireEnd, chosenDays, haveReminder, planIsDone], ',')
                if haveReminder == True:
                    saveDict.append({'timestamp': timeCreated+ilen, 'dateTYPE': plantyp, 'dateSTARTSHOWING': istart, 'dateDATE': iend, 'dateTIME': dayPlanLen, 'dateTIMEEND': endTime, 'dateDAY': chosenDays, 'dateNAME': planName, 'dateEXPIRESTART': expireStart, 'dateEXPIREEND': expireEnd})
            print('saving...')
            planDateS.save(save_string)
            if not saveDict == []:
                await cloud_func.table(cloud_plan_var).insert(saveDict).execute()

            chooseSetting = None
        timeTypToSet = None

asyncio.run(main())