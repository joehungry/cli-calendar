def err(string):
    print(f'\033[91m{string}\033[0m')

def ask(*string):
    for i in string:
        print(i)
    askvar = input('>> ')
    return askvar

def barrier():
    print('--')

def loading(num):
    loadingSymbol = ["*", "-", "/", "^", '+', "=", ">", "<", "v", "o", "O", "|", ":", ";", ".", ",", "~"]
    devide00 = int(num/100)
    fourCap = devide00 - (((len(loadingSymbol)) * int(devide00 / (len(loadingSymbol)))))-1
    if fourCap == -1:
        fourCap = 0
    until00 = loadingSymbol[fourCap]
    if fourCap == len(loadingSymbol)-1:
        from00 = loadingSymbol[0]
    else:
        from00 = loadingSymbol[fourCap+1]
    
    #print(until00)
    #print(from00)
    devide00times00 = int(num/100) * 100
    if not devide00times00 == 0:
        numRange = num - (devide00times00)+100
    else:
        numRange = num
    for n in range(numRange):
        if n > 99:
            break
        elif numRange <= 100 or numRange-n <= 100:
            print(until00, end = '')
            #print(f'num:{num} n:{n} num0n:{num-n}')
        elif numRange-n > 100:
            print(from00, end = '')
            #print(f'num:{num} n:{n} True num0n:{num-n}')
        else:
            err(n)
    print()

def progress(percentage, bar_length=50):
    """
    Displays a text-based progress bar.

    Args:
        percentage (float): The completion percentage (0.0 to 100.0).
        bar_length (int): The total length of the progress bar in characters.
    """
    if not 0 <= percentage <= 100:
        print(f'*not valid number{percentage}*')

    filled_length = int(bar_length * percentage / 100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'|{bar}| {percentage:.1f}%')

if __name__ == '__main__':
    test = 0
    import os
    while True:
        loading(test)
        test += 1
        os.system('cls')