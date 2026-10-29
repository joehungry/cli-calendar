from funcs import breakup

def create(*elements):
    plantoNum = ''
    finalElements = []
    for i in elements:
        if type(i) == tuple or type == list:
            for listedElement in list(i):
                finalElements.append(listedElement)
        else:
            finalElements.append(i)
    for i in finalElements:
        if len(str(i)) == 1:
            i = f'0{i}'
        plantoNum += str(i)
    return plantoNum

def numify(planList):
    listToSort = []
    planDict = {}
    plantoNum = ''
    for planelement in planList:
        sPlanelement = str(planelement)
        if sPlanelement == None:
            plantoNum += '0'
        elif '/' in sPlanelement:
            plantoNum += create(breakup.date(sPlanelement))
        elif ':' in sPlanelement:
            plantoNum += create(breakup.time(sPlanelement))
        else:
            plantoNum += sPlanelement
        listToSort.append(plantoNum)
        plantoNum = ''
    for ilen, i in enumerate(listToSort):
        planDict[ilen] = i
    return planDict

