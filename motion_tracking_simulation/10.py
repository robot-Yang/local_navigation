# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2019-10-20 14:11:56

import matplotlib.pyplot as plt
import numpy as np
from random import random

x_camera_traj, y_camera_traj = [], []
x_center_traj, y_center_traj = [], []
Rho = []
RhoStar = []
Chair_bottom_rho = []
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
safe_distance = 0.35 # distanc between attractor (the destination of camera,not CoQolo) and chair's front edge

alpha_bar = 40
d = safe_distance + chair_length / 2
l = 0.1

Kp_rho = 0.5 # depends on the real Qolo's speed
Kp_alpha = 2 #15
# Kp_beta = -((3*d)/2 + 6*l + 9/4)/(2*d*np.sin((np.pi*alpha_bar)/180)**2 + 3*l*np.sin((np.pi*alpha_bar)/180)**2 - 2*np.sin((np.pi*alpha_bar)/180)**2)
Kp_beta = 10
print(Kp_beta)

original = 0
sequence = 5
A = [original] * sequence
B = [original] * sequence

# ax = plt.gca()
# ax.set_aspect(1)

# fig = plt.figure(figsize=(6, 6))

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
    absAlpha = [abs(i) for i in Alpha]
    max_index0 = absFOV.index(max(absFOV))
    # max_index1 = absAlpha.index(max(absAlpha))
    X_fov = x_camera_traj[max_index0]
    Y_fov = y_camera_traj[max_index0]

    # plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
    # plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
    # plt.scatter(x_camera_traj[-1], y_camera_traj[-1], s=60, c='b', marker=".", zorder=30)
    # plt.scatter(x_center_traj[-1], y_center_traj[-1], s=60, c='b', marker=".", zorder=30)

    # print("Start Point BearingAngle =", absFOV[0] * 180 / np.pi)
    # print("max BearingAngle =", max(absFOV) * 180 / np.pi, "position =", X_fov, Y_fov)
    print("Start Point Alpha =", absAlpha[0])
    print("max Alpha =", max(absAlpha))

    # show velocity/aceelaration of linear and angular
    timeSeries = np.linspace(0,len(FOV)*dt,len(FOV))
    timeSeries0 = np.linspace(0,len(AlphaDot)*dt,len(AlphaDot))
    # print(len(timeSeries), len(timeSeries0))
    # plt.figure('FOV')
    # plt.plot(timeSeries, FOV, 'r-')
    # plt.ylim(0,min(FOV),max(FOV))
    # plt.xlabel("time(s)")
    # plt.ylabel("FOV")

    plt.figure('V-Rho')
    plt.plot(Rho, V, 'r-')
    plt.xlabel("Rho")
    plt.ylabel("linear Velocity(m/s)")

    plt.figure('W-Rho')
    degreeW = [i*180/np.pi for i in W]
    plt.plot(Rho, degreeW, 'b-')
    plt.xlabel("Rho")
    plt.ylabel("Angular Velocity(degree/s)")
    # plt.legend(labels = [startPoint[2]],loc='best')
    # # plt.savefig("./Output_curve/V-Rho.png")
    
    plt.figure('Alpha-Rho')
    plt.plot(Rho, Alpha, 'b-')
    plt.xlabel("Rho")
    plt.ylabel("Alpha(degree)")

    plt.figure('Beta-Rho')
    plt.plot(Rho, Beta, 'r-')
    plt.xlabel("Rho")
    plt.ylabel("Beta(degree)")

    plt.figure('RhoStar-Rho')
    plt.plot(Rho, RhoStar, 'r-')
    plt.xlabel("Rho")
    plt.ylabel("RhoStar")
    # plt.savefig("./Output_curve/V-Rho.png")

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
        self.rho = np.sqrt(self.c_x_diff**2 + self.c_y_diff**2)
        Rho.append(self.rho)
        

    def trajCollect(self):
        x_camera_traj.append(self.x_camera)
        y_camera_traj.append(self.y_camera)
        x_center_traj.append(self.x_center)
        y_center_traj.append(self.y_center)

    def Angle(self):
        self.alpha = np.arctan2(self.c_y_diff, self.c_x_diff) - self.theta
        self.beta = - np.arctan2(self.c_y_diff, self.c_x_diff) + theta_goal
        self.bearingAngle = np.arctan2(self.c_y_diff, self.c_x_diff) - self.theta        # self.n_beta = - np.arctan2(self.n_y_diff, self.n_x_diff) + theta_goal
        self.rhoStar = np.sqrt(self.rho**2 + d**2 -2*self.rho*d*np.cos(self.beta))
        Alpha.append(self.alpha*180/np.pi)
        Beta.append(self.beta*180/np.pi)
        RhoStar.append(self.rhoStar)
        # print(self.alpha)
        # print(self.beta)

    def AngleDot(self):
        self.alphaDot = (Alpha[-1] - Alpha[-2]) / dt
        self.betaDot = (Beta[-1] - Beta[-2]) / dt
        AlphaDot.append(self.alphaDot)
        BetaDot.append(self.betaDot)

    def SpeedToGo(self):
        # self.v =  Kp_rho * self.rho * np.cos(self.alpha)
        # self.w =  Kp_alpha * np.sin(self.alpha) * np.cos(self.alpha) - Kp_beta * self.beta * ((np.sin(alpha_bar*np.pi/180))**2 - np.sin(self.alpha)**2)
        cosA = (self.rhoStar**2 + d**2 - self.rho**2) / (2*self.rhoStar*d)
        self.v =  np.sign(-cosA) * Kp_rho * self.rhoStar * np.cos(self.alpha)
        self.w = Kp_alpha * np.sin(self.alpha) * np.cos(self.alpha) - Kp_beta * self.beta * ((np.sin(alpha_bar*np.pi/180))**2 - np.sin(self.alpha)**2)
        # if self.alpha > np.pi / 2 or self.alpha < -np.pi / 2:
        #     self.v = - self.v

    def CurrentPosition(self):
        self.theta = self.theta + self.w * dt
        self.x_center = self.x_center + self.v * np.cos(self.theta) * dt
        self.y_center = self.y_center + self.v * np.sin(self.theta) * dt
        self.x_camera = self.x_center + self.deviation * np.cos(self.theta)
        self.y_camera = self.y_center + self.deviation * np.sin(self.theta)

    def PlotAll(self):
        plt.figure('trajectory')
        ax = plt.gca()
        ax.set_aspect(1)
        # plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
        #           0.15*np.sin(theta_start), color='r', width=0.03)
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
        plt.annotate('Center of Chair(Objective)', xy=(chair_bottom_x, chair_bottom_y), xytext=(0.55, chair_bottom_y+0.05), 
            arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.15)) # annotation of text: 'center of chair'
        plt.annotate('Location of Attractor', xy=(Chair[0], Chair[1]), xytext=(0.55, Chair[1]+0.05), 
            arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.15)) # annotation of text
        # plt.annotate('Center of Qolo', xy=(0.2,-1), xytext=(0.55,-1+0.075), 
        #     arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.15)) # annotation of text
        # plt.annotate('Trajectory of Camera', xy=(0,-0.5), xytext=(0.55,-0.5+0.075), 
        #     arrowprops=dict(headlength=8,headwidth=5,width=0.5, facecolor='black', shrink=0.25)) # annotation of text
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
        self.x_center = x_start
        self.y_center = y_start
        self.x_camera = x_start + self.deviation * np.cos(theta_start)
        self.y_camera = y_start + self.deviation * np.sin(theta_start)
        self.theta = theta_start

        self.setDestination()
        self.distance()
        self.Angle()
        self.collect(L_x_chair, L_y_chair, R_x_chair, R_y_chair)
        self.trajCollect()

        count = 0

        while (self.rho > d or abs(self.alpha+self.beta) > 0) and count < 2100:
        # while (self.rho > 0.05) and count < 500:
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
            self.trajCollect()

        if count >= 4000:
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

        plt.plot(x_camera_traj, y_camera_traj, 'r--')
        # plt.plot(x_center_traj, y_center_traj, 'b--')  

        # plt.plot([self.x_camera,x_goal],[self.y_camera,y_goal], color ='gray', linewidth=1.5, linestyle="--")
        # plt.plot([self.x_camera, p1[0]],[self.y_camera, p1[1]], color ='gray', linewidth=1.5, linestyle="--")

        #plt.axis("equal")
        # plt.xlim(-0.5, 0.5)
        # plt.ylim(-1, 1)
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
# Chair = [(-0.2, 1, np.pi/3), (-0.1, 1, np.pi/3), (0, 1, np.pi/3), (0.2, 1, np.pi/2)]
Chair = (0, 0, np.pi/2) # this is the location of attractor
x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(Chair)
StartPoint = []
requiredMinAngle = - 20
requiredMaxAngle = 20
requireMaxDistance = 2
requireMinDistance = 1.5

# for requiredDistance in np.linspace(requireMinDistance, requireMaxDistance, 5):
#     for requiredAngle in np.linspace(requiredMinAngle, requiredMaxAngle, 5):
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

# print(StartPoint)
# StartPoint = [(-0.2, -1, np.pi*2/3), (-0.2, -1, np.pi/2), (-0.2, -1, np.pi/3), (0, -1, np.pi/2), (0.2, -1, np.pi*2/3), (0.2, -1, np.pi/2), (0.2, -1, np.pi/3)]
StartPoint = [(-0.2, -1, np.pi*2/3)]

if __name__ == '__main__':
    for i in StartPoint:
        # print ("FFF",x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y)
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
        AlphaDot = [0]
        BetaDot = [0]
        V = [0]
        W = [0]
        # Kp_beta = -((3*d)/2 + 6*l + 9/4)/(2*d*np.sin((np.pi*alpha_bar)/180)**2 + 3*l*np.sin((np.pi*alpha_bar)/180)**2 - 2*np.sin((np.pi*alpha_bar)/180)**2)
        

        
plt.show()



