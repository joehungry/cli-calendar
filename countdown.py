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
from funcs import cli
showTypD = {'予定表示': 0, 'タスク表示': 1}

os.system('cls')
print('何を表示しますか：')
print()
cli.chooseScreen(showTypD)

import datetime, asyncio
#print(True)
from funcs import num, compare, breakup, prints
#print(True)
import dotenv
#print(True)
#import supabase
#print(True)
import easyfileio, sync
#print(True)

cloud_plan_var = 'plansTable'

dayRightNow = datetime.datetime.now()
fDayRightNow = f'{dayRightNow.year}/{dayRightNow.month}/{dayRightNow.day}'

dayRightNowNum = num.numify(fDayRightNow)
timeRightNow = num.numify(f'{fDayRightNow} {dayRightNow.hour}:{dayRightNow.minute}')

dotenv.load_dotenv('supabaseLoginInfo/cloudLoginInfo.env')
supabaseURL = os.getenv("SUPABASE_URL")
supabaseKey = os.getenv("SUPABASE_KEY")


def nearestWeekday(weekday, refDay, dayinfo):
    refYear, refMonth, refDate = breakup.date(refDay)
    rawRefDate = datetime.date(refYear, refMonth, refDate)
    refWeekday = rawRefDate.weekday()
    countDays = 0
    refToWeekday = refWeekday
    while not refToWeekday == weekday:
        countDays += 1
        refToWeekday = num.cap(refWeekday+countDays, 7)

    rawDeadlineDate = rawRefDate + datetime.timedelta(days=countDays)
    deadlineDate = rawDeadlineDate.strftime('%Y/%m/%d')

    onlyTimeNow =  num.numify(dayRightNow.strftime('%H%M'))
    onlyTimePlan = num.numify(dayinfo[dateTIMELoc])


    if num.numify(deadlineDate) == num.numify(fDayRightNow) and onlyTimeNow > onlyTimePlan:
        deadlineDate = rawDeadlineDate + datetime.timedelta(days=7)
    return deadlineDate



async def main():
    sync_plans = sync.get_cloud(supabaseURL, supabaseKey)
    #cloud_func: supabase.AsyncClient = await supabase.acreate_client(supabaseURL, supabaseKey)
    asyncio.create_task(sync_plans.main())

    os.system('cls')
    print('何を表示しますか：')
    print()
    cli.chooseScreen(showTypD)
    typChooseInput = await asyncio.to_thread(input, '>> ')
    typChooseNum = cli.choosing(typChooseInput, showTypD)

    from funcs import opdict
    if typChooseNum == 1:
        from funcs import epochTime
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

        planDateS = easyfileio.content('calendar', 'planDateSettings.txt', encode='cp932')
        planDateContentRaw = planDateS.fetch()
        planDateContent = [easyfileio.de_stringify_list(plan, ",") for plan in planDateContentRaw]



        activePlanDateL = {}
        weekdayPlanDateL = []
        compareAndDeleteD = {}
        loading_num = 1
        prints.loading(loading_num)
        for dayinfo in planDateContent:
            if dayinfo[dateTypLoc] == 0:
                pass
            elif not dayinfo[dateDAYLoc] == None:
                weekdayPlanDateL.append(dayinfo)  
        for dayinfo in weekdayPlanDateL:
            startingDay = dayinfo[dateSTARTSHOWINGLoc]

            if startingDay == True:
                startingDay = fDayRightNow
            if len(str(dayinfo[dateDONELoc])) == 1:
                lastTimeCompleted = startingDay
            else:
                lastTimeCompleted = dayinfo[dateDONELoc]
            lastTimeDeadline = nearestWeekday(dayinfo[dateDAYLoc], lastTimeCompleted, dayinfo)
            thisWeekDeadline = nearestWeekday(dayinfo[dateDAYLoc], fDayRightNow, dayinfo)
            if breakup.date(lastTimeDeadline) < breakup.date(thisWeekDeadline):
                doneVar = 0
            else:
                doneVar = dayinfo[dateDONELoc]
            planDateContent.remove(dayinfo)
            if (not dayinfo[dateDATELoc] == True) and breakup.date(thisWeekDeadline) > breakup.date(dayinfo[dateDATELoc]):
                pass
            elif breakup.date(fDayRightNow) < breakup.date(startingDay):
                pass
            else:
                activePlanDateL[easyfileio.stringify_list([doneVar, dayinfo[timestamp], dayinfo[dateNAMELoc]], '.')] = epochTime.fromDate(thisWeekDeadline, dayinfo[dateTIMELoc])
                compVar = ''
                for ilen, i in enumerate(dayinfo):
                    if not ilen == 0:
                        compVar += ','
                    compVar += str(i)

                compareAndDeleteD[compVar] = epochTime.fromDate(thisWeekDeadline, dayinfo[dateTIMELoc])
        loading_num += 1
        prints.loading(loading_num)
        for ilen,dayinfo in enumerate(planDateContent):
            startShowing = dayinfo[dateSTARTSHOWINGLoc]
            startShowingNum = num.numify(startShowing)
            if startShowingNum > dayRightNowNum and not startShowing == None:
                pass
            elif not dayinfo[dateTypLoc] == 1 and not dayinfo[dateTypLoc] == 2:
                pass
            else:
                activePlanDateL[easyfileio.stringify_list([dayinfo[dateDONELoc],dayinfo[timestamp],dayinfo[dateNAMELoc]], '.')] = epochTime.fromDate(dayinfo[dateDATELoc], dayinfo[dateTIMELoc])
                compVar = ''
                for ilen, i in enumerate(dayinfo):
                    if not ilen == 0:
                        compVar += ','
                    compVar += str(i)

                compareAndDeleteD[compVar] = epochTime.fromDate(dayinfo[dateDATELoc], dayinfo[dateTIMELoc])
        loading_num += 1
        prints.loading(loading_num)
        

        sortedActivePlanDateL = opdict.sort(activePlanDateL, 'value')
        soretedCompareAndDeleteD = opdict.sort(compareAndDeleteD, 'value')
        loading_num += 1
        os.system('cls')

        if len(sortedActivePlanDateL) == 0:
            while True:
                print('タスク：')
                print()
                print(None)
                input()
                os.system('cls')

        import win32api, time
        while True:
            print('タスク：')
            print()
            #len = 0
            for rawplanName, planTime in sortedActivePlanDateL.items():
                #len += 1
                countdown4Plan = int(planTime)-time.time()
                countdownDays = int(countdown4Plan/86400)
                countdownHours = int((countdown4Plan-countdownDays*86400)/3600)
                countdownMinutes = int((countdown4Plan-countdownHours*3600-countdownDays*86400)/60)#
                countdownSeconds = int(countdown4Plan-countdownHours*3600-countdownDays*86400-countdownMinutes*60)#-countdownMinutes*60
                
                planNameL = easyfileio.de_stringify_list(rawplanName, '.')
                planName = planNameL[2]

                if countdown4Plan < 0:
                    pass
                elif planNameL[0] == 0:
                    print(f'UNTIL {planName}: ')
                    print(f'{countdownDays}日　{countdownHours}時間　{countdownMinutes}分　{countdownSeconds}秒')
                    print()
            print()
            print()
            print('完了：')
            for rawplanName, planTime in sortedActivePlanDateL.items():
                planNameL = easyfileio.de_stringify_list(rawplanName, '.')
                planName = planNameL[2]
                if not planNameL[0] == 0:
                    print(planName)
            time.sleep(1)
            os.system('cls')
            changeScreen = win32api.GetKeyState(0x0D)
            if changeScreen < 0:
                while True:
                    deleteKeyD = soretedCompareAndDeleteD
                    keyDeletingList = []
                    truelen = 0
                    for i in sortedActivePlanDateL.keys():
                        activePlanList = easyfileio.de_stringify_list(i, '.')
                        if activePlanList[0] == 0:
                            truelen += 1
                            print(f'{truelen}.{activePlanList[2]}')
                        else:
                            keyDeletingList.append(i)

                    for completeKey in keyDeletingList:
                        completedPlanElement = easyfileio.de_stringify_list(completeKey, '.')
                        completedPlanName = completedPlanElement[2]
                        allPlans = opdict.sort(deleteKeyD, 'key')
                        for allPlansElement in allPlans:
                            if completedPlanName in allPlansElement:
                                del deleteKeyD[allPlansElement]
                    print()
                    try:
                        completePlan = int(input('>> '))-1
                        break
                    except:
                        os.system('cls')   
                
                updateData = list(deleteKeyD.keys())
                is_valid_plan = True
                if completePlan >= len(updateData):
                    is_valid_plan = False

                if is_valid_plan == True:
                    originalIndex = planDateContentRaw.index(updateData[completePlan])
                    updatedData = easyfileio.de_stringify_list(updateData[completePlan], ',')

                    #updatedData[dateNAMELoc] = updatedData[dateNAMELoc]
                    #updatedData[dateDONELoc] = fDayRightNow
                    sortedActivePlanDateL = opdict.replaceKey(easyfileio.stringify_list([fDayRightNow, updatedData[timestamp], updatedData[dateNAMELoc]], '.'), f'0.{updatedData[timestamp]}.{updatedData[dateNAMELoc]}', sortedActivePlanDateL)
                    updatedData[dateDONELoc] = str(fDayRightNow)
                if is_valid_plan == False:
                    pass
                elif updatedData[dateREMINDERLoc] == True:
                    pass
                    #await cloud_func.table(cloud_plan_var).update({"dateDONE": str(fDayRightNow)}).eq('timestamp', updatedData[timestamp]).execute() #so that it doesn't tell me anything online
                

                if is_valid_plan == True:
                    planDateS.change(originalIndex, easyfileio.stringify_list(updatedData, ','))
            os.system('cls')


    elif typChooseNum == 0:
        from funcs import splice
        print('予定を見たい月を教えて下さい')
        showMonth = input('>> ')
        try:
            if '/' in showMonth:
                year, month = splice.splice(showMonth, '/', 'int')
            else:
                year = dayRightNow.year
                month = int(showMonth)
        except:
            year = dayRightNow.year
            month = dayRightNow.month

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

        planDateS = easyfileio.content('calendar', 'planDateSettings.txt', encode='cp932')
        planDateContentRaw = planDateS.fetch()
        planDateContent = [easyfileio.de_stringify_list(plan, ",") for plan in planDateContentRaw]


        planDateD = {}
        planDateLongD = {}
        planDateDayD = {}
        planDateDayExludedD = {}
        plandateTimestamp = [easyfileio.stringify_list(i, ',')[0] for i in planDateContent]
        for planDate in planDateContent:
            plandateList = easyfileio.stringify_list(planDate, ',')
            if not planDate[dateTypLoc] == 0 and not planDate[dateTypLoc] == 2:
                pass
            elif not planDate[dateDAYLoc] == None:
                numifiedNum = num.numify(f'{planDate[dateTIMELoc]} {planDate[dateTIMEENDLoc]}')
                planDateDayD[plandateList] = numifiedNum
            elif planDate[dateNAMELoc] in plandateTimestamp: #除外日程を設定
                numifiedNum = num.numify(planDate[dateSTARTSHOWINGLoc])
                planDateDayExludedD[plandateList] = numifiedNum
            elif planDate[dateSTARTSHOWINGLoc] == None or planDate[dateTypLoc] != 0: 
                numifiedNum = num.numify(f'{planDate[dateDATELoc]} {planDate[dateTIMELoc]} {planDate[dateTIMEENDLoc]}')
                planDateD[plandateList] = numifiedNum
            else:
                numifiedNum = num.numify(planDate[dateSTARTSHOWINGLoc])
                planDateLongD[plandateList] = numifiedNum

        sortedPlandateD = opdict.sort(planDateD, 'value') #2/5
        sortedPlanDateLongD = opdict.sort(planDateLongD, 'value') #2/5-2/10
        sortedPlanDateDayD = opdict.sort(planDateDayD, 'value') #every sunday 7pm
        sortedPplanDateDayExludedD = opdict.sort(planDateDayExludedD, 'value')

        import calendar
        dateName = ["月", "火", "水", "木", "金", "土", "日"]
        plan_num = 0
        #plan_num += 1
        #print(plan_num)
        change_plan = False
        while True:
            os.system('cls')
            print(f'{year}年　{month}月')
            os.system('cls')
            print(f'{year}年　{month}月')#こうしないとなんか意味わかんないバグ出てきて殺したくなったから適当に解決した
            hasPlan = False
            if year == dayRightNow.year and month == dayRightNow.month:
                monthIsNow = True
            else:
                monthIsNow = False
            for week in calendar.monthcalendar(year, month):
                for date,day in enumerate(week):
                    dayHasPlan = False
                    if not day == 0:
                        dayToCheck = f'{year}/{month}/{day}'
                        nowday = num.numify(dayToCheck)
                        dayprinted = False
                        color = '\033[0m'
                        dayExcluded = False
                        if monthIsNow == True and day == dayRightNow.day:
                            print('\033[1m' + '\033[36m', end='')
                            color = '\033[4m'
                        show_plan = ''
                        for plandate in sortedPplanDateDayExludedD:
                            planinfo = easyfileio.de_stringify_list(plandate, ',')
                            #print(plandate)
                            #input()
                            planstart = num.numify(planinfo[dateSTARTSHOWINGLoc])
                            planend = num.numify(planinfo[dateDATELoc])
                            if planend == nowday:
                                dayExcluded = planinfo[dateNAMELoc]
                            elif planstart == 0:
                                pass
                            elif compare.isSandwitchNum(nowday, planstart, planend) == True:
                                dayExcluded = planinfo[dateNAMELoc]


                        for plandate in sortedPlanDateDayD:
                            planinfo = easyfileio.de_stringify_list(plandate, ',')
                            planstart = num.numify(planinfo[dateSTARTSHOWINGLoc])
                            planend = num.numify(planinfo[dateDATELoc])
                            isStarted = False
                            isNotOver = False
                            showTime = None

                            if planinfo[dateDONELoc] != 0:
                                pastDeadline = nearestWeekday(planinfo[dateDAYLoc], fDayRightNow, planinfo)
                            else:
                                pastDeadline = 0


                            if planinfo[dateSTARTSHOWINGLoc] == True:
                                isStarted = True
                            elif planstart <= nowday:
                                isStarted = True

                            if planinfo[dateDATELoc] == True:
                                isNotOver = True
                            elif planend >= nowday:
                                isNotOver = True

                            if planinfo[dateTIMEENDLoc] != None:
                                showTime = f'{planinfo[dateTIMELoc]}-{planinfo[dateTIMEENDLoc]}'
                            else:
                                showTime = f'{planinfo[dateTIMELoc]}'

                            if dayRightNowNum > nowday:
                                pass
                            elif isStarted == False:
                                pass
                            elif isNotOver == False:
                                pass
                            elif not date == planinfo[dateDAYLoc]:
                                pass
                            elif dayExcluded == None:
                                pass
                            elif dayExcluded == planinfo[timestamp]:
                                pass
                            elif nowday <= num.numify(pastDeadline): #if its complete, dont do anything
                                pass
                            elif dayprinted == False:
                                show_plan += f'{dayToCheck}（{dateName[date]}）:\n'
                                show_plan += f'{color}{planinfo[dateNAMELoc]}: {showTime}\n'

                                dayprinted = True
                                hasPlan = True
                                dayHasPlan = True
                            else:
                                show_plan += f'{color}{planinfo[dateNAMELoc]}: {showTime}\n'

                                hasPlan = True
                                dayHasPlan = True

                        for plandate in sortedPlanDateLongD:
                            planinfo = easyfileio.de_stringify_list(plandate, ',')
                            planstart = num.numify(planinfo[dateSTARTSHOWINGLoc])
                            planend = num.numify(planinfo[dateDATELoc])

                            if compare.isSandwitchNum(nowday, planstart, planend) == False:
                                pass
                            elif nowday < dayRightNowNum:
                                pass
                            elif dayExcluded == None:
                                pass
                            elif dayExcluded == planinfo[timestamp]:
                                pass
                            elif dayprinted == False:
                                show_plan += f'{dayToCheck}（{dateName[date]}）:\n'
                                show_plan += f'{color}{planinfo[dateNAMELoc]}\n'

                                dayprinted = True
                                hasPlan = True
                                dayHasPlan = True
                            else:
                                show_plan += planinfo[dateNAMELoc]

                                hasPlan = True
                                dayHasPlan = True

                        for plandate in sortedPlandateD:
                            planinfo = easyfileio.de_stringify_list(plandate, ',')

                            if planinfo[dateTIMEENDLoc] != None:
                                showTime = f'{planinfo[dateTIMELoc]}-{planinfo[dateTIMEENDLoc]}'
                            else:
                                showTime = f'{planinfo[dateTIMELoc]}'

                            if not dayToCheck == planinfo[dateDATELoc]:
                                pass
                            elif dayExcluded == None:
                                pass
                            elif dayExcluded == planinfo[timestamp]:
                                pass
                            elif planinfo[dateDONELoc] != 0:
                                pass
                            elif dayprinted == False:
                                show_plan += f'{dayToCheck}（{dateName[date]}）:\n'
                                show_plan += f'{color}{planinfo[dateNAMELoc]}: {showTime}\n'

                                dayprinted = True
                                hasPlan = True
                                dayHasPlan = True
                            else:
                                show_plan += f'{planinfo[dateNAMELoc]}: {showTime}\n'

                                hasPlan = True
                                dayHasPlan = True

                    if dayHasPlan != True:
                        pass
                    elif change_plan == True:
                        print(f'{plan_num + 1}. ', end='')
                        plan_num += 1
                    if dayHasPlan == True:
                        print(f'{show_plan}\033[0m')
                    elif monthIsNow == True and day == dayRightNow.day:
                        print(f'{dayToCheck}（{dateName[date]}）')
                        print(None)
                        print()
                        print('\033[0m', end='')
            if hasPlan == False:
                print(None)
            addNum = 1
            command = input()
            if command == 'back':
                addNum = -1
            if command == 'change':
                change_plan = True
            else:
                monthCap = month + addNum
            month = num.cap(monthCap-1, 12)+1
            if change_plan == True:
                pass
            elif month == 1:
                year += 1
    else:
        os.system('cls')
        input('incorrect input:\nclosing program')

asyncio.run(main())