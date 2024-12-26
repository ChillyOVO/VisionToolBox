import fcl
import numpy as np

import numpy as np
import fcl


# v1 = np.array([1.0, 2.0, 3.0])
# v2 = np.array([2.0, 1.0, 3.0])
# v3 = np.array([3.0, 2.0, 1.0])
# x, y, z = 1, 2, 3
# rad, lz = 1, 2.0
# n = np.array([1.0, 0.0, 0.0])
# d = 5.0
#
# t = fcl.TriangleP(v1, v2, v3)  # 三点v1, v2, v3 定义一个Triangle
# b = fcl.Box(x, y, z)  # 三边长度x, y, z 定义与坐标轴轴对齐的box
# s = fcl.Sphere(rad)  # 半径rad 定义Sphere
# e = fcl.Ellipsoid(x, y, z)  # 三个半径x, y, z 定义与坐标轴对齐的Ellipsoid
# c = fcl.Capsule(rad, lz)  # 半径rad和与z轴一致的高度lz 定义一个capsule
# # c = fcl.Cone(rad, lz)         # 半径rad和与z轴一致的高度lz 定义一个Cone
# # c = fcl.Cylinder(rad, lz)     # 半径rad和与z轴一致的高度lz 定义一个Cylinder
# h = fcl.Halfspace(n, d)  # {x : <n, x> < d} 定义Halfspace
# p = fcl.Plane(n, d)  # {x : <n, x> = d} 定义Plane
#
# # 定义两个形状
# box = fcl.Box(1, 1, 1)  # 三边长度1, 1, 1 定义与坐标轴轴对齐的box
# sphere = fcl.Sphere(1)  # 半径1 定义Sphere
#
# # 定义两个位姿,并使其保持一致
# T1 = np.array([1.0, 2.0, 3.0])  # 平移矩阵表示位置
# q1 = np.array([0.707, 0.0, 0.0, 0.707])  # 四元数，表示姿态
# T2 = np.array([0.0, 0.0, 3])  # 平移矩阵表示位置
# q2 = np.array([0, 0.0, 0.0, 0])  # 四元数，表示姿态
# box_tf = fcl.Transform(q1, T1)  # 四元数旋转与平移
# sphere_tf = fcl.Transform(q2, T2)  # 也可以用另一个Transform初始化
#
# T0 = np.array([0, 0, 0])
# q0 = np.array([0, 0, 0, 0])
# capsule_tf = fcl.Transform(q0, T0)
#
# # 通过形状和位置，生成碰撞对象
# box_obj = fcl.CollisionObject(box, box_tf)
# sphere_obj = fcl.CollisionObject(sphere, sphere_tf)
# capsule_obj = fcl.CollisionObject(c, capsule_tf)
#
# # 碰撞检测
# request = fcl.CollisionRequest()
# result = fcl.CollisionResult()
# ret = fcl.collide(box_obj, sphere_obj, request, result)
# print("箱子和球是否发生了碰撞", result.is_collision)
#
# # 距离检测
# request = fcl.DistanceRequest()
# result = fcl.DistanceResult()
# ret = fcl.distance(box_obj, sphere_obj, request, result)
# print("两者之间最小距离", result.min_distance)
#
# # Capsule 测试
# request = fcl.CollisionRequest()
# result = fcl.CollisionResult()
# ret = fcl.collide(capsule_obj, sphere_obj, request, result)
# print("胶囊体和球是否发生了碰撞", result.is_collision)


class CollisionCheck():
    def __init__(self):
        self.request = fcl.CollisionRequest()
        self.result = fcl.CollisionResult()

    def addObject(self, Type, Size, RotMat, TransMat):
        if Type == 'Box':
            try:
                obj = fcl.Box(Size[0], Size[1], Size[2])
            except:
                print('Size Error')
                return None
        elif Type == 'Sphere':
            try:
                obj = fcl.Sphere(Size[0])
            except:
                print('Size Error')
                return None
        elif Type == 'Ellipsoid':
            try:
                obj = fcl.Ellipsoid(Size[0], Size[1], Size[2])
            except:
                print('Size Error')
                return None
        elif Type == 'Capsule':
            try:
                obj = fcl.Capsule(Size[0], Size[1])
            except:
                print('Size Error')
                return None
        elif Type == 'Cone':
            try:
                obj = fcl.Cone(Size[0], Size[1])
            except:
                print('Size Error')
                return None
        elif Type == 'Cylinder':
            try:
                obj = fcl.Cylinder(Size[0], Size[1])
            except:
                print('Size Error')
                return None
        elif Type == 'Halfspace':
            try:
                obj = fcl.Halfspace(Size[0], Size[1])
            except:
                print('Size Error')
                return None
        elif Type == 'Plane':
            try:
                obj = fcl.Plane(Size[0], Size[1])
            except:
                print('Size Error')
                return None
        tf = fcl.Transform(RotMat, TransMat)
        obj = fcl.CollisionObject(obj, tf)
        return obj

    def check(self, obj1, obj2):
        request = fcl.CollisionRequest()
        result = fcl.CollisionResult()
        ret = fcl.collide(obj1, obj2, request, result)
        # print(result)
        return result.is_collision


# 测试碰撞
# 初始化
cc = CollisionCheck()
Rot1 = np.zeros((3, 3))
# 添加对象
box = cc.addObject('Box', [1, 1, 1], [0, 0, 0, 0], [0, 0, 1.51])
sphere = cc.addObject('Sphere', [1], [0, 0, 0, 0], [0, 0, 0])
# 检测
print(cc.check(box, sphere))
