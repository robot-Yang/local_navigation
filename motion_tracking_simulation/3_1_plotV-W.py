# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-05-26 23:30:23

# simulate all possible initial states, for finding the constrains, 

import matplotlib.pyplot as plt
import numpy as np
from random import random
import feasible_velocity as fv

x_camera_traj, y_camera_traj = [], []
x_center_traj, y_center_traj = [], []
Rho = []
Alpha = []
Beta = []
AlphaStar = []
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


dt = 0.01
chair_width = 0.5
chair_length = 0.5
safe_distance = 0.45 # distance between attractor and chair's front edge

l = 0.1
d = 0.7

original = 0
sequence = 5
A = [original] * sequence
B = [original] * sequence

DISTANCE = 0.62

# maximum velocity for each wheel (m/s)
v_l_min = -5.44
v_l_max = 5.44
v_r_min = -5.44
v_r_max = 5.44

Left_initialState = []
Left_initialX = []
Left_initialY = []
Left_initialPosture = []
Left_StartPoint = []
Delete_StartPoint = []

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

def transform(a):
    x_diff =  x_goal - a[0]
    y_diff =  y_goal - a[1]
    rho = (x_diff**2 + y_diff**2)**(1/2)
    alpha = (np.arctan2(y_diff, x_diff) - a[2] + np.pi)% (2 * np.pi) - np.pi
    beta = (- np.arctan2(y_diff, x_diff) + theta_goal + np.pi) % (2 * np.pi) - np.pi
    rhoAlphaBeta = [rho, alpha, beta]
    return rhoAlphaBeta

def Left_rhoAlphaBeta_Output():
    print('Left_StartPoint =', Left_StartPoint)
    print('---------------------------------')

    # plt.figure('Left_StartPoint')
    # for i in Left_StartPoint:
    #     x_start = i[0]
    #     y_start = i[1]
    #     theta_start = i[2]
    #     ax = plt.gca()
    #     ax.set_aspect(1)
    #     plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
    #               0.15*np.sin(theta_start), color='r', width=0.03)
    #     plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
    #               0.15*np.sin(theta_goal), color='g', width=0.03)
    #     plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
    #     plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
    #     plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
    #     plt.xlim(-2, 2)
    #     plt.ylim(-2.5, 1) 
    #     
    Left_rhoAlphaBeta = [transform(i) for i in Left_StartPoint]
    print('Left_rhoAlphaBeta =', Left_rhoAlphaBeta)
    print('---------------------------------')
    Left_Rho = [i[0] for i in Left_rhoAlphaBeta]
    Left_Alpha = [i[1] for i in Left_rhoAlphaBeta]
    Left_Beta = [i[1] for i in Left_rhoAlphaBeta]
    print('Left_Rho = ', Left_Rho)
    print('----------------')
    print('Left_Alpha = ', Left_Alpha)
    print('----------------')
    print('Left_Beta = ', Left_Beta)
    print('----------------')

def Deleted_rhoAlphaBeta_Output():
    print('Deleted_StartPoint =', Delete_StartPoint)
    print('---------------------------------')  
    Delete_rhoAlphaBeta = [transform(i) for i in Delete_StartPoint]
    print('Delete_rhoAlphaBeta =', Delete_rhoAlphaBeta)
    print('---------------------------------')
    Delete_Rho = [i[0] for i in Delete_rhoAlphaBeta]
    Delete_Alpha = [i[1] for i in Delete_rhoAlphaBeta]
    Delete_Beta = [i[1] for i in Delete_rhoAlphaBeta]
    print('Delete_Rho = ', Delete_Rho)
    print('----------------')
    print('Delete_Alpha = ', Delete_Alpha)
    print('----------------')
    print('Delete_Beta = ', Delete_Beta)


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
        # print(self.dest_X)
        # print(self.dest_Y)

    def distance(self):
        self.x_diff = self.dest_X - self.x_center
        self.y_diff = self.dest_Y - self.y_center
        self.c_x_diff = chair_bottom_x - self.x_camera
        self.c_y_diff = chair_bottom_y - self.y_camera
        # self.goal_x_diff = chair_bottom_x - self.dest_X
        # self.goal_y_diff = chair_bottom_y - self.dest_Y
        self.rho = np.sqrt(self.x_diff**2 + self.y_diff**2) # * np.sign(np.arctan2(self.y_diff, self.x_diff))
        Rho.append(self.rho)
        self.chair_bottom_rho = np.sqrt(self.c_x_diff**2 + self.c_y_diff**2)

    def trajCollect(self):
        x_camera_traj.append(self.x_camera)
        y_camera_traj.append(self.y_camera)
        x_center_traj.append(self.x_center)
        y_center_traj.append(self.y_center)

    def Angle(self):
        self.alpha = (np.arctan2(self.y_diff, self.x_diff) - self.theta + np.pi) % (2 * np.pi) - np.pi
        self.beta = (- np.arctan2(self.y_diff, self.x_diff) + theta_goal + np.pi) % (2 * np.pi) - np.pi

        # OB = self.rho * np.sin(self.beta) / np.sin(np.pi-self.alpha-self.beta)
        # BC = self.rho * np.sin(self.alpha) / np.sin(np.pi-self.alpha-self.beta)
        # AB = OB - l
        # BD = BC + d
        # AD = (AB**2 + BD**2 - 2*AB*BD*np.cos(np.pi-self.alpha-self.beta))**(1/2)
        # self.alphaStar = np.arcsin(BD*np.sin(np.pi-self.alpha-self.beta) / AD)

        x_o = - self.rho * np.sin(self.beta)
        y_o = - self.rho * np.cos(self.beta)
        theta_o = np.pi/2 - (self.alpha + self.beta)
        x_d = 0
        y_d = d
        theta_d = np.pi/2
        x_a = x_o + l*np.cos(theta_o)
        y_a = y_o + l*np.sin(theta_o)
        theta_a = theta_o
        y_diff_da = y_d - y_a
        x_diff_da = x_d - x_a
        self.alphaStar = np.arctan2(y_diff_da, x_diff_da) - theta_a

        # self.alphaStar = np.arctan2(self.c_y_diff, self.c_x_diff) - self.theta
        Alpha.append(self.alpha*180/np.pi)
        Beta.append(self.beta*180/np.pi)
        AlphaStar.append(self.alphaStar*180/np.pi)

    def AngleDot(self):
        self.alphaDot = (Alpha[-1] - Alpha[-2]) / dt
        self.betaDot = (Beta[-1] - Beta[-2]) / dt
        AlphaDot.append(self.alphaDot)
        BetaDot.append(self.betaDot)

    def SpeedToGo(self):
        self.v =  Kp_rho * (self.rho) * np.cos(self.alpha)
        self.w =  Kp_alpha * np.sin(self.alpha) * np.cos(self.alpha) - Kp_beta * self.beta * ((np.sin(alpha_bar*np.pi/180))**2 - np.sin(self.alphaStar)**2)
        # self.w =  Kp_alpha * np.sin(self.alpha)
        if self.alpha > np.pi / 2 or self.alpha < - np.pi / 2:
            self.v = - self.v

    def CurrentPosition(self):
        self.theta = self.theta + self.w * dt # means positive w --> Qolo turn left 
        self.x_center = self.x_center + self.v * np.cos(self.theta) * dt
        self.y_center = self.y_center + self.v * np.sin(self.theta) * dt
        self.x_camera = self.x_center + self.deviation * np.cos(self.theta)
        self.y_camera = self.y_center + self.deviation * np.sin(self.theta)

    def PlotAll(self):
        plt.figure('V-W')
        plt.plot(V,W,'g-')
        
    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair):
        self.x_center = x_start
        self.y_center = y_start
        self.x_camera = x_start + self.deviation * np.cos(theta_start)
        self.y_camera = y_start + self.deviation * np.sin(theta_start)
        self.theta = theta_start

        self.setDestination()
        self.distance()
        self.Angle()
        self.trajCollect()

        count = 0

        while (self.rho > 0 or abs(self.alpha-self.beta) > 0) and count < 4000:
        # while (self.rho > 0.05) and count < 500:
            count += 1

            self.SpeedToGo()

            # filter
            # read_update(self.v, self.w)
            # self.v, self.w = move_average()

            # for monitoring v, w a_v, a_w
            V.append(self.v)
            W.append(self.w*180/np.pi)

            self.CurrentPosition()
            self.distance()
            self.Angle()
            self.AngleDot()
            self.trajCollect()

        self.PlotAll()


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
Chair = (0, 0, np.pi/2) # this is the location of attractor
x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(Chair)
StartPoint = []
requiredMinAngle = - 40
requiredMaxAngle = 40
requireMaxDistance = 2
requireMinDistance = 1.5
alpha_bar = 40

Kp_rho = 0.15 # depends on the real Qolo's speed
Kp_alpha = 0.6 # 15
# Kp_rho = 0.1 # depends on the real Qolo's speed
# Kp_alpha = 0.4 # 15
Kp_beta = round((Kp_rho - Kp_alpha)**2 / (4 * Kp_rho * np.sin(alpha_bar*np.pi/180)**2), 2) # depends on the linearization result
print(Kp_rho, Kp_alpha, Kp_beta)

# generate all possiable initial states
for requiredDistance in np.linspace(requireMinDistance, requireMaxDistance+1, 10):
    for requiredAngle in np.linspace(requiredMinAngle, requiredMaxAngle, 10):
        startPoint_x = chair_bottom_x + requiredDistance * np.sin(requiredAngle * np.pi/180)
        startPoint_y = chair_bottom_y - requiredDistance * np.cos(requiredAngle * np.pi/180)

        c_x_diff = chair_bottom_x - startPoint_x
        c_y_diff = chair_bottom_y - startPoint_y
        feasiblePostureMin = np.arctan2(c_y_diff, c_x_diff) - (alpha_bar) * np.pi / 180
        feasiblePostureMax = np.arctan2(c_y_diff, c_x_diff) + (alpha_bar) * np.pi / 180
        for feasiblePosture in np.linspace(feasiblePostureMin, feasiblePostureMax, 10):
            startPoint = (startPoint_x, startPoint_y, feasiblePosture)
            StartPoint.append(startPoint)
# print ('All_StartPoint =', StartPoint)

if __name__ == '__main__':
    for i in StartPoint:
        x_start = i[0]
        y_start = i[1]
        theta_start = i[2]
        a.main()

        # reset trajectory list
        x_camera_traj, y_camera_traj = [], []
        x_center_traj, y_center_traj = [], []
        FOV = []
        Rho = []
        Alpha = []
        Beta = []
        AlphaStar = []
        AlphaDot = [0]
        BetaDot = [0]
        V = [0]
        W = [0]

    # Left_rhoAlphaBeta_Output()
    # Deleted_rhoAlphaBeta_Output()

plt.xticks(fontsize=16) 
plt.yticks(fontsize=16) 
plt.xlabel(r'$v$''(m/s)', fontsize=16)
plt.ylabel(r'$w$''(degree/s)', fontsize=16)
# plt.xlabel(r'$\rho$''(meter)', fontsize=16)
# plt.ylabel(r'$\alpha^*$''(degre)', fontsize=16)
plt.tight_layout()
fv.main()

plt.show()



