import os, easyfileio
from funcs import cli, splice, opdict, prints

updateLocContent = easyfileio.content('updateFolder', 'updateLoc.txt')
updateLocContent.fetch()

#variableのデフォルトを書いて
updateStrContent = easyfileio.content('updateFolder', 'what to make variable of new loc.txt')
updateStrContent.fetch()

countdouwnContent = easyfileio.content(None, 'countdown.py')
countdouwnContent.fetch()

settingContent = easyfileio.content(None, 'setting.py')
settingContent.fetch()

scheduleContent = easyfileio.content('calendar', 'planDateSettings.txt', 'encode:cp932')
settingContent.fetch()

countdownProgram = countdouwnContent.fetch()

LocList = []
for ilen, i in enumerate(countdownProgram):
    if not i == '':
        LocList.append(i)
    else:
        whereToFindfinalLoc = ilen
        break

optionD = {'ファイル作成': 0, 'アップデート': 1}


while True:
    print('何をしますか')
    cli.chooseScreen(optionD)
    print()
    rawOption = input('>> ')
    optionchosen = cli.choosing(rawOption, optionD)
    if optionchosen == 0:
        printLoc = ''
        for ilen, i in enumerate(LocList):
            printLoc += f'{i}\n'
        updateLocContent.save(printLoc, overwrite=True)
    elif optionchosen == 1:
        updatedLocD = {}
        pastLocD = {}
        updatedLoc = updateLocContent.fetch()
        for i in updatedLoc:
            locVar, locNum = splice.splice(i, ' = ', 'str')
            updatedLocD[locVar] = int(locNum)
        for i in LocList:
            locVar, locNum = splice.splice(i, ' = ', 'str')
            pastLocD[locVar] = int(locNum)
        pastKeySortedD = opdict.sort(pastLocD, 'value')
        keyToSort = {}
        for var in pastKeySortedD:
            if not var in updatedLocD:
                pass
            else:
                keyToSort[var] = updatedLocD[var]
        for var in updatedLocD:
            if not var in pastKeySortedD:
                keyToSort[var] = updatedLocD[var]
        
        
        rawSchedule = scheduleContent.fetch()
        extractedSchedule = []
        for i in rawSchedule:
            extractedSchedule.append(easyfileio.de_stringify_list(i, ','))
        putInThisString = updateStrContent.fetch()
        while len(extractedSchedule[0])-1 < max(keyToSort.values()):
            for i in extractedSchedule:
                i.append(putInThisString[max(keyToSort.values())-len(extractedSchedule[0])])
        trueOrder = list(keyToSort.values())
        scheduleTempL = []
        filalSchedule = []
        for scdle in extractedSchedule:
            while len(scheduleTempL)-1 < max(keyToSort.values()):
                scheduleTempL.append(None)
            for oldLoc, newLoc in enumerate(trueOrder):
                scheduleTempL[newLoc] = scdle[oldLoc]
            filalSchedule.append(scheduleTempL)
            scheduleTempL = []


        saveListVar = ''
        for ilen, i in enumerate(filalSchedule):
            saveListVar += f'{easyfileio.stringify_list(i, ',')}\n'
            os.system('cls')
        scheduleContent.delete_file()
        scheduleContent.save(saveListVar)

        updatedLocCombined = ''
        for i in updatedLoc:
            updatedLocCombined += f'{i}\n'
        updatedLocCombined += '\n'
        settingContent.fetch()
        while not countdownProgram[0] == '':
            del countdownProgram[0]
            countdouwnContent.deleteBulk([0])
            settingContent.deleteBulk([0])
        countdouwnContent.change(0, updatedLocCombined)
        settingContent.change(0, updatedLocCombined)
        os.system('cls')
        input('タスクを完了しました...')
        break