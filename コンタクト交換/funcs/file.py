import os
import stat

try:
    from funcs import num
except:
    import num

def autoCreate(var):
    if not os.path.exists(var):
        os.makedirs(var)

def exists(file):
    try:
        with open(file, 'r') as o:
            return True
    except FileNotFoundError:
        return False
    
def lockFile(file):
    if os.path.exists(file):
        os.chmod(file, stat.S_IRUSR)

def saveJSON(file, JSON):
    if os.path.exists(file):
        os.chmod(file, stat.S_IWUSR)
    with open(file, 'a') as o:
        o.writelines(str(JSON))
        o.writelines('\n')
    os.chmod(file, stat.S_IRUSR)

def fetchList(fileList, spliceSign):
    strippedList = []
    stripVar = ''
    for iLen , i in enumerate(fileList):
        if i == spliceSign:
            strippedList.append(stripVar)
            stripVar = ''
        elif i == '[' or i == ']':
            pass
        else:
            stripVar += str(i)
    strippedList.append(stripVar)
    correctList = []
    for i in strippedList:
        if i == 'False':
            checkVar = False
        elif i == 'True':
            checkVar = True
        elif i == 'None':
            checkVar = None
        else:
            checkVar = i
        datatyp = num.dataType(checkVar)
        if checkVar == '':
            pass
        elif datatyp == 'float':
            correctList.append(float(checkVar))
        elif datatyp == 'int':
            correctList.append(int(checkVar))
        else:
            correctList.append(checkVar)
        
    return correctList


class content:

    def __init__(self, folderPath, *fileName):
        if not folderPath == None:
            autoCreate(folderPath)
            folderPath += '/'
        else:
            folderPath = ''
        self.fpath = folderPath
        self.encoder = 'utf-8'
        if not len(fileName) == 0:
            self.file = f'{folderPath}{fileName[0]}'
        if len(fileName) == 0:
            pass
        elif os.path.exists(self.file):
            os.chmod(self.file, stat.S_IWUSR)
        else:
            with open(self.file, 'a') as o:
                pass
        for i in fileName:
            if i == '*lock*':
                lockFile(self.file)
            elif 'encode:' in i:
                self.encoder = i[7:].strip()

        
    def save(self, *save):
        if len(save) == 0:
            saveString = ''
        else:
            saveString = save[0]
        settings = save[1:]

        howtoOpen = 'a'
        if '*overwrite*' in settings:
            howtoOpen = 'w'

        for i in settings:
            if 'encode:' in i:
                self.encoder = i[7:].strip()
        
        if os.path.exists(self.file):
            os.chmod(self.file, stat.S_IWUSR)
        with open(self.file, howtoOpen, encoding=self.encoder) as o:
            if self.fileContent == []:
                pass
            elif '*sameLN*' in settings:
                pass
            elif not '\n' in self.fileContent[len(self.fileContent)-1]:
                o.writelines('\n')
            o.writelines(str(saveString))
            if not '*sameLN*' in settings:
                o.writelines('\n')
        if '*lock*' in settings:
            lockFile(self.file)
        elif '*unlock*' in settings:
            os.chmod(self.file, stat.S_IWUSR)

    def saveList(self, *save):
        howtoOpen = 'a'
        saveList = save[0]
        settings = save[1:]

        for i in settings:
            if 'encode:' in i:
                self.encoder = i[7:].strip()

        if '*overwrite*' in settings:
            howtoOpen = 'w'

        if os.path.exists(self.file):
            os.chmod(self.file, stat.S_IWUSR)
        with open(self.file, howtoOpen, encoding=self.encoder) as o:
            if self.fileContent == []:
                pass
            elif not '\n' in self.fileContent[len(self.fileContent)-1] and not self.fileContent == "":
                o.writelines('\n')
            iNum = 0
            for i in saveList:
                iNum += 1
                if iNum == 1:
                    pass
                else:
                    o.writelines(',')
                o.writelines(str(i))
            o.writelines('\n')
        if '*lock*' in settings:
            lockFile(self.file)
        elif '*unlock*' in settings:
            os.chmod(self.file, stat.S_IWUSR)

    def fetch(self, *encoding):
        iList = []
        for i in encoding:
            if 'encode:' in i:
                self.encoder = i[7:].strip()
        if not os.path.exists(self.file):
            return None
        with open(self.file, 'r', encoding=self.encoder) as o:
            file_lines = (o.readlines())
        if '*noStrip*' in encoding:
            iList = file_lines
        else:
            for i in file_lines:
                iStrip = i.strip()
                iList.append(iStrip)
        self.fileContent = file_lines
        return iList

    def change(self, thingToChangeIndex, changedThing, *locq):
        if '*List*' in locq:
            iNum = 0
            changedContent = ''
            for i in changedThing:
                iNum += 1
                if iNum == 1:
                    pass
                else:
                    changedContent += ','

                changedContent += str(i)
        else:
            changedContent = changedThing
        changedContent += '\n'

        self.fileContent[thingToChangeIndex] = changedContent
        #if os.path.exists(self.file):
        #    os.chmod(self.file, stat.S_IWUSR)
        # Check if file is locked (read-only)
        file_stat = os.stat(self.file)
        input(file_stat)
        with open(self.file, 'w', encoding=self.encoder) as o:
            for i in self.fileContent:
                o.writelines(str(i))
        if '*lock*' in locq:
            lockFile(self.file)
        elif '*unlock*' in locq:
            os.chmod(self.file, stat.S_IWUSR)

    def delete(self, thingToDeleteIndex, *locq):
        if thingToDeleteIndex == '*file*':
            if os.path.exists(self.file):
                os.chmod(self.file, stat.S_IWUSR)
                os.remove(self.file)
        else:
            del self.fileContent[thingToDeleteIndex]
            os.chmod(self.file, stat.S_IWUSR)
            with open(self.file, 'w', encoding=self.encoder) as o:
                for i in self.fileContent:
                    o.writelines(str(i))
            if '*lock*' in locq:
                lockFile(self.file)
            elif '*unlock*' in locq:
                os.chmod(self.file, stat.S_IWUSR)


if __name__ == '__main__':
    ftest = content('test','whyNotWorking.txt')
    ftest.fetch()
    ftest.save('fileContent, *lock*')

    ftest.change(0, 'true', '*lock*')

    pointsFile = content('Python Report/python_hidden_file', 'CT_LS.txt')
    pointsFileContent = pointsFile.fetch()
    pointsFile.change(8, str(40), '*lock*')
