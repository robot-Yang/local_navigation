# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2019-10-12 17:17:53

import matplotlib.pyplot as plt
import numpy as np
from random import random

x_camera_traj, y_camera_traj = [], []
x_center_traj, y_center_traj = [], []
Rho = []
Alpha = []
Beta = []
AlphaDot = [0]
BetaDot = [0]

V = [0]
W = [0]
A_V = []
A_W = []
FOV = []
C_FOV = []
L_FOV = []
R_FOV = []

v_threshold = 25
w_threshold = 5
a_v_threshold = 5
a_w_threshold = 4

Kp_rho = 0.5 # depends on the real Qolo's speed
# K4 = 3.21
# K = [8.31,6.42] 
# K4 = 1.43
# K = [6.57,2.86]
K4 = 4.85
# K = [5.6, 1.06]
# K4 = 0.53
K = [2, 12.4] 
# K = [4.36, 0.85]
Kp_alpha = K[0] #15
Kp_beta = K[1] #2   # 3 is better than 5 or 10 or 15
dt = 0.05
chair_width = 0.5
chair_length = 0.5
safe_distance = 0.35 # distanc between destination and chair's front edge
x_start = 0.0
y_start = 0.0
theta_start = np.pi/2

original = 0
sequence = 5
A = [original] * sequence
B = [original] * sequence

show_animation = True
ax = plt.gca()
ax.set_aspect(1)

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

# for both move_average and butterworth filter
def read_update(a,b):
    A.append(a)
    B.append(b)
    A.pop(0)
    B.pop(0)
    # return A, B, C, D, E

# move_average filter
def move_average():
    #global A, B
    a1 = sum(A) / sequence
    b1 = sum(B) / sequence
    return a1, b1

def collectPlot():
    absFOV = [abs(i) for i in FOV]
    max_index0 = absFOV.index(max(absFOV))
    X_fov = x_camera_traj[max_index0]
    Y_fov = y_camera_traj[max_index0]
    # min_index1 = C_FOV.index(min(C_FOV))
    # C_X_fov = x_camera_traj[min_index1]
    # C_Y_fov = y_camera_traj[min_index1]
    # max_index2 = L_FOV.index(max(L_FOV))
    # L_X_fov = x_camera_traj[max_index2]
    # L_Y_fov = y_camera_traj[max_index2]
    # max_index3 = R_FOV.index(max(R_FOV))
    # R_X_fov = x_camera_traj[max_index3]
    # R_Y_fov = y_camera_traj[max_index3]

    # plt.scatter(X_fov, Y_fov, s=50, c='r', marker="x")
    plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
    plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
    plt.scatter(x_camera_traj[-1], y_camera_traj[-1], s=60, c='b', marker=".", zorder=30)
    # plt.scatter(C_X_fov, C_Y_fov, s=50, c='r', marker="o")
    # plt.scatter(L_X_fov, L_Y_fov, s=50, c='r', marker="x")
    # plt.scatter(R_X_fov, R_Y_fov, s=50, c='b', marker="x")

    print("max BearingAngle =", max(absFOV) * 180 / np.pi, "position =", X_fov, Y_fov)
    # print("min C_FOV =", min(C_FOV) * 180 / np.pi, "position =", C_X_fov, C_Y_fov)
    # print("max L_FOV =", max(L_FOV) * 180 / np.pi, "position =", L_X_fov, L_Y_fov)
    # print("max R_FOV =", max(R_FOV) * 180 / np.pi, "position =", R_X_fov, R_Y_fov)
    # print ("final_FOV_diff =", C_FOV[-1] * 180 / np.pi)

class chen():
    def __init__(self):
        # simulation parameters
        self.v0 = 0
        self.w0 = 0
        self.v = 0
        self.w = 0

        self.x_camera = 0
        self.y_camera = 0.1
        self.x_center = 0
        self.y_center = 0
        self.deviation = 0.1

        self.dest_X = 0
        self.dest_Y = 0

        self.L_fov = 0
        self.R_fov = 0

        self.AngleCenter = 0

    def setDestination(self):
        self.dest_X = x_goal
        self.dest_Y = y_goal

    def distance(self):
        self.x_diff = self.dest_X - self.x_camera
        self.y_diff = self.dest_Y - self.y_camera
        self.c_x_diff = chair_bottom_x - self.x_camera
        self.c_y_diff = chair_bottom_y - self.y_camera
        # self.goal_x_diff = chair_bottom_x - self.dest_X
        # self.goal_y_diff = chair_bottom_y - self.dest_Y
        self.rho = np.sqrt(self.x_diff**2 + self.y_diff**2)
        Rho.append(self.rho)
        self.chair_bottom_rho = np.sqrt(self.c_x_diff**2 + self.c_y_diff**2)

    def trajPlot(self):
        x_camera_traj.append(self.x_camera)
        y_camera_traj.append(self.y_camera)
        x_center_traj.append(self.x_center)
        y_center_traj.append(self.y_center)

    def Angle(self):
        self.alpha = np.arctan2(self.y_diff, self.x_diff) - self.theta
        self.alphaStar = np.arctan2(self.c_y_diff, self.c_x_diff) - self.theta
        self.beta = - np.arctan2(self.y_diff, self.x_diff) + theta_goal
        self.bearingAngle = np.arctan2(self.c_y_diff, self.c_x_diff) - self.theta
        self.spiralBeta = theta_goal - np.arctan2(self.c_y_diff, self.c_x_diff)
        self.hh = np.log((safe_distance + chair_length/2) / self.chair_bottom_rho)
        self.spiralAngle = np.arctan(self.spiralBeta/self.hh)
        Alpha.append(self.alpha*180/np.pi)
        Beta.append(self.beta*180/np.pi)

    def AngleDot(self):
        self.alphaDot = (Alpha[-1] - Alpha[-2]) / dt
        self.betaDot = (Beta[-1] - Beta[-2]) / dt
        AlphaDot.append(self.alphaDot)
        BetaDot.append(self.betaDot)

    def SpeedToGo(self):
        self.v =  Kp_rho * self.rho * np.cos(self.alpha)
        self.w =  Kp_alpha * np.sin(self.alpha) * np.cos(self.alpha) - Kp_beta * self.beta * ((np.sin(40*np.pi/180))**2 - np.sin(self.alphaStar)**2)
        if self.alpha > np.pi / 2 or self.alpha < -np.pi / 2:
            self.v = - self.v

    def CurrentPosition(self):
        self.theta = self.theta + self.w * dt
        self.x_center = self.x_center + self.v * np.cos(self.theta) * dt
        self.y_center = self.y_center + self.v * np.sin(self.theta) * dt
        self.x_camera = self.x_center + self.deviation * np.cos(self.theta)
        self.y_camera = self.y_center + self.deviation * np.sin(self.theta)

    def PlotAll(self):
        plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
                  0.15*np.sin(theta_start), color='r', width=0.03)
        plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                  0.15*np.sin(theta_goal), color='g', width=0.03)
        # rect0 = plt.Rectangle((F_x_chair, F_y_chair), chair_length, chair_width/2, angle = theta_goal * 180 / np.pi, fill=False, edgecolor = 'red',linewidth=1)
        # ax.add_patch(rect0)
        # rect1 = plt.Rectangle((R_x_chair, R_y_chair), chair_length, chair_width/2, angle = theta_goal * 180 / np.pi, fill=False, edgecolor = 'red',linewidth=1)
        # ax.add_patch(rect1)
        # plt.scatter(F_x_chair, F_y_chair, s=50, c='r', marker="x")
        # plt.scatter(L_x_chair, L_y_chair, s=50, c='r', marker="x")
        # plt.scatter(R_x_chair, R_y_chair, s=50, c='r', marker="x")
        plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
        self.plot_vehicle()
        #plt.scatter(0,4, c='r', marker="o")

    def collect(self, L_x_chair, L_y_chair, R_x_chair, R_y_chair):
        L_x_diff = L_x_chair - self.x_camera
        L_y_diff = L_y_chair - self.y_camera
        # L_fov = (np.arctan2(L_x_diff, L_y_diff) - theta + np.pi) % (2 * np.pi) - np.pi
        L_line = np.arctan2(L_y_diff, L_x_diff)
        self.L_fov = np.arctan2(L_y_diff, L_x_diff) - self.theta
        R_x_diff = R_x_chair - self.x_camera
        R_y_diff = R_y_chair - self.y_camera
        # R_fov = (np.arctan2(R_x_diff, R_y_diff) - theta + np.pi) % (2 * np.pi) - np.pi
        R_line = np.arctan2(R_y_diff, R_x_diff)
        self.R_fov = np.arctan2(R_y_diff, R_x_diff) - self.theta
        self.AngleCenter = (np.arctan2(R_y_diff, R_x_diff) + np.arctan2(L_y_diff, L_x_diff)) / 2
        FOV.append(self.bearingAngle)  # field of view
        C_FOV.append(abs(self.theta - theta_goal))
        L_FOV.append(abs(self.L_fov))
        R_FOV.append(abs(self.R_fov))

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair):
        """
        rho is the distance between the robot and the goal position
        alpha is the angle to the goal relative to the heading of the robot
        beta is the angle between the robot's position and the goal position plus the goal angle

        Kp_rho*rho and Kp_alpha*alpha drive the robot along a line towards the goal
        Kp_beta*beta rotates the line so that it is parallel to the goal angle
        """
        self.x_center = x_start
        self.y_center = y_start
        self.x_camera = x_start
        self.y_camera = y_start + self.deviation
        self.theta = theta_start

        self.setDestination()
        self.distance()
        self.Angle()
        self.firstspiralAngle = self.spiralAngle
        self.collect(L_x_chair, L_y_chair, R_x_chair, R_y_chair)
        self.trajPlot()

        count = 0

        # while (self.rho > 0.01 or abs(self.alpha-self.beta) > 0.01) and count < 150:
        while (self.rho > 0.05) and count < 220:
            count += 1
            # print("count =", count)

            self.SpeedToGo()

            # filter
            read_update(self.v, self.w)
            self.v, self.w = move_average()

            # for monitoring v, w a_v, a_w
            V.append(self.v)
            W.append(self.w)
            # a_v = self.v - self.v0
            # a_w = self.w - self.w0
            # A_V.append(a_v)
            # A_W.append(a_w)
            # print("v =", v, "w =", w)

            self.CurrentPosition()
            self.distance()
            self.Angle()
            self.AngleDot()
            self.collect(L_x_chair, L_y_chair, R_x_chair, R_y_chair)
            self.trajPlot()

        if count >= 120:
            print("timeout")

        # print ("x_traj, y_traj= ", x_traj, y_traj)
        collectPlot()
        # plt.show()
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

        plt.plot(x_camera_traj, y_camera_traj, 'b--')
        # plt.plot(x_center_traj, y_center_traj, 'r--')  

        # plt.plot([self.x_camera,x_goal],[self.y_camera,y_goal], color ='gray', linewidth=1.5, linestyle="--")
        # plt.plot([self.x_camera, p1[0]],[self.y_camera, p1[1]], color ='gray', linewidth=1.5, linestyle="--")

        #plt.axis("equal")
        plt.xlim(-1, 3)
        plt.ylim(-1, 3)
        # plt.pause(dt)

    def transformation_matrix(self):
        return np.array([
            [np.cos(self.theta), -np.sin(self.theta), self.x_camera],
            [np.sin(self.theta), np.cos(self.theta), self.y_camera],
            [0, 0, 1]
        ])

    def main(self): 
        self.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair)

        # for different locations
        self.v0 = 0
        self.w0 = 0
        self.v = 0
        self.w = 0

        self.x_camera = 0
        self.y_camera = 0.1
        self.x_center = 0
        self.y_center = 0
        self.deviation = 0.1

        self.dest_X = 0
        self.dest_Y = 0

        self.L_fov = 0
        self.R_fov = 0

        self.AngleCenter = 0

a = chen()
Chair = [(-0.2, 1, np.pi/3), (-0.1, 1, np.pi/3), (0, 1, np.pi/3), (0.2, 1, np.pi/2)]
# Chair = [(0.2, 1, np.pi/3)]
if __name__ == '__main__':
    for i in Chair:
        # fig = plt.gcf()
        print('x_camera_traj =', x_camera_traj)
        x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(i)
        print ("FFF",x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y)
        a.main()

        # save previous data
        # x_camera_trajSave, y_camera_trajSave = x_camera_traj, y_camera_traj


        # for different locations
        x_camera_traj, y_camera_traj = [], []
        x_center_traj, y_center_traj = [], []
        FOV = []
        
plt.show()


