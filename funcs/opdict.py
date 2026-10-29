def sort(dict, keyOrValue):
    sortedDict = {}
    if keyOrValue == 'key':
        loc = 0
    elif keyOrValue == 'value':
        loc = 1
    sortedTuple =  sorted(dict.items(), key = lambda i:str(i[loc]))
    for i in sortedTuple:
        sortedDict[i[0]] = i[1]
    return sortedDict

def create(keyList, valueList):
    dictionary = {}
    for key, value in zip(keyList, valueList):
        if key in dictionary.keys():
            dictionary[key] = f'{dictionary[key]},{value}'
        else:
            dictionary[key] = value
    return dictionary

def replaceValue(replacedThing, thingToReplace, dictionary):
    for ikey, ivalue in dictionary.items():
        if ivalue == thingToReplace:
            dictionary[ikey] = replacedThing
    return dictionary

def replaceKey(replacedThing, thingToReplace, dictionary):
    newDict = {}
    for ikey, ivalue in dictionary.items():
        if ikey == thingToReplace:
            newDict[replacedThing] = dictionary[ikey]
        else:
            newDict[ikey] = ivalue
    return newDict

if __name__ == '__main__':
    Tdict = {'cute': 'animals', 'ugly': 'adults', 'bad': 'everthing'}
    print(Tdict)
    print(replaceKey('good', 'bad', Tdict))