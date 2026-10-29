try:
    from funcs import breakup
    from funcs import splice
except:
    import breakup
    import splice

def cap(num, cap):
    capNum = num - (((cap) * int(num / cap)))
    return capNum

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

def numify(planraw):
    plan = str(planraw)
    plan += 'e'#to end the program
    plantoNumL = []
    plantoNum = ''
    for planelement in plan:
        if isNum(planelement) == True:
            plantoNum += planelement
        elif len(str(plantoNum)) < 2:
            plantoNumL.append(f'0{plantoNum}')
            plantoNum = ''
        else:
            plantoNumL.append(plantoNum)
            plantoNum = ''

    numified = ''
    for numElement in plantoNumL:
        numified += str(numElement)
    return int(numified)

def isNum(number):
    try:
        int(number)
        return True
    except:
        return False

def dataType(number):
    if number == True or number == False:
        return 'Boolean'
    if isNum(number) == False:
        return 'notNum'
    if not '.' in str(number):
        return 'int'
    beforeDecimal, afterDecimal = splice.splice(number, '.', 'int')
    if int(afterDecimal) == 0:
        return 'int'
    return 'float'

if __name__ == '__main__':
    print(numify('2024/10/7'))
    print(cap(12-1, 13)+1)
    print(dataType(True))