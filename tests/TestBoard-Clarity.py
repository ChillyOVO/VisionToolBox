import math
import sys
import time

import cv2
import numpy as np

import src.PDDTVisionToolBox as pd


def getImageClarity(Image):
    """
     清晰度测试函数
    :param Image: 图像
    :return: 分辨率
    """

    # 计算梯度
    Grad = cv2.Laplacian(Image, cv2.CV_64F)
    Grad = cv2.convertScaleAbs(Grad)
    # 计算图像均值
    Mean = np.mean(Grad)
    Mean = np.round(Mean, 1)
    return Mean


# 主函数
if __name__ == '__main__':
    # 打开USB摄像头
    Cap = cv2.VideoCapture(1)
    temp = 0
    tempMax = 0
    while True:
        # 获取图像
        Ret, Image = Cap.read()
        # 计算清晰度
        Image = pd.showImageClarity(Image)
        # 不显示清晰度调整策略
        # if Clarity > tempMax:
        #     cv2.putText(Image, 'Rot On' % Clarity, (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        #     tempMax = Clarity
        #     temp = Clarity
        # elif Clarity > temp:
        #     cv2.putText(Image, 'Rot On' % Clarity, (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        #     temp = Clarity
        # else:
        #     cv2.putText(Image, 'Rot Inverse' % Clarity, (400, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
        #     temp = Clarity
        # 显示图像
        cv2.imshow('Image', Image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # cv2.waitKey(0)
        # print(Clarity)
