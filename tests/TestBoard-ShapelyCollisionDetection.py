import cv2
import numpy as np
import sys
import src.PDDTVisionToolBox as pd

from shapely.geometry import Polygon as pl1
from shapely.geometry import Point as pt1


# RRT算法测试

def obstacle_collision_check_Sphere(Obstacle, Point, Radius):
    """
    球形障碍物检测
    :param Obstacle: 障碍物中心
    :param Point: 点
    :param Radius: 半径
    :return: 碰撞结果
    """
    # 循环计算距离
    for i in range(len(Obstacle)):
        if np.linalg.norm(Obstacle[i] - Point) <= Radius[i]:
            return True
    # 当且仅当遍历所有障碍物均未包络后，返回False
    else:
        return False


def obstacle_collision_check_Polygon(Obstacle, Point):
    """
    多边形障碍物检测
    :param Obstacle: 障碍物
    :param Point: 点
    :return: 碰撞结果
    """
    # 生成点
    Point = pt1(Point[0], Point[1], Point[2])
    # 循环检测是否在各障碍物内
    for i in range(len(Obstacle)):
        # 生成封闭多边形
        Polygon = pl1(Obstacle[i])
        # 检测是否在多边形内
        if Polygon.contains(Point):
            return True
    # 当且仅当遍历所有障碍物均未包络后，返回False
    else:
        return False


# 执行主程序
if __name__ == '__main__':
    # 障碍物
    # 球形障碍物
    ObstacleSphere = [[500, 100, 800], [800, -200, 1000], [-400, 600, 1200], [1000, 2000, 700], [1500, 0, 3000]]
    ObstacleSphereRadius = [100, 100, 200, 300, 400]
    # 多边形障碍物
    ObstaclePolygon = [
        [(1000, 1000, 0), (500, 500, 0), (500, 1000, 0), (1000, 500, 0), (1000, 1000, 2000), (500, 500, 2000),
         (500, 1000, 2000), (1000, 500, 2000)]]
    # 检测点
    Point = np.array([1200, 1500, 1500])
    # 球形障碍物检测
    print("球形障碍物检测：", obstacle_collision_check_Sphere(ObstacleSphere, Point, ObstacleSphereRadius))
    # 多边形障碍物检测
    print("多边形障碍物检测：", obstacle_collision_check_Polygon(ObstaclePolygon, Point))
