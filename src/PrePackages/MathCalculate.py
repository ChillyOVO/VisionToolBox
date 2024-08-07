import math
import random
import secrets


class MHYCalculate:
    def __init__(self):
        # Initial the count
        self.countLevel5 = 1
        self.countLevel4 = 1
        self.countCharacterUp = 0
        self.countWeaponUp = 0
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
        # List of Characters Level 5 permanent
        # List of Characters Level 4 permanent
        # List of Characters other

        # List of Weapon Level 5 up
        # List of Weapon Level 5 permanent
        # List of Weapon Level 4 permanent
        # List of Weapon other

    def probabilityOfCharacterNow(self, countLevel5, countLevel4):
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
        if countLevel5 in range(1, 81) and countLevel4 in range(1, 11):
            # print('数据正常')
            getProbabilitySuccess = 1
        else:
            print('输入数据异常')
            return 0, 0, 0
        pLevel5 = min(self.pWeaponLevel5 + 0.06 * max((countLevel5 - self.cWeaponLevel5), 0), 1)
        if 1 - pLevel5 < 0:
            pLevel4 = 0
        else:
            pLevel4 = min(self.pWeaponLevel5 + 0.51 * max((countLevel4 - self.cWeaponLevel4), 0), 1 - pLevel5)
        pLevel3 = max(1 - pLevel5 - pLevel4, 0)
        # 格式化
        pLevel5 = round(pLevel5, 3)
        pLevel4 = round(pLevel4, 3)
        pLevel3 = round(pLevel3, 3)
        return pLevel5, pLevel4, pLevel3

    def singleWishOfUpCharacterPool(self):
        # 模拟单次
        # 生成当前概率
        pLevel5, pLevel4, pLevel3 = self.probabilityOfCharacterNow(self.countLevel5, self.countLevel4)
        # 模拟一次
        CharacterPool = ['0'] * int(pLevel3 * 1000) + ['1'] * int(pLevel4 * 1000) + ['2'] * int(pLevel5 * 1000)
        wishResult = secrets.choice(CharacterPool)
        # 判断结果,修正计数值
        if wishResult == '0':
            # 蓝
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = self.countLevel4 + 1
        elif wishResult == '1':
            # 紫
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = 1
        else:
            # 金
            self.countLevel5 = 1
            self.countLevel4 = 1
        # 具体对象
        return wishResult

    def singleWishOfUpWeaponPool(self):
        # 模拟单次
        # 生成真随机数
        randNum = secrets.randbelow(100000000)
        randNum = randNum / 100000000
        # 生成当前概率
        pLevel5, pLevel4, pLevel3 = self.probabilityOfWeaponNow(self.countLevel5, self.countLevel4)
        # 判断结果,修正计数值
        if randNum <= pLevel3:
            wishResult = 0
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = self.countLevel4 + 1
        elif randNum <= pLevel3 + pLevel4:
            wishResult = 1
            self.countLevel5 = self.countLevel5 + 1
            self.countLevel4 = 1
        else:
            wishResult = 2
            self.countLevel5 = 1
            self.countLevel4 = 1
        # 具体对象
        return wishResult
