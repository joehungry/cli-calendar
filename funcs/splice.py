
def splice(variable ,spliceSign, varTyp):
    stringVar = str(variable)
    SpliceVariable = stringVar.find(spliceSign)
    if SpliceVariable == -1:
        return False, False
    if varTyp == "str":
        return stringVar[:SpliceVariable], stringVar[SpliceVariable+len(spliceSign):]#len(spliceSign) is there so that it wouldnt return the splice sign
    elif varTyp == "int":
        try:
            return int(stringVar[:SpliceVariable]), int(stringVar[SpliceVariable+1:])
        except:
            return False, False
        
def toList(variable, spliceSign, varTyp):
    List = []
    while spliceSign in variable:
        variable1, variable = splice(variable, spliceSign, varTyp)
        List.append(variable1)
    List.append(variable)
    return List
        
if __name__ == '__main__':
    testvar = 'true'
    testList = toList(testvar, '!', 'str')
    print(testList)
    input()

    testVar = 'Wallace & Gromit'
    human, dog = splice(testVar, ' & ', 'str')
    print(testVar)
    print(f'{human=}')
    print(f'{dog=}')
    print()

    testVar = '1+2'
    one, two = splice(testVar, '+', 'int')
    print(testVar)
    print(f'{one=}')
    print(f'{two=}')
    print(f'{one+two=}')
    print()

    testVar = '1+a'
    print(testVar)
    one, two = splice(testVar, '+', 'int')
    print(f'{one=}')
    print(f'{two=}')
    print()

    testVar = "here's.. the.. motherf//kin'.. tea"
    testList = toList(testVar, '.. ', 'str')

    testvar = 'jklfda, hoijfddajkldsj'
    one, two = splice(testVar, '+', 'int')