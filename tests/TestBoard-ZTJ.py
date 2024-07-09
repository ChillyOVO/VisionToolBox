import cv2
import numpy as np
import src.PDDTVisionToolBox as pd

# Vec1 = np.array([0, 2, 0])
# Vec2 = np.array([1, 2, 1])
#
# Rot = pd.getCoordinateByNormalVectorAndPlane(Vec1, Vec2)
# print(Rot)
# rx, ry, rz = pd.getRotationMatrixToAngles(Rot)
# print(rx*180/np.pi, ry*180/np.pi, rz*180/np.pi)
# 左上-右上-右下-左下
P1 = np.array([2160.713, -392.2607, 618.6835])
P2 = np.array([2009.309, -390.839, 618.6964])
P3 = np.array([2009.307, -386.7201, 474.0135])
P4 = np.array([2163.016, -388.0243, 474.0114])
# 组合点
P = np.vstack((P1, P2, P3, P4))
P = P.T
# print(P)
# 左上-右上-右下
angles = pd.getAngleBy3DPointsInDegree(P1, P2, P3)
print("左上-右上-右下夹角：", angles, "°")
# 右上-右下-左下
angles = pd.getAngleBy3DPointsInDegree(P2, P3, P4)
print("右上-右下-左下夹角：", angles, "°")
# 计算平面
Plane = pd.getPlaneFitting(P)
# print(Plane)
normal = np.array([[Plane[0][0]], [Plane[1][0]], [-1]])
# print(normal)
VecInject = np.array([[0], [0], [1]])
Rot = pd.getCoordinateBy2Vectors(normal, VecInject)
print(Rot)
Rot = Rot[:, [1, 0, 2]]
rx, ry, rz = pd.getRotationMatrixToAngles(Rot)
print('旋转角度：Rx = %.6f °, Ry = %.6f °, Rz = %.6f °' % (rx * 180 / np.pi, ry * 180 / np.pi, rz * 180 / np.pi))
