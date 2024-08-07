import src.PrePackages as pp

# 初始化
cal1 = pp.MHYCalculate()
# 测试段-概率测试
# a, b, c = cal1.probabilityOfCharacterNow(80, 1)
# print('5星概率: {:.2%}'.format(a))
# print('4星概率: {:.2%}'.format(b))
# print('3星概率: {:.2%}'.format(c))
# a, b, c = cal1.probabilityOfWeaponNow(88,10)
# print('5星概率: {:.2%}'.format(a))
# print('4星概率: {:.2%}'.format(b))
# print('3星概率: {:.2%}'.format(c))

# from random import choice
# import secrets
#
# # a = ['温迪', '莫娜', '阿贝多', '琴']
# a = ['0'] * 0 + ['1'] * 9 + ['2'] * 1
# print(a)
# print(secrets.choice(a))
# cal1.countLevel4 =1
count = 0
for i in range(1,201):
    # print(cal1.countLevel5,cal1.countLevel4)
    count = count + 1
    a = cal1.singleWishOfUpCharacterPool()
    # print(a)
    if a == '2':
        print('Level5:', count)
        count = 0