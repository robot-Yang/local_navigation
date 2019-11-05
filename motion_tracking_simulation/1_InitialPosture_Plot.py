# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2019-10-22 21:51:18

import matplotlib.pyplot as plt
import numpy as np
from random import random

chair_width = 0.5
chair_length = 0.5
safe_distance = 0.45 # distanc between attractor and chair's front edge


# ax = plt.gca()
# ax.set_aspect(1)

# fig = plt.figure(figsize=(6, 6))
# plt.figure('trajectory')

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
        plt.arrow(x_start, y_start, 0.1*np.cos(theta_start),
                  0.1*np.sin(theta_start), color='b', width=0.02)
        plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                  0.15*np.sin(theta_goal), color='g', width=0.03)
        plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
        plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
        # rect0 = plt.Rectangle((F_x_chair, F_y_chair), chair_length, chair_width/2, angle = theta_goal * 180 / np.pi, fill=False, edgecolor = 'red',linewidth=1)
        # ax.add_patch(rect0)
        # rect1 = plt.Rectangle((R_x_chair, R_y_chair), chair_length, chair_width/2, angle = theta_goal * 180 / np.pi, fill=False, edgecolor = 'red',linewidth=1)
        # ax.add_patch(rect1)
        # plt.scatter(F_x_chair, F_y_chair, s=50, c='r', marker="x")
        # plt.scatter(L_x_chair, L_y_chair, s=50, c='r', marker="x")
        # plt.scatter(R_x_chair, R_y_chair, s=50, c='r', marker="x")
        plt.scatter(chair_bottom_x, chair_bottom_y, s=60, c='r', marker="x")
        plt.annotate('Center of Chair(Objective)', xy=(chair_bottom_x, chair_bottom_y), xytext=(0.55, chair_bottom_y+0.05), 
            arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.15)) # annotation of text: 'center of chair'
        plt.annotate('Location of Attractor', xy=(Chair[0], Chair[1]), xytext=(0.55, Chair[1]+0.05), 
            arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.15)) # annotation of text
        # plt.annotate('Center of Qolo', xy=(0.2,-1), xytext=(0.55,-1+0.075), 
        #     arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.15)) # annotation of text
        # plt.annotate('Trajectory of Camera', xy=(0,-0.5), xytext=(0.55,-0.5+0.075), 
        #     arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.25)) # annotation of text
        # self.plot_vehicle()
        # plt.scatter(0,4, c='r', marker="o")
        # 
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
requiredMinAngle = - 20
requiredMaxAngle = 20
requireMaxDistance = 2
requireMinDistance = 1.5
alpha_bar = 40
for requiredDistance in np.linspace(requireMinDistance, requireMaxDistance, 5):
    for requiredAngle in np.linspace(requiredMinAngle, requiredMaxAngle, 5):
        startPoint_x = chair_bottom_x + requiredDistance * np.sin(requiredAngle * np.pi/180)
        startPoint_y = chair_bottom_y - requiredDistance * np.cos(requiredAngle * np.pi/180)

        # startPoint_x = 0
        # startPoint_y = chair_bottom_y - 2
        c_x_diff = chair_bottom_x - startPoint_x
        c_y_diff = chair_bottom_y - startPoint_y
        feasiblePostureMin = np.arctan2(c_y_diff, c_x_diff) - (40) * np.pi / 180
        feasiblePostureMax = np.arctan2(c_y_diff, c_x_diff) + (40) * np.pi / 180
        for feasiblePosture in np.linspace(feasiblePostureMin, feasiblePostureMax, 3):
            startPoint = (startPoint_x, startPoint_y, feasiblePosture)
            StartPoint.append(startPoint)

lineDistance = requireMaxDistance
for requiredAngle in np.linspace(requiredMinAngle, requiredMaxAngle, 5):
    linePoint_x = chair_bottom_x + lineDistance * np.sin(requiredAngle * np.pi/180)
    linePoint_y = chair_bottom_y - lineDistance * np.cos(requiredAngle * np.pi/180)
    linePoint = (linePoint_x, linePoint_y)
    LinePoint.append(linePoint)
# print(StartPoint)
# StartPoint = [(-0.2, -1, np.pi*2/3), (-0.2, -1, np.pi/2), (-0.2, -1, np.pi/3), (0, -1, np.pi/2), (0.2, -1, np.pi*2/3), (0.2, -1, np.pi/2), (0.2, -1, np.pi/3)]
# StartPoint = [(0, 0.2, np.pi/2)]
# StartPoint = [(-0.2, -1, np.pi/2)]

if __name__ == '__main__':
    for i in StartPoint:
        x_start = i[0]
        y_start = i[1]
        theta_start = i[2]
        a.main()
     
plt.xlim(-1, 1)
plt.ylim(-1.5, 0.8)   
plt.show()



