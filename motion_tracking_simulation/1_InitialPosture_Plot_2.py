# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-06-08 00:42:32

# for plot all initial states based on simuation result analysis

import matplotlib.pyplot as plt
import numpy as np
from random import random

chair_width = 0.5
chair_length = 0.5
safe_distance = 0.45 # distanc between attractor and chair's front edge

def chair_info(chair):
    x_goal = chair[0]
    y_goal = chair[1]
    theta_goal = chair[2]
    F_x_chair = x_goal + safe_distance * np.cos(theta_goal)
    F_y_chair = y_goal + safe_distance * np.sin(theta_goal)
    L_x_chair = F_x_chair + chair_width / 2 * np.cos(theta_goal + np.pi/2)
    L_y_chair = F_y_chair + chair_width / 2 * np.sin(theta_goal + np.pi/2)
    R_x_chair = F_x_chair + chair_width / 2 * np.cos(theta_goal - np.pi/2)
    R_y_chair = F_y_chair + chair_width / 2 * np.sin(theta_goal - np.pi/2)
    chair_bottom_x = F_x_chair + chair_length / 2 * np.cos(theta_goal)
    chair_bottom_y = F_y_chair + chair_length / 2 * np.sin(theta_goal)
    chair_back_x = F_x_chair + chair_length * np.cos(theta_goal)
    chair_back_y = F_y_chair + chair_length  * np.sin(theta_goal)
    return x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y


class chen():
    def __init__(self):

        self.x_camera = 0
        self.y_camera = 0.1
        self.x_center = 0
        self.y_center = 0
        self.deviation = 0.1

        self.dest_X = 0
        self.dest_Y = 0

    def PlotAll(self):
        plt.figure('trajectory')
        ax = plt.gca()
        ax.set_aspect(1)
        # plt.arrow(x_start, y_start, 0.1*np.cos(theta_start),
        #           0.1*np.sin(theta_start), color='b', width=0.02)
        plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                  0.15*np.sin(theta_goal), color='g', width=0.03)
        plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
        plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)

        plt.scatter(chair_bottom_x, chair_bottom_y, s=60, c='r', marker="x")

        for i in LinePoint:
            plt.plot([chair_bottom_x, i[0]],[chair_bottom_y,i[1]], color ='gray', linewidth=1.5, linestyle="--")

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair):
        self.PlotAll()

    def main(self): 
        self.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair)


a = chen()
# Chair = [(-0.2, 1, np.pi/3), (-0.1, 1, np.pi/3), (0, 1, np.pi/3), (0.2, 1, np.pi/2)]
Chair = (0, 0, np.pi/2) # this is the location of attractor
x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(Chair)
StartPoint = []
LinePoint = []
alpha_bar = 40

requiredMinAngle = - 40
requiredMaxAngle = 40
requireMaxDistance = 2
requireMinDistance = 1.5

# for requiredDistance in np.linspace(requireMinDistance, requireMaxDistance+1, 3):
#     for requiredAngle in np.linspace(requiredMinAngle, requiredMaxAngle, 10):
#         startPoint_x = chair_bottom_x + requiredDistance * np.sin(requiredAngle * np.pi/180)
#         startPoint_y = chair_bottom_y - requiredDistance * np.cos(requiredAngle * np.pi/180)

#         # startPoint_x = 0
#         # startPoint_y = chair_bottom_y - 2
#         c_x_diff = chair_bottom_x - startPoint_x
#         c_y_diff = chair_bottom_y - startPoint_y
#         feasiblePostureMin = np.arctan2(c_y_diff, c_x_diff) - (40) * np.pi / 180
#         feasiblePostureMax = np.arctan2(c_y_diff, c_x_diff) + (40) * np.pi / 180
#         for feasiblePosture in np.linspace(feasiblePostureMin, feasiblePostureMax, 3):
#             startPoint = (startPoint_x, startPoint_y, feasiblePosture)
#             StartPoint.append(startPoint)

k4 = 1
sam_len = 3
Rhoo = []
Alphaa = []
Phii = []
for rho in np.linspace(0.1, 1, sam_len):
    phi_max = rho**2 / k4**2
    for phi in np.linspace(-phi_max, phi_max, sam_len):
        alpha_max = (1- abs(phi) / phi_max) * (alpha_bar*np.pi/180)
        Alpha = np.linspace(-alpha_max, alpha_max, sam_len)
        Alpha = Alpha.tolist()
        # print ('Alpha=', Alpha)
        # print (type(Alpha))

        conRho = [rho] * sam_len
        conPhi = [phi] * sam_len
        Rhoo = Rhoo + conRho
        Phii = Phii + conPhi
        # print('Alphaa=', Alphaa)
        Alphaa.extend(Alpha)
        # print('Alphaa=', Alphaa)
        # size_Rhoo = len(Rhoo)
        # size_Alphaa = len(Alphaa)

# tranform (rho, alpha, phi) into (x,y,theta)
# for rho in Rhoo:
#     for alpha in Alphaa:
#         for phi in Phii:
#             startPoint_x = - rho * np.sin(Phii)
#             startPoint_y = - rho * np.cos(Phii)
#             feasiblePosture = np.pi - alpha - phi
#             startPoint = (startPoint_x, startPoint_y, feasiblePosture)
#             StartPoint.append(startPoint)


lineDistance = requireMaxDistance
for requiredAngle in np.linspace(requiredMinAngle, requiredMaxAngle, 3):
    linePoint_x = chair_bottom_x + lineDistance * np.sin(requiredAngle * np.pi/180)
    linePoint_y = chair_bottom_y - lineDistance * np.cos(requiredAngle * np.pi/180)
    linePoint = (linePoint_x, linePoint_y)
    LinePoint.append(linePoint)

if __name__ == '__main__':
    for i in StartPoint:
        x_start = i[0]
        y_start = i[1]
        theta_start = i[2]
        a.main()
     
plt.xlim(-2, 2)
plt.ylim(-2.5, 1)
plt.xticks(fontsize=16) 
plt.yticks(fontsize=16) 
plt.xlabel(r'$x$''(meter)', fontsize=16)
plt.ylabel(r'$y$''(meter)', fontsize=16)
plt.axis('equal')
plt.tight_layout()

plt.show()



