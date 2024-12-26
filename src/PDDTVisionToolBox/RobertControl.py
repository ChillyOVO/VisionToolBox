import math
import sys
import cv2
import os
# import math
# import tkinter
import numpy as np
# from tkinter import *
# from tkinter import ttk
from numpy import arctan2, arccos, arcsin, sqrt
from numpy import cos, sin
import openpyxl


class Robert:
    """
    ``计算规定，输入采用 mm 位置，计算过程中均使用m 作为单位，输出仍采用mm
    """

    def __init__(self):
        # 初始化D-H参数,d,a,alpha,theta
        self.DH = np.zeros((7, 4))
        # 初始化关节角
        self.Joints = [0, 0, 0, 0, 0, 0]
        # 初始化末端位置
        self.PosNow = np.array([[0, 0, 0, 0, 0, 0]])
        # 初始化逆运动学参数
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.ox = 0
        self.oy = 0
        self.oz = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.px = 0
        self.py = 0
        self.pz = 0

    def getDHParameters(self, talbeName):
        """
            图像化设置D-H参数
        :return:
        """
        # 重定位地址
        path = os.getcwd()
        path = os.path.dirname(path)
        tablePath = os.path.join(path, "assets/DH_Table.xlsx")
        # print(tablePath)
        # 打开表格
        wb = openpyxl.load_workbook(tablePath)
        # 读表格
        sheet = wb[talbeName]
        # 参数赋值
        for i in range(7):
            for j in range(4):
                temp = sheet.cell(i + 2, j + 2).value
                if temp == None:
                    temp = 0
                self.DH[i, j] = float(temp)
        Method = sheet.cell(2, 6).value

        return Method

    def getTransferMatrix(self, num):
        """
            计算第i-1关节到i关节的变换
        :param num:
        :return:
        """
        # 修改为行数
        num = num - 1
        # 取得DH参数
        d = self.DH[num, 0]
        a = self.DH[num, 1]
        from numpy import radians
        alpha = radians(self.DH[num, 2])
        # theta = math.radians(self.DH[num, 3] + self.Joints[num])
        theta = radians(self.Joints[num])
        # 初始化矩阵
        TransMat = np.array([[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
                             [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
                             [0, sin(alpha), cos(alpha), d],
                             [0, 0, 0, 1]])
        return TransMat

    def getTransferMatrixMDH(self, num):
        """
            利用后置MDH算法进行正向运动学计算
        :param num:
        :return:
        """
        # 修改为行数
        num = num - 1
        # 取得DH参数
        d = self.DH[num, 0]
        a = self.DH[num, 1]
        from numpy import radians
        alpha = radians(self.DH[num, 2])
        theta = radians(self.DH[num, 3] + self.Joints[num])
        # theta = radians(self.Joints[num])
        TransMat = np.array([[cos(theta), -sin(theta), 0, a],
                             [sin(theta) * cos(alpha), cos(theta) * cos(alpha), -sin(alpha), -d * sin(alpha)],
                             [sin(theta) * sin(alpha), cos(theta) * sin(alpha), cos(alpha), d * cos(alpha)],
                             [0, 0, 0, 1]])
        return TransMat

    def getTransferMatrixKukaKr(self, num):
        """
            计算第i-1关节到i关节的变换
        :param num:
        :return:
        """
        # 取得DH参数
        d = self.DH[num, 0]
        a = self.DH[num, 1]
        from numpy import radians
        alpha = radians(self.DH[num, 2])
        # theta = math.radians(self.DH[num, 3] + self.Joints[num])
        if num == 0:
            theta = 0
        else:
            theta = radians(self.Joints[num - 1] + self.DH[num, 3])
        # 初始化矩阵
        TransMat = np.array([[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
                             [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
                             [0, sin(alpha), cos(alpha), d],
                             [0, 0, 0, 1]])
        return TransMat

    def getTransferMatrixKukaKrStatuts(self, num, Joints):
        """
            计算第i-1关节到i关节的变换
        :param num:
        :return:
        """
        # 取得DH参数
        d = self.DH[num, 0]
        a = self.DH[num, 1]
        from numpy import radians
        alpha = radians(self.DH[num, 2])
        # theta = math.radians(self.DH[num, 3] + self.Joints[num])
        if num == 0:
            theta = 0
        else:
            # print(Joints[0][num - 1])
            theta = radians(Joints[0][num - 1] + self.DH[num, 3])
        # 初始化矩阵
        # print(theta)
        TransMat = np.array([[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
                             [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
                             [0, sin(alpha), cos(alpha), d],
                             [0, 0, 0, 1]])
        return TransMat

    def getEndPosNow(self, Joints, method):
        """
            根据关节角得到末端位置
        :param Joints:
        :param method: 方法
        :return:
        """
        # 解析关节角
        self.Joints[0] = Joints[0]
        self.Joints[1] = Joints[1]
        self.Joints[2] = Joints[2]
        self.Joints[3] = Joints[3]
        self.Joints[4] = Joints[4]
        self.Joints[5] = Joints[5]
        # 计算各关节变换矩阵
        if method == 'SDH':
            T1 = self.getTransferMatrix(1)
            T2 = self.getTransferMatrix(2)
            T3 = self.getTransferMatrix(3)
            T4 = self.getTransferMatrix(4)
            T5 = self.getTransferMatrix(5)
            T6 = self.getTransferMatrix(6)
            # 计算末端位置
            T = T1 @ T2 @ T3 @ T4 @ T5 @ T6
        elif method == 'MDH':
            T1 = self.getTransferMatrixMDH(1)
            T2 = self.getTransferMatrixMDH(2)
            T3 = self.getTransferMatrixMDH(3)
            T4 = self.getTransferMatrixMDH(4)
            T5 = self.getTransferMatrixMDH(5)
            T6 = self.getTransferMatrixMDH(6)
            # 计算末端位置
            T = T1 @ T2 @ T3 @ T4 @ T5 @ T6
        elif method == 'Kuka-KR':
            T0 = self.getTransferMatrixKukaKr(0)
            T1 = self.getTransferMatrixKukaKr(1)
            T2 = self.getTransferMatrixKukaKr(2)
            T3 = self.getTransferMatrixKukaKr(3)
            T4 = self.getTransferMatrixKukaKr(4)
            T5 = self.getTransferMatrixKukaKr(5)
            T6 = self.getTransferMatrixKukaKr(6)
            T = T0 @ T1 @ T2 @ T3 @ T4 @ T5 @ T6
        else:
            print("getEndPosNow 方法错误 请选择SDH 或 MDH")
            sys.exit()
        # 计算末端位置
        # T = T1 @ T2 @ T3 @ T4 @ T5 @ T6
        self.PosNow = T
        return T

    def getJointsCobot(self, Pos):
        """
            根据位置（RPY）角，对协作臂关节进行反向求解，求解顺序156324，理论上会求出8组解
        :param Pos:
        :return:
        """
        # 初始化Joints
        joints = np.zeros((8, 6))
        count = 0
        # 导入位姿
        self.getInverseParameters(Pos)
        # 求解Joints1
        theta1 = self.getJoints1()
        for i, joint1 in enumerate(theta1):
            theta5 = self.getJoints5(joint1)
            for j, joint5 in enumerate(theta5):
                joint6 = self.getJoints6(joint1, joint5)
                theta3 = self.getJoints3(joint1, joint6)
                for k, joint3 in enumerate(theta3):
                    joint2 = self.getJoints2(joint1, joint6, joint3)
                    joint4 = self.getJoints4(joint1, joint2, joint3, joint6)
                    joints[[count], :] = np.array([joint1, joint2, joint3, joint4, joint5, joint6])
                    count = count + 1
        return joints

    def getAnglesToRotaionMatrix(self, Rx, Ry, Rz):
        """
            利用弧度制的角度转换为旋转矩阵,RPY方式
        :param Rx:旋转角
        :param Ry:
        :param Rz:
        :return:
        """
        # 计算旋转矩阵的X分量
        from numpy import cos, sin
        RotMatX = np.array([[1, 0, 0],
                            [0, cos(Rx), -sin(Rx)],
                            [0, sin(Rx), cos(Rx)]])

        # 计算旋转矩阵的Y分量
        RotMatY = np.array([[cos(Ry), 0, sin(Ry)],
                            [0, 1, 0],
                            [-sin(Ry), 0, cos(Ry)]])

        # 计算旋转矩阵的Z分量
        RotMatZ = np.array([[cos(Rz), -sin(Rz), 0],
                            [sin(Rz), cos(Rz), 0],
                            [0, 0, 1]])
        RotMat = RotMatZ @ RotMatY @ RotMatX

        return RotMat

    def getInverseParameters(self, Pos):
        """
            导入位姿
        :param Pos:
        :return:
        """
        # 获取旋转矩阵
        Rot = self.getAnglesToRotaionMatrix(Pos[3], Pos[4], Pos[5])
        # 旋转矩阵参数
        self.nx = Rot[0, 0]
        self.ny = Rot[1, 0]
        self.nz = Rot[2, 0]
        self.ox = Rot[0, 1]
        self.oy = Rot[1, 1]
        self.oz = Rot[2, 1]
        self.ax = Rot[0, 2]
        self.ay = Rot[1, 2]
        self.az = Rot[2, 2]
        # 获取平移参数
        self.px = Pos[0]
        self.py = Pos[1]
        self.pz = Pos[2]

        return 0

    def getJoints1(self):
        """
            计算关节1
        :return:
        """
        # 构造
        d4 = self.DH[3, 0]
        d6 = self.DH[5, 0]
        m = self.ay * d6 - self.py
        n = self.ax * d6 - self.px
        # 求解关节1
        if m ** 2 + n ** 2 - d4 ** 2 >= 0:
            theta11 = arctan2(m, n) - arctan2(d4, sqrt(m ** 2 + n ** 2 - d4 ** 2))
            theta12 = arctan2(m, n) - arctan2(d4, -sqrt(m ** 2 + n ** 2 - d4 ** 2))
        else:
            print("肩关节奇异，关节1无法求解")
            sys.exit()
        return [theta11, theta12]

    def getJoints2(self, theta1, theta6, theta3):
        """

        :return:
        """
        # 构造参数
        d1 = self.DH[0, 0]
        d5 = self.DH[4, 0]
        d6 = self.DH[5, 0]
        a2 = self.DH[1, 1]
        a3 = self.DH[2, 1]
        m = d5 * (sin(theta6) * (self.nx * cos(theta1) + self.ny * sin(theta1)) + cos(theta6) * (
                self.ox * cos(theta1) + self.oy * sin(theta1))) - d6 * (
                    self.ax * cos(theta1) + self.ay * sin(theta1)) + self.px * cos(theta1) + self.py * sin(theta1)
        n = self.pz - d1 - self.az * d6 + d5 * (self.oz * cos(theta6) + self.nz * sin(theta6))
        s2 = (n * (a3 * cos(theta3) + a2) - a3 * sin(theta3) * m) / (a2 ** 2 + a3 ** 2 + 2 * a2 * a3 * cos(theta3))
        c2 = (m + a3 * sin(theta3) * s2) / (a3 * cos(theta3) + a2)
        # 求解
        theta2 = arctan2(s2, c2)
        return theta2

    def getJoints3(self, theta1, theta6):
        """

        :return:
        """
        # 构造参数
        d1 = self.DH[0, 0]
        d5 = self.DH[4, 0]
        d6 = self.DH[5, 0]
        a2 = self.DH[1, 1]
        a3 = self.DH[2, 1]
        m = d5 * (sin(theta6) * (self.nx * cos(theta1) + self.ny * sin(theta1)) + cos(theta6) * (
                self.ox * cos(theta1) + self.oy * sin(theta1))) - d6 * (
                    self.ax * cos(theta1) + self.ay * sin(theta1)) + self.px * cos(theta1) + self.py * sin(theta1)
        n = self.pz - d1 - self.az * d6 + d5 * (self.oz * cos(theta6) + self.nz * sin(theta6))
        if m ** 2 + n ** 2 <= (a2 + a3) ** 2:
            theta31 = arccos((m ** 2 + n ** 2 - a2 ** 2 - a3 ** 2) / (2 * a2 * a3))
            theta32 = -arccos((m ** 2 + n ** 2 - a2 ** 2 - a3 ** 2) / (2 * a2 * a3))
        else:
            print("肘部奇异，关节3无法求解")
            # sys.exit()
            theta31 = 4
            theta32 = 4

        return [theta31, theta32]

    def getJoints4(self, theta1, theta2, theta3, theta6):
        """

        :return:
        """
        # 求解
        theta4 = arctan2(
            -sin(theta6) * (self.nx * cos(theta1) + self.ny * sin(theta1)) - cos(theta6) * (
                    self.ox * cos(theta1) + self.oy * sin(theta1)),
            self.oz * cos(theta6) + self.nz * sin(theta6)) - theta2 - theta3

        return theta4

    def getJoints5(self, theta1):
        """
            获取关节5
        :param theta1:
        :return:
        """
        # 构造参数
        m = self.ax * sin(theta1) - self.ay * cos(theta1)
        # 求解
        if m <= 1:
            theta51 = arccos(m)
            theta52 = -arccos(m)
        else:
            print("余弦构造奇异，关节5无法求解")
            # sys.exit()
            theta51 = 4
            theta52 = 4

        return [theta51, theta52]

    def getJoints6(self, theta1, theta5):
        """

        :return:
        """
        # 构造参数
        m = self.nx * sin(theta1) - self.ny * cos(theta1)
        n = self.ox * sin(theta1) - self.oy * cos(theta1)
        # 求解
        if theta5 != 0:
            theta6 = arctan2(m, n) - arctan2(sin(theta5), 0)
            # theta6 = arctan2(m / sin(theta5), n / sin(theta5))
        else:
            print("肘关节奇异，关节6无法求解")
            # sys.exit()
            theta6 = 4

        return theta6

    def getJointsKukaKR(self, Pos):
        """
            根据位置（RPY）角，对球形腕Kuka类型工业臂关节进行反向求解，求解顺序123-456，理论上会求出8组解
        :param Pos:
        :return:
        """
        # 初始化Joints
        Joints = np.zeros((1, 6))
        joints = np.zeros((100, 6))
        count = 0
        # 导入位姿
        self.getInverseParameters(Pos)
        # 计算关节1
        theta1 = self.getJoint1Kuka()
        # 计算关节2、3、23角度合
        for i, joint1 in enumerate(theta1):
            theta2, theta3, theta23 = self.getJoint2AndJoint3Kuka(joint1)
            # print("theta3值", theta3)
            for j, joint2 in enumerate(theta2):
                joint3 = theta3[j]
                joint23 = theta23[j]
                # 计算关节4、5、6
                joint4, theta5, joint6 = self.getJoint456Kuka(joint1, joint23)
                for k, joint5 in enumerate(theta5):
                    # print("循环内J5", np.degrees(joint5))
                    joints[[count], :] = np.array([joint1, joint2, joint3, joint4, joint5, joint6])
                    joints[[count + 1], :] = np.array([joint1, joint2, joint3, joint4 + np.pi, -joint5, joint6 + np.pi])
                    joints[[count + 2], :] = np.array([joint1, joint2, joint3, joint4 - np.pi, -joint5, joint6 - np.pi])
                    count = count + 3

        length = len(joints[:, [0]])
        # print(joints)
        # joints = joints[[not np.all(joints[j] == 0) for j in range(joints.shape[0])], :]
        # print("未筛选解：", np.degrees(joints))
        # print(length)
        for i in range(length):
            Jo1 = abs(np.degrees(joints[i, 0]))
            Jo2 = np.degrees(joints[i, 1])
            Jo3 = np.degrees(joints[i, 2])
            Jo4 = abs(np.degrees(joints[i, 3]))
            Jo5 = abs(np.degrees(joints[i, 4]))
            Jo6 = abs(np.degrees(joints[i, 5]))
            # 可达范围 KR360范围
            if Jo1 < 185 and -130 < Jo2 < 20 and -100 < Jo3 < 144 and Jo4 < 350 and Jo5 < 120 and Jo6 < 350:
                Joints = np.row_stack((Joints, joints[[i], :]))
                # 以（-360，360，180）为循环测试4、6轴可得与否
                for j in range(5):
                    j = j - 2
                    for k in range(5):
                        k = k - 2
                        # print(j,k)
                        jo4 = joints[[i], 3] + j * np.pi * 2
                        jo6 = joints[[i], 5] + k * np.pi * 2
                        joLimit = np.radians(350)
                        if abs(jo4) < joLimit and abs(jo6) < joLimit:
                            # if abs(jo4) < joLimit and abs(jo6) < joLimit and ((j + k) & 1) == 0:
                            if j == 0 and k == 0:
                                # do nothing
                                temp = 0
                            else:
                                temp = joints[[i], :]
                                temp[0, 3] = jo4
                                temp[0, 5] = jo6
                                Joints = np.row_stack((Joints, temp))
        Joints = Joints[[not np.all(Joints[j] == 0) for j in range(Joints.shape[0])], :]
        Joints = np.round(Joints, 6)
        Joints = np.unique(Joints, axis=0)
        # print(Joints)
        # 验证位置是否正确
        length = len(Joints[:, 0])
        # print(length)
        # i =0
        # print([Joints[i, 0], Joints[i, 1], Joints[i, 2], Joints[i, 3], Joints[i, 4], Joints[i, 5]])
        for i in range(length):
            pos = self.getEndPosNow(
                [np.degrees(Joints[i, 0]), np.degrees(Joints[i, 1]), np.degrees(Joints[i, 2]), np.degrees(Joints[i, 3]),
                 np.degrees(Joints[i, 4]), np.degrees(Joints[i, 5])], 'Kuka-KR')
            # print(pos)
            dis = sqrt((Pos[0] - pos[0, 3]) ** 2 + (Pos[1] - pos[1, 3]) ** 2 + (Pos[2] - pos[2, 3]) ** 2)
            # print(dis)
            if dis > 10:
                Joints[[i], :] = 0
        Joints = Joints[[not np.all(Joints[j] == 0) for j in range(Joints.shape[0])], :]
        # 输出标志位
        length = len(Joints[:, 0])
        KukaStatusList = []
        KukaTurnList = []
        KukaST = np.zeros((length, 2))
        for i in range(length):
            statusFlag, statusNum = self.getKukaKrStatus(np.degrees(Joints[[i], :]))
            turnFlag, turnNum = self.getKukaKrTurn(np.degrees(Joints[[i], :]))
            KukaST[i, 0] = statusNum
            KukaST[i, 1] = turnNum
            KukaStatusList.append(statusFlag)
            KukaTurnList.append(turnFlag)
            # print(KukaST)
            # Joints = np.hstack((Joints, KukaST))
        return Joints, KukaST, KukaStatusList, KukaTurnList

    def getJoint1Kuka(self):
        """
            求解kuka 关节 1
        :return:
        """
        # 构造参数
        d6 = self.DH[6, 0]
        m = d6 * self.ay + self.py
        n = d6 * self.ax + self.px
        # 计算
        theta11 = - arctan2(m, n)
        if theta11 > 0:
            theta12 = theta11 - np.pi
        else:
            theta12 = theta11 + np.pi

        return [theta11, theta12]

    def getJoint2AndJoint3Kuka(self, theta1):
        """
            求解kuka 关节2 和 关节3
        :param theta1:关节1
        :return:
        """
        # 构造参数
        d0 = self.DH[0, 0]
        d4 = self.DH[4, 0]
        d6 = self.DH[6, 0]
        a1 = self.DH[1, 1]
        a2 = self.DH[2, 1]
        a3 = self.DH[3, 1]
        m1 = cos(theta1) * (self.ax * d6 + self.px) - sin(theta1) * (self.ay * d6 + self.py) - a1
        m2 = d0 - self.pz - self.az * d6
        m3 = (a2 ** 2 - d4 ** 2 - a3 ** 2 - m1 ** 2 - m2 ** 2) / 2
        n1 = sqrt((d4 * m2 - a3 * m1) ** 2 + (d4 * m1 + a3 * m2) ** 2)
        # print(m3/n1)
        if abs(m3 / n1) <= 1:
            # 求解theta23
            theta231 = arctan2(d4 * m2 - a3 * m1, d4 * m1 + a3 * m2) + arccos(m3 / n1)
            theta232 = arctan2(d4 * m2 - a3 * m1, d4 * m1 + a3 * m2) - arccos(m3 / n1)
            # print(theta231, theta232)
            # 求解theta2
            # print("t1", (m1 + d4 * cos(theta231) - a3 * sin(theta231)) / a2)
            # print("t2", (m1 + d4 * cos(theta232) - a3 * sin(theta232)) / a2)
            theta21 = arccos((m1 + d4 * cos(theta231) - a3 * sin(theta231)) / a2)
            theta22 = -arccos((m1 + d4 * cos(theta231) - a3 * sin(theta231)) / a2)
            theta23 = arccos((m1 + d4 * cos(theta232) - a3 * sin(theta232)) / a2)
            theta24 = -arccos((m1 + d4 * cos(theta232) - a3 * sin(theta232)) / a2)
            # 求解theta3
            theta31 = theta231 - theta21
            theta32 = theta231 - theta22
            theta33 = theta232 - theta23
            theta34 = theta232 - theta24
            theta31 = self.getKukaKrTheta3Ajust(theta31)
            theta32 = self.getKukaKrTheta3Ajust(theta32)
            theta33 = self.getKukaKrTheta3Ajust(theta33)
            theta34 = self.getKukaKrTheta3Ajust(theta34)
        else:
            # print("余弦构造失败，关节2、3解算失败")
            theta21 = 2 * np.pi
            theta22 = 2 * np.pi
            theta23 = 2 * np.pi
            theta24 = 2 * np.pi
            theta31 = 2 * np.pi
            theta32 = 2 * np.pi
            theta33 = 2 * np.pi
            theta34 = 2 * np.pi
            theta231 = 2 * np.pi
            theta232 = 2 * np.pi

        return [theta21, theta22, theta23, theta24], [theta31, theta32, theta33, theta34], [theta231, theta231,
                                                                                            theta232, theta232]

    def getJoint456Kuka(self, theta1, theta23):
        """
            求解关节5
        :param theta1: 关节1
        :param theta23: 关节23
        :return:
        """
        # 计算
        # print("theta23", theta23)
        # print('测试余弦', abs(cos(theta23) * (self.ax * cos(theta1) - self.ay * sin(theta1)) - self.az * sin(theta23)))
        if abs(cos(theta23) * (self.ax * cos(theta1) - self.ay * sin(theta1)) - self.az * sin(theta23)) <= 1:
            theta51 = arccos(cos(theta23) * (self.ax * cos(theta1) - self.ay * sin(theta1)) - self.az * sin(theta23))
            theta52 = arccos(cos(theta23) * (self.ax * cos(theta1) - self.ay * sin(theta1)) - self.az * sin(theta23))
            # print("J5", np.degrees(theta51), np.degrees(theta52))
            theta4 = arctan2(-self.ax * sin(theta1) - self.ay * cos(theta1),
                             sin(theta23) * (self.ay * sin(theta1) - self.ax * cos(theta1)) - self.az * cos(theta23))
            theta6 = arctan2(cos(theta23) * (self.oy * sin(theta1) - self.ox * cos(theta1)) + self.oz * sin(theta23),
                             cos(theta23) * (self.ny * sin(theta1) - self.nx * cos(theta1)) + self.nz * sin(theta23))
        else:
            theta4 = 4
            theta51 = 4
            theta52 = 4
            theta6 = 4
        return theta4, [theta51, theta52], theta6

    def getKukaKrTheta3Ajust(self, theta3):
        """
            修正theta3值，
        :param theta3:
        :return:
        """
        if np.degrees(theta3) <= -100:
            theta3 = theta3 + np.pi * 2
        elif np.degrees(theta3) >= 144:
            theta3 = theta3 - np.pi * 2
        return theta3

    def getA4PosKukaKr(self, Joints):
        """
            获取手轴位置,输入为角度制
        :return:
        """
        T0 = self.getTransferMatrixKukaKrStatuts(0, Joints)
        T1 = self.getTransferMatrixKukaKrStatuts(1, Joints)
        T2 = self.getTransferMatrixKukaKrStatuts(2, Joints)
        T3 = self.getTransferMatrixKukaKrStatuts(3, Joints)
        T4 = self.getTransferMatrixKukaKrStatuts(4, Joints)
        T5 = self.getTransferMatrixKukaKrStatuts(5, Joints)
        T6 = self.getTransferMatrixKukaKrStatuts(6, Joints)
        # T6 = self.getTransferMatrixKukaKr(6)
        T = T0 @ T1 @ T2 @ T3 @ T4
        return T

    def getKukaKrStatus(self, Joints):
        """
            计算当前关节角对应状态S,输入角度位角度制
        :param Joints:
        :return:
        """
        # 状态位1
        PosX = self.getA4PosKukaKr(Joints)[0, 3]
        # 手轴位置X为负表示为过顶区域，flag = 1
        if PosX < 0:
            flag0 = 1
        else:
            flag0 = 0
        # 状态位2
        if Joints[0, 2] >= 0:
            flag1 = 1
        else:
            flag1 = 0
        # 状态位3
        if Joints[0, 4] >= 0:
            flag2 = 1
        else:
            flag2 = 0
        # 状态位4
        flag3 = 0
        # 输出状态字符号
        flagStr = str(flag3) + str(flag2) + str(flag1) + str(flag0)
        flagNum = flag3 * (2 ** 3) + flag2 * (2 ** 2) + flag1 * 2 + flag0
        # print(flagNum)
        return flagStr, flagNum

    def getKukaKrTurn(self, Joints):
        """
            计算当前关节角对应转角T,输入角度位角度制
        :param Joints:
        :return:
        """
        # 状态位0
        if Joints[0, 0] >= 0:
            flag0 = 0
        else:
            flag0 = 1
        # 状态位1
        if Joints[0, 1] >= 0:
            flag1 = 0
        else:
            flag1 = 1
        # 状态位2
        if Joints[0, 2] >= 0:
            flag2 = 0
        else:
            flag2 = 1
        # 状态位3
        if Joints[0, 3] >= 0:
            flag3 = 0
        else:
            flag3 = 1
        # 状态位4
        if Joints[0, 4] >= 0:
            flag4 = 0
        else:
            flag4 = 1
        # 状态位5
        if Joints[0, 5] >= 0:
            flag5 = 0
        else:
            flag5 = 1

        # 输出状态字符号
        flagStr = str(00) + str(flag5) + str(flag4) + str(flag3) + str(flag2) + str(flag1) + str(flag0)
        flagNum = flag5 * (2 ** 5) + flag4 * (2 ** 4) + flag3 * (2 ** 3) + flag2 * (2 ** 2) + flag1 * 2 + flag0
        # print(flagNum)
        return flagStr, flagNum
