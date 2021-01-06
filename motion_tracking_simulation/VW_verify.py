# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-12-03 20:40:27

import matplotlib.pyplot as plt
import numpy as np
from random import random

x_camera_traj, y_camera_traj = [], []
x_center_traj, y_center_traj = [], []

dt = 1.0/30 # frequeny is 30HZ

R = 0.62

show_animation = True

class chen():
    def __init__(self):
        self.v = 0
        self.w = 0

        self.x_center = 0
        self.y_center = 0

    def trajCollect(self):
        x_center_traj.append(self.x_center)
        y_center_traj.append(self.y_center)
        # wheel_L_x_traj.append(self.wheel_L_x)
        # wheel_L_y_traj.append(self.wheel_L_y)
        # wheel_R_x_traj.append(self.wheel_R_x)
        # wheel_R_y_traj.append(self.wheel_R_x)

    # change speed here
    def SpeedToGo(self):
        self.v = 2 # linear veloity, m/s
        self.w = 0.1 # angular veloity, rad/s
    
    def CurrentPosition(self):
        self.theta = self.theta + self.w * dt
        self.x_center = self.x_center + self.v * np.cos(self.theta) * dt
        self.y_center = self.y_center + self.v * np.sin(self.theta) * dt
        # self.wheel_L_x = self.x_center + R * np.cos(self.theta + np.pi/2)
        # self.wheel_L_y = self.x_center + R * np.sin(self.theta + np.pi/2)
        # self.wheel_R_x = self.x_center + R * np.cos(self.theta - np.pi/2)
        # self.wheel_R_x = self.x_center + R * np.cos(self.theta - np.pi/2)

    def PlotAll(self):
        plt.figure('Trajectory')
        plt.cla()
        plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
              0.15*np.sin(theta_start), color='r', width=0.03)
        self.plot_vehicle()

    def move_to_pose(self, x_start, y_start, theta_start):
        self.x_center = x_start
        self.y_center = y_start
        self.theta = theta_start
        self.trajCollect()
        count = 0

        while count < 100: # ccontrol the total time, 100/30 = 3.3 seconds
            count += 1

            self.SpeedToGo()

            self.CurrentPosition()
            self.trajCollect()

        plt.show()
        self.PlotAll()

    def plot_vehicle(self):  # pragma: no cover
        # Corners of triangular vehicle when pointing to the right (0 radians)
        p1_i = np.array([0.15, 0, 1]).T
        p2_i = np.array([-0.15, 0.075, 1]).T
        p3_i = np.array([-0.15, -0.075, 1]).T

        T = self.transformation_matrix()
        p1 = np.matmul(T, p1_i)
        p2 = np.matmul(T, p2_i)
        p3 = np.matmul(T, p3_i)

        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
        plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'k-')
        plt.plot([p3[0], p1[0]], [p3[1], p1[1]], 'k-')

        # plt.plot(x_camera_traj, y_camera_traj, 'r--')
        plt.plot(x_center_traj, y_center_traj, 'b--')  

        plt.axis("equal")
        plt.xticks(fontsize=16) 
        plt.yticks(fontsize=16) 
        plt.xlabel(r'$x$''(meter)', fontsize=16)
        plt.ylabel(r'$y$''(meter)', fontsize=16)
        plt.tight_layout()

    def transformation_matrix(self):
        return np.array([
            [np.cos(self.theta), -np.sin(self.theta), self.x_center],
            [np.sin(self.theta), np.cos(self.theta), self.y_center],
            [0, 0, 1]
        ])

    def main(self): 
        self.move_to_pose(x_start, y_start, theta_start)


StartPoint = [0, 0, 90* np.pi / 180]
print(StartPoint)

a = chen()
x_start = StartPoint[0]
y_start = StartPoint[1]
theta_start = StartPoint[2]
a.main()


plt.show()


