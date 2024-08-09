import src.PrePackages as pp

if __name__ == '__main__':
    # 初始化
    emu1 = pp.MHYCalculate()
    emu1.ListUpCharacterLevel5 = ['艾梅莉埃']
    emu1.ListUpCharacterLevel4 = ['烟绯', '香菱', '雷泽']
    emu1.ListUpWeaponLevel5 = ['柔灯挽歌', '若水']
    emu1.ListUpWeaponLevel4 = ['笛剑', '玛海菈的水色', '西风长枪', '流浪的晚星', '西风猎弓']
    # 开始模拟
    identity = emu1.emulationOfCharacterPool(10)
    identity = emu1.emulationOfWeaponPool(10)

