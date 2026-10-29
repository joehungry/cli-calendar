def choosing(number,settingsDict):
    try:
        return settingsDict[list(settingsDict)[int(number)-1]]#これは、settingsDictと、inputを照らし合わせ、設定の変数を取得するプログラムです
    except:
        return None
    
def chooseScreen(settingsDict):
    for lenI, i in enumerate(settingsDict):
        print(f'{lenI+1}. {i}')