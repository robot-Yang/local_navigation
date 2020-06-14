# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-06-11 19:58:52

# optimize running time regarding plot frequency, simulate all possible initial states, for finding the constrains

import matplotlib.pyplot as plt
import numpy as np
from random import random
import InitialPosture_Plot_4 as IntPoint

x_camera_traj, y_camera_traj = [], []
x_center_traj, y_center_traj = [], []
X_center_traj, Y_center_traj = [], []
center_traj = []
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

dt = 0.1
chair_width = 0.5
chair_length = 0.5
safe_distance = 0.45 # distance between attractor and chair's front edge

l = 0.1 # distance between camera and center of Qolo
d = 0.7 # distance between attractor (destination) and objective (center of chair)

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

def collectPlot():
    plt.figure('AlphaStar-Rho')
    plt.plot(Rho, AlphaStar, 'g-')
    plt.xlabel("Rho")
    plt.ylabel("AlphaStar(degree)")
    # plt.savefig("./Output_curve/V-Rho.png")

    # select the initial states whose AlphaStar is within alphaBar
    
    Abs_AlphaStar = [abs(i) for i in AlphaStar]
    print ('max(Abs_AlphaStarAlphaStar) =', max(Abs_AlphaStar))

    k_final = (AlphaStar[-1]- AlphaStar[-2]) / (Rho[-1] - Rho[-2])

    if AlphaStar[-1] > 0:
        judge = (k_final >=0 and k_final < 150)
    elif AlphaStar[-1] < 0:
        judge = (k_final <=0 and k_final > -150)
    else:
        judge = (k_final <150 and k_final > -150)
    # print (judge)

    if max(Abs_AlphaStar) < 40 and judge:
        plt.figure('Left_initialState')
        # plt.figure('trajectory')
        ax = plt.gca()
        ax.set_aspect(1)
        plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
                  0.15*np.sin(theta_start), color='r', width=0.03)
        plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                  0.15*np.sin(theta_goal), color='g', width=0.03)
        plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
        plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
        plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
        plt.xlim(-2, 2)
        plt.ylim(-2.5, 1)   

        plt.figure('Left_AlphaStar-Rho')
        plt.plot(Rho, AlphaStar, 'g-')
        plt.xlabel("Rho")
        plt.ylabel("AlphaStar(degree)")

        plt.figure('Left_trajectory')
        ax = plt.gca()
        ax.set_aspect(1)
        plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
                  0.15*np.sin(theta_start), color='r', width=0.03)
        plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                  0.15*np.sin(theta_goal), color='g', width=0.03)
        plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
        self.plot_vehicle()

def PlotAll():
    plt.figure('trajectory')
    ax = plt.gca()
    ax.set_aspect(1)
    plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
              0.15*np.sin(theta_start), color='r', width=0.03)
    plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
              0.15*np.sin(theta_goal), color='g', width=0.03)
    plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
    # a.plot_vehicle()
    # print (len(X_center_traj))
    # print (X_center_traj[0])

    # plt.plot(center_traj[0],center_traj[1], center_traj[2],center_traj[3],'b--') 
    plt.plot(*center_traj) 
    print (len(center_traj))
    # plt.plot(X_center_traj, Y_center_traj, 'b--')  

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
        self.alpha = np.arctan2(self.y_diff, self.x_diff) - self.theta 
        self.beta = - np.arctan2(self.y_diff, self.x_diff) + theta_goal 

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

    # control law
    def SpeedToGo(self):
        self.v =  Kp_rho * (self.rho) * np.cos(self.alpha)
        self.w =  Kp_alpha * np.sin(self.alpha) * np.cos(self.alpha) - Kp_beta * self.beta * ((np.sin(alpha_bar*np.pi/180))**2 - np.sin(self.alphaStar)**2)

    def CurrentPosition(self):
        self.theta = self.theta + self.w * dt # means positive w --> Qolo turn left 
        self.x_center = self.x_center + self.v * np.cos(self.theta) * dt
        self.y_center = self.y_center + self.v * np.sin(self.theta) * dt
        self.x_camera = self.x_center + self.deviation * np.cos(self.theta)
        self.y_camera = self.y_center + self.deviation * np.sin(self.theta)

    def PlotAll(self):
        plt.figure('trajectory')
        ax = plt.gca()
        ax.set_aspect(1)
        plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
                  0.15*np.sin(theta_start), color='r', width=0.03)
        plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                  0.15*np.sin(theta_goal), color='g', width=0.03)
        plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
        self.plot_vehicle()

    def collectPlot(self):
        plt.figure('AlphaStar-Rho')
        plt.plot(Rho, AlphaStar, 'g-')
        plt.xlabel("Rho")
        plt.ylabel("AlphaStar(degree)")
        plt.xlim(-0.2, 2.7)
        plt.ylim(-60, 60)
        # plt.savefig("./Output_curve/V-Rho.png")

        # select the initial states whose AlphaStar is within alphaBar
        
        Abs_AlphaStar = [abs(i) for i in AlphaStar]
        # print ('max(Abs_AlphaStarAlphaStar) =', max(Abs_AlphaStar))

        k_final = (AlphaStar[-1]- AlphaStar[-2]) / (Rho[-1] - Rho[-2])
        if AlphaStar[-1] > 0:
            judge = (k_final >=0 and k_final < 150)
        elif AlphaStar[-1] < 0:
            judge = (k_final <=0 and k_final > -150)
        else:
            judge = (k_final <150 and k_final > -150)
        # print (judge)

        if max(Abs_AlphaStar) < 40 and judge:
            Left_StartPoint.append([x_start,y_start,theta_start])
            plt.figure('Left_initialState')
            # plt.figure('trajectory')
            ax = plt.gca()
            ax.set_aspect(1)
            plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
                      0.15*np.sin(theta_start), color='r', width=0.03)
            plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                      0.15*np.sin(theta_goal), color='g', width=0.03)
            plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
            plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
            plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
            plt.xlim(-2, 2)
            plt.ylim(-2.5, 1)   

            plt.figure('Left_AlphaStar-Rho')
            plt.plot(Rho, AlphaStar, 'g-')
            plt.xlabel("Rho")
            plt.ylabel("AlphaStar(degree)")
            plt.xlim(-0.2, 2.7)
            plt.ylim(-60, 60)

            plt.figure('Left_trajectory')
            ax = plt.gca()
            ax.set_aspect(1)
            plt.arrow(x_start, y_start, 0.15*np.cos(theta_start),
                      0.15*np.sin(theta_start), color='r', width=0.03)
            plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
                      0.15*np.sin(theta_goal), color='g', width=0.03)
            plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
            self.plot_vehicle()

        else:
            Delete_StartPoint.append([x_start,y_start,theta_start])

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

        while (self.rho > 0 or abs(self.alpha-self.beta) > 0) and count < 2000:
            count += 1

            self.SpeedToGo()

            self.CurrentPosition()
            self.distance()
            self.Angle()
            self.AngleDot()
            self.trajCollect()

        # if count >= 2000:
        #     print("timeout")

        self.collectPlot()
        self.plot_vehicle()

    def plot_vehicle(self):  # pragma: no cover
        # Corners of triangular vehicle when pointing to the right (0 radians)
        # p1_i = np.array([0.15, 0, 1]).T
        # p2_i = np.array([-0.15, 0.075, 1]).T
        # p3_i = np.array([-0.15, -0.075, 1]).T

        # T = self.transformation_matrix()
        # p1 = np.matmul(T, p1_i)
        # p2 = np.matmul(T, p2_i)
        # p3 = np.matmul(T, p3_i)

        # plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
        # plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'k-')
        # plt.plot([p3[0], p1[0]], [p3[1], p1[1]], 'k-')

        # X_center_traj.append(x_center_traj)
        # Y_center_traj.append(y_center_traj)
        center_traj.append(x_center_traj)
        center_traj.append(y_center_traj)
        center_traj.append('b--')
        # plt.plot(x_center_traj, y_center_traj, 'b--')  


    def transformation_matrix(self):
        return np.array([
            [np.cos(self.theta), -np.sin(self.theta), self.x_center],
            [np.sin(self.theta), np.cos(self.theta), self.y_center],
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
Chair = (0, 0, np.pi/2) # this is the location of attractor
x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(Chair)
StartPoint = []
requireMinDistance = 1.5
alpha_bar = 40

Kp_rho = 0.15 # depends on the real Qolo's speed
Kp_alpha = 0.6 # 15
Kp_beta = round((Kp_rho - Kp_alpha)**2 / (4 * Kp_rho * np.sin(alpha_bar*np.pi/180)**2), 2) # depends on the linearization result
print(Kp_rho, Kp_alpha, Kp_beta)

# generate all possiable initial states
samRho = 2 # sampling number/step of rho
samAlpha = 4 # sampling number/step of alpha
samPhi = 4 # sampling number/step of phi
Rhoo = []
Alphaa = []
Phii = []
rhoo = np.linspace(0, 2.5, samRho)
alphaa = np.linspace(-np.pi/2, np.pi/2, samAlpha)
phii = np.linspace(-np.pi/2, np.pi/2, samPhi)
[Rhoo,Alphaa,Phii] = np.meshgrid(rhoo,alphaa,phii)
Rhoo = Rhoo.flatten() # reshape 2D array to 1D array
Alphaa = Alphaa.flatten()
Phii = Phii.flatten()

Rhoo,Alphaa,Phii = IntPoint.load_initializePoint(0,1,2)

# tranform (rho, alpha, phi) into (x,y,theta)
for i in range(len(Rhoo)):
    startPoint_x = - Rhoo[i] * np.sin(Phii[i])
    startPoint_y = - Rhoo[i] * np.cos(Phii[i])
    feasiblePosture = np.pi/2 - Alphaa[i] - Phii[i]
    startPoint = (startPoint_x, startPoint_y, feasiblePosture)
    StartPoint.append(startPoint)


# lambda function，filter the points we want to observe
# StartPoint = filter(lambda new_point: (new_point[0]<-0.2 or new_point[0]>0.2 ) and (new_point[1] > 0) and (new_point[2] == np.pi/2), StartPoint) 
# StartPoint = filter(lambda new_point: (new_point[1] > -1) , StartPoint) 
# StartPoint = [(-0.3, 0.5, 85* np.pi / 180)]

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

    PlotAll()


plt.show()



