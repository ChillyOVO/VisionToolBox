import cv2
import numpy as np
import os
import subprocess


def getLocationByYOLOX(Img, Model_Type):
    """
        利用YOLOX识别工件类型并返回其形心位置
    :param Img: 输入图像
    :param Model_Type:调用模型
    :return:
    """
    if Model_Type == 0:
        pathImgWrite = './img/1.bmp'
        pathPosRead = './pose_data/data.csv'
    else:
        print('所选模型未训练,请重新选择')
        os._exit(0)
    cv2.imwrite(pathImgWrite, Img)
    myPose = subprocess.Popen("predict.exe")
    try:
        myPose.wait(timeout=100)
    except Exception as e:
        print("Time Out")
        myPose.kill()
    ImgResult = cv2.imread('./img_out/1.bmp')
    # cv2.namedWindow("Test", 0)
    # cv2.resizeWindow("Test", 1920, 1080)
    # cv2.imshow('Test', ImgResult)
    # cv2.waitKey(0)
    pos = np.genfromtxt(pathPosRead, delimiter=',', dtype=int)
    return pos