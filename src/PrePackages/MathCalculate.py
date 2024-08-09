import math
import random
import secrets


class MHYCalculate:
    def __init__(self):
        # Initial the count
        self.countLevel5 = 1
        self.countLevel4 = 1
        self.countCharacterUp = 0
        self.countCharacterLevel4Up = 0
        self.countWeaponUp = 0
        self.countCharacterLevel5 = 1
        self.countWeaponLevel5 = 1
        self.countWeaponLevel4Up = 0
        # Table of probability
        self.pCharacterLevel5 = 0.006
        self.pCharacterLevel4 = 0.051
        self.pCharacterLevel3 = 0.943
        self.pWeaponLevel5 = 0.007
        self.pWeaponLevel4 = 0.060
        self.pWeaponLevel3 = 0.933
        # Number of guarantees
        self.gCharacter = 90
        self.gWeapon = 80
        self.gCountTen = 10
        # Counts of beginning to increase probability
        self.cCharacterLevel5 = 73
        self.cCharacterLevel4 = 8
        self.cWeaponLevel5 = 62
        self.cWeaponLevel4 = 7
        # List of Characters Level 5 up
        self.ListUpCharacterLevel5 = ['艾梅莉埃']
        # List of Characters Level 5 permanent
        self.ListPermanentCharacterLevel5 = ['迪希雅', '提纳里', '迪卢克', '刻晴', '莫娜', '七七', '琴']
        # List of Characters Level 4 up
        self.ListUpCharacterLevel4 = ['烟绯', '香菱', '雷泽']
        # List of Characters Level 4 permanent
        self.ListPermanentCharacterLevel4 = ['赛索斯', '嘉明', '夏沃蕾', '夏洛蒂', '菲米尼', '琳妮特', '绮良良', '卡维',
                                             '米卡', '瑶瑶', '珐露珊', '莱依拉', '坎蒂丝', '多莉', '柯莱', '鹿野院平藏',
                                             '久岐忍', '云堇', '五郎', '托马', '九条裟罗', '早柚', '烟绯', '罗莎莉亚',
                                             '辛焱', '迪奥娜', '安柏', '芭芭拉', '北斗', '班尼特', '重云', '菲谢尔',
                                             '凯亚', '丽莎', '凝光', '诺艾尔', '雷泽', '砂糖', '香菱', '行秋']
        # List of Characters other

        # List of Weapon Level 5 up
        self.ListUpWeaponLevel5 = ['柔灯挽歌', '若水']
        self.railedWeapon = ['柔灯挽歌']
        # List of Weapon Level 4 up
        self.ListUpWeaponLevel4 = ['笛剑', '玛海菈的水色', '西风长枪', '流浪的晚星', '西风猎弓']
        # List of Weapon Level 5 permanent
        self.ListPermanentWeaponLevel5 = ['天空之刃', '风鹰剑', '狼的末路', '天空之傲', '和璞鸢', '天空之脊',
                                          '四风原典', '天空之卷', '阿莫斯之弓', '天空之翼']
        # List of Weapon Level 4 permanent
        self.ListPermanentWeaponLevel4 = ['匣里龙吟', '祭礼剑', '笛剑', '西风剑', '雨裁', '祭礼大剑', '钟剑',
                                          '西风大剑', '西风长枪', '匣里灭辰', '昭心', '祭礼残章', '流浪乐章',
                                          '西风秘典', '弓藏', '祭礼弓', '绝弦', '西风猎弓']
        self.ListPermanentWeaponLevel3 = ['飞天御剑', '黎明神剑', '冷刃', '以理服人', '沐浴龙血的剑', '铁影阔剑',
                                          '黑缨枪', '翡玉法球', '讨龙英杰谭', '魔导绪论', '弹弓', '神射手之誓',
                                          '鸦羽弓']
        # List of Weapon other

    def probabilityOfCharacterNow(self, countLevel5, countLevel4):
        """

        :param countLevel5:
        :param countLevel4:
        :return:
        """
        if countLevel5 in range(1, 91) and countLevel4 in range(1, 11):
            # print('数据正常')
            getProbabilitySuccess = 1
        else:
            print('输入数据异常')
            return 0, 0, 0
        pLevel5 = min(self.pCharacterLevel5 + 0.06 * max((countLevel5 - self.cCharacterLevel5), 0), 1)
        if 1 - pLevel5 < 0:
            pLevel4 = 0
        else:
            # print(self.pCharacterLevel4 + 0.51 * max((countLevel4 - self.cCharacterLevel4), 0))
            pLevel4 = min(self.pCharacterLevel4 + 0.51 * max((countLevel4 - self.cCharacterLevel4), 0), 1 - pLevel5)
        pLevel3 = max(1 - pLevel5 - pLevel4, 0)
        # 格式化
        pLevel5 = round(pLevel5, 3)
        pLevel4 = round(pLevel4, 3)
        pLevel3 = round(pLevel3, 3)
        return pLevel5, pLevel4, pLevel3

    def probabilityOfWeaponNow(self, countLevel5, countLevel4):
        """

        :param countLevel5:
        :param countLevel4:
        :return:
        """
        if countLevel5 in range(1, 81) and countLevel4 in range(1, 11):
            # print('数据正常')
            getProbabilitySuccess = 1
        else:
            print('输入数据异常')
            return 0, 0, 0
        pLevel5 = min(self.pWeaponLevel5 + 0.07 * max((countLevel5 - self.cWeaponLevel5), 0), 1)
        if 1 - pLevel5 < 0:
            pLevel4 = 0
        else:
            pLevel4 = min(self.pWeaponLevel5 + 0.60 * max((countLevel4 - self.cWeaponLevel4), 0), 1 - pLevel5)
        pLevel3 = max(1 - pLevel5 - pLevel4, 0)
        # 格式化
        pLevel5 = round(pLevel5, 3)
        pLevel4 = round(pLevel4, 3)
        pLevel3 = round(pLevel3, 3)
        return pLevel5, pLevel4, pLevel3

    def singleWishOfUpCharacterPool(self):
        """
            角色池单抽
        :return:
        """
        # 模拟单次
        # 生成当前概率
        pLevel5, pLevel4, pLevel3 = self.probabilityOfCharacterNow(self.countLevel5, self.countLevel4)
        # 模拟一次
        CharacterPool = ['0'] * int(pLevel3 * 1000) + ['1'] * int(pLevel4 * 1000) + ['2'] * int(pLevel5 * 1000)
        wishResult = secrets.choice(CharacterPool)
        # 判断结果,修正计数值
        if wishResult == '0':
            # 蓝，抽卡次数调整
            cResult = self.decisionOfLevel3()
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = self.countLevel4 + 1
        elif wishResult == '1':
            # 紫，抽卡次数调整
            cResult = self.decisionOfCharacterLevel4()
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = 1
        else:
            # 金，抽卡次数调整
            # self.countCharacterLevel5 = self.countCharacterLevel5 + 1
            cResult = self.decisionOfCharacterLevel5()
            self.countLevel5 = 1
            self.countLevel4 = 1
        return wishResult, cResult

    def singleWishOfUpWeaponPool(self):
        """
            武器池单抽
        :return:
        """
        # 模拟单次
        # 生成当前概率
        pLevel5, pLevel4, pLevel3 = self.probabilityOfWeaponNow(self.countLevel5, self.countLevel4)
        # 模拟一次
        WeaponPool = ['0'] * int(pLevel3 * 1000) + ['1'] * int(pLevel4 * 1000) + ['2'] * int(pLevel5 * 1000)
        wishResult = secrets.choice(WeaponPool)
        # 判断结果,修正计数值
        if wishResult == '0':
            # 蓝，抽卡次数调整
            wResult = self.decisionOfLevel3()
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = self.countLevel4 + 1
        elif wishResult == '1':
            # 紫，抽卡次数调整
            wResult = self.decisionOfWeaponLevel4()
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = 1
        else:
            # 金，抽卡次数调整
            # self.countCharacterLevel5 = self.countCharacterLevel5 + 1
            wResult = self.decisionOfWeaponLevel5()
            self.countLevel5 = 1
            self.countLevel4 = 1
        return wishResult, wResult

    def decisionOfCharacterLevel5(self):
        """
            决定是哪个五星的时刻到了
        :return:
        """
        # 确认保底次数
        if self.countCharacterLevel5 == 2:
            # 大保底
            Result = self.ListUpCharacterLevel5[0]
            self.countCharacterLevel5 = 1
        else:
            # 小保底
            num = len(self.ListPermanentCharacterLevel5)
            List = self.ListUpCharacterLevel5 * num + self.ListPermanentCharacterLevel5
            # print(List)
            Result = secrets.choice(List)
            if Result == self.ListUpCharacterLevel5[0]:
                self.countCharacterLevel5 = 1
            else:
                self.countCharacterLevel5 = self.countCharacterLevel5 + 1
        return Result

    def decisionOfCharacterLevel4(self):
        """
            该决定是哪个4星了
        :return:
        """
        if self.countCharacterLevel4Up == 0:
            # 调入全部4星角色表
            upResult = secrets.choice(['0', '1'])
            if upResult == '0':
                List = self.ListPermanentCharacterLevel4 + self.ListPermanentWeaponLevel4
                Result = secrets.choice(List)
                if Result in str(self.ListUpCharacterLevel4):
                    self.countCharacterLevel4Up = 0
                else:
                    self.countCharacterLevel4Up = 1
            else:
                List = self.ListUpCharacterLevel4
                Result = secrets.choice(List)
                self.countCharacterLevel4Up = 0
        else:
            # 4星保底
            List = self.ListUpCharacterLevel4
            Result = secrets.choice(List)
            self.countCharacterLevel4Up = 0

        return Result

    def decisionOfWeaponLevel5(self):
        """
                   决定是哪个五星武器的时刻到了
               :return:
               """
        # 确认保底次数
        if self.countWeaponLevel5 == 3:
            # 大保底
            Result = self.railedWeapon[0]
            self.countWeaponLevel5 = 1
        else:
            # 小保底
            upResult = secrets.choice(['0', '1', '1', '1'])
            if upResult == '0':
                List = self.ListPermanentWeaponLevel5
                Result = secrets.choice(List)
                self.countWeaponLevel5 = self.countWeaponLevel5 + 1
            else:
                List = self.ListUpWeaponLevel5
                Result = secrets.choice(List)
                if Result == self.railedWeapon[0]:
                    self.countWeaponLevel5 = 1
                else:
                    # 定轨 +1
                    self.countWeaponLevel5 = self.countWeaponLevel5 + 1
        return Result

    def decisionOfWeaponLevel4(self):
        """
                    该决定是哪个4星了
                :return:
                """
        if self.countWeaponLevel4Up == 0:
            # 调入全部4星武器表
            upResult = secrets.choice(['0', '1'])
            if upResult == '0':
                List = self.ListPermanentCharacterLevel4 + self.ListPermanentWeaponLevel4
                Result = secrets.choice(List)
                if Result in str(self.ListUpWeaponLevel4):
                    self.countWeaponLevel4Up = 0
                else:
                    self.countWeaponLevel4Up = 1
            else:
                List = self.ListUpWeaponLevel4
                Result = secrets.choice(List)
                self.countWeaponLevel4Up = 0
        else:
            # 4星保底
            List = self.ListUpWeaponLevel4
            Result = secrets.choice(List)
            self.countWeaponLevel4Up = 0

        return Result

    def decisionOfLevel3(self):
        """
            没人关心该是哪个3星
        :return:
        """
        List = self.ListPermanentWeaponLevel3
        Result = secrets.choice(List)
        return Result

    def emulationOfCharacterPool(self, totalTimes):
        """
            角色池模拟
        :param totalTimes:总数
        :return:
        """
        # 修改当前up角色
        # self.ListUpCharacterLevel5 = upCharacter
        # 计数清零
        countTillUp = 0
        countLevel5Total = 0
        # 结果列表初始化
        Result5 = '5星抽取顺序：'
        Result4 = '4星抽取顺序：'
        # Result3 = '3星抽取顺序：'
        ResultTotal = '本次共进行 ' + str(totalTimes) + ' 次抽卡, 抽取结果为：'
        # 开始模拟
        count = 0
        Level5Count = 0
        Level5UpCount = 0
        for i in range(1, totalTimes + 1):
            count = count + 1
            # print(cal1.countLevel5,cal1.countLevel4)
            countTillUp = countTillUp + 1
            characterFlag, character = self.singleWishOfUpCharacterPool()
            ResultTotal = ResultTotal + character + ' '
            if characterFlag == '1':
                # 4星
                Result4 = Result4 + character + ' '
            if characterFlag == '2':
                # 5星
                # print('Level5:', count, '  character: ', character)
                Result5 = Result5 + character + ':' + str(count) + ' '
                count = 0
                countTillUp = 0
                Level5Count = Level5Count + 1
                if character == self.ListUpCharacterLevel5[0]:
                    Level5UpCount = Level5UpCount + 1
        print(ResultTotal)
        print(Result4)
        print(Result5)
        if Level5Count == 0:
            print('本次未抽到5星角色！')
            avgLevel5Count = 90
            avgLevel5UpCount = 180
        else:
            avgLevel5Count = totalTimes / Level5Count
            print('本次共抽取到 ', Level5Count, ' 个5星角色,平均每 ', avgLevel5Count, ' 抽可获得5星角色')
            if Level5UpCount == 0:
                avgLevel5UpCount = 180
                print('本次未抽到限定5星角色！')
            else:
                avgLevel5UpCount = totalTimes / Level5UpCount
                print('本次共抽取到 ', Level5UpCount, ' 个限定5星角色,平均每 ', avgLevel5UpCount,
                      ' 抽可获得当前限定角色')
        if avgLevel5UpCount < 120:
            if avgLevel5Count < 35:
                result = '极致欧皇'
            elif avgLevel5Count < 60:
                result = '大欧皇'
            else:
                result = '小欧皇'
        else:
            if avgLevel5Count < 40:
                result = '欧非二象性'
            elif avgLevel5Count < 60:
                result = '欧中带非'
            else:
                result = '非酋'
        print('本次抽卡欧气判定为：', result)
        return result

    def emulationOfWeaponPool(self, totalTimes):
        """
            武器池模拟
        :param totalTimes:总数
        :return:
        """
        # 修改当前up角色
        # self.ListUpCharacterLevel5 = upCharacter
        # 计数清零
        countTillUp = 0
        countLevel5Total = 0
        # 结果列表初始化
        Result5 = '5星抽取顺序：'
        Result4 = '4星抽取顺序：'
        # Result3 = '3星抽取顺序：'
        ResultTotal = '本次共进行 ' + str(totalTimes) + ' 次抽卡, 抽取结果为：'
        # 开始模拟
        count = 0
        Level5Count = 0
        Level5UpCount = 0
        Level5UpRailedCount = 0
        for i in range(1, totalTimes + 1):
            count = count + 1
            # print(cal1.countLevel5,cal1.countLevel4)
            countTillUp = countTillUp + 1
            weaponFlag, weapon = self.singleWishOfUpWeaponPool()
            ResultTotal = ResultTotal + weapon + ' '
            if weaponFlag == '1':
                # 4星
                Result4 = Result4 + weapon + ' '
            if weaponFlag == '2':
                # 5星
                # print('Level5:', count, '  character: ', character)
                Result5 = Result5 + weapon + ':' + str(count) + ' '
                count = 0
                countTillUp = 0
                Level5Count = Level5Count + 1
                if weapon in str(self.ListUpWeaponLevel5):
                    Level5UpCount = Level5UpCount + 1
                    if weapon == self.railedWeapon[0]:
                        Level5UpRailedCount = Level5UpRailedCount + 1
        print(ResultTotal)
        print(Result4)
        print(Result5)
        if Level5Count == 0:
            print('本次未抽到5星武器！')
            avgLevel5Count = 90
            avgLevel5UpCount = 180
            avgLevel5UpRailedCount = 270
        else:
            avgLevel5Count = totalTimes / Level5Count
            print('本次共抽取到 ', Level5Count, ' 把5星武器,平均每 ', avgLevel5Count, ' 抽可获得5星角色')
            if Level5UpCount == 0:
                avgLevel5UpCount = 180
                avgLevel5UpRailedCount = 270
                print('本次未抽到限定5星武器！')
            else:
                avgLevel5UpCount = totalTimes / Level5UpCount
                print('本次共抽取到 ', Level5UpCount, ' 把限定5星武器,平均每 ', avgLevel5UpCount,
                      ' 抽可获得当前限定角色')
                if Level5UpRailedCount == 0:
                    avgLevel5UpRailedCount = 270
                    print('本次未抽到定轨武器')
                else:
                    avgLevel5UpRailedCount = totalTimes / Level5UpRailedCount
                    print('本次共抽取到 ', Level5UpRailedCount, ' 把定轨限定5星武器,平均每 ', avgLevel5UpCount,
                          ' 抽可获得当前定轨武器')
        if avgLevel5UpRailedCount < 105:
            if avgLevel5Count < 35:
                result = '极致欧皇'
            elif avgLevel5Count < 55:
                result = '大欧皇'
            else:
                result = '小欧皇'
        else:
            if avgLevel5Count < 35:
                result = '欧非二象性'
            elif avgLevel5Count < 55:
                result = '欧中带非'
            else:
                result = '非酋'
        print('本次抽卡欧气判定为：', result)
        return result
