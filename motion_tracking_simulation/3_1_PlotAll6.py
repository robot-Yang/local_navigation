# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-12-01 18:04:08

'''
Simulate all possible initial states, give constraint of a* and convergence, find the feasible space, save data into csv
For fitting the boundary
change the chair into a cube
'''

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import random
import csv

x_camera_traj, y_camera_traj = [], []
x_center_traj, y_center_traj = [], []
Rho = []
Alpha = []
Beta = []
AlphaStar = []
AlphaStar_LR = []
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


dt = 1.0/30
chair_width = 0.5
chair_length = 0.5
safe_distance = 0.45 # distance between attractor and chair's front edge

l = 0.26 # distance between camera and center of Qolo
d = 0.9 # distance between attractor (destination) and objective (center of chair)

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
Left_StartPoint = []
Delete_StartPoint = []

Left_initialX = []
Left_initialY = []
Left_initialPosture = []
Left_initialRho = []
Left_initialAlpha = []
Left_initialPhi = []
Left_maxAlphaStar = []
Left_Stable_flag = []

Delete_initialX = []
Delete_initialY = []
Delete_initialPosture = []
Delete_initialRho = []
Delete_initialAlpha = []
Delete_initialPhi = []
Delete_maxAlphaStar = []
Delete_Stable_flag = []

judge = 0

def chair_info(chair):
    x_goal = chair[0] # attractor
    y_goal = chair[1]
    theta_goal = chair[2]
    chair_bottom_x = x_goal + d * np.cos(theta_goal) # objective
    chair_bottom_y = y_goal + d * np.sin(theta_goal)
    F_x_chair = chair_bottom_x - chair_length/2 * np.cos(theta_goal)
    F_y_chair = chair_bottom_y - chair_length/2 * np.sin(theta_goal)
    F_L_x_chair = F_x_chair + chair_width / 2 * np.cos(theta_goal + np.pi/2)
    F_L_y_chair = F_y_chair + chair_width / 2 * np.sin(theta_goal + np.pi/2)
    F_R_x_chair = F_x_chair + chair_width / 2 * np.cos(theta_goal - np.pi/2)
    F_R_y_chair = F_y_chair + chair_width / 2 * np.sin(theta_goal - np.pi/2)
    B_x_chair = chair_bottom_x + chair_length/2 * np.cos(theta_goal)
    B_y_chair = chair_bottom_y + chair_length/2 * np.sin(theta_goal)
    B_L_x_chair = B_x_chair + chair_width / 2 * np.cos(theta_goal + np.pi/2)
    B_L_y_chair = B_y_chair + chair_width / 2 * np.sin(theta_goal + np.pi/2)
    B_R_x_chair = B_x_chair + chair_width / 2 * np.cos(theta_goal - np.pi/2)
    B_R_y_chair = B_y_chair + chair_width / 2 * np.sin(theta_goal - np.pi/2)
    chair_back_x = F_x_chair + chair_length * np.cos(theta_goal)
    chair_back_y = F_y_chair + chair_length  * np.sin(theta_goal)
    plt.plot([F_L_x_chair, F_R_x_chair], [F_L_y_chair, F_R_y_chair], 'k-')
    plt.plot([B_L_x_chair, B_R_x_chair], [B_L_y_chair, B_R_y_chair], 'k-')
    plt.plot([F_L_x_chair, B_L_x_chair], [F_L_y_chair, B_L_y_chair], 'k-')
    plt.plot([F_R_x_chair, B_R_x_chair], [F_R_y_chair, B_R_y_chair], 'k-')
    return x_goal, y_goal, theta_goal, F_L_x_chair, F_L_y_chair, F_R_x_chair, F_R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y


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

def plotPoints():
    #  plot in (x, y, theta) 2D space
    plt.figure('Left_initialState-2D')
    ax = plt.gca()
    ax.set_aspect(1)
    plt.quiver(Left_initialX, Left_initialY, np.cos(Left_initialPosture), np.sin(Left_initialPosture), scale =20)
    plt.arrow(x_goal, y_goal, 0.15*np.cos(theta_goal),
              0.15*np.sin(theta_goal), color='g', width=0.03)
    plt.scatter(chair_bottom_x, chair_bottom_y, s=50, c='r', marker="x")
    plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) # 
    plt.scatter(Left_initialX, Left_initialY, s=60, c='k', marker=".", zorder=30)
    plt.xlim(-2, 2)
    plt.ylim(-2.5, 1)

    #  plot in (rho, alpha, phi) 3D space
    fig = plt.figure('Left_initialState-3D')
    ax = Axes3D(fig)
    ax.scatter(Left_initialRho, Left_initialAlpha, Left_initialPhi, c='k', marker=".")
    ax.set_xlabel('rho')
    ax.set_ylabel('alpha')
    ax.set_zlabel('phi')
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=10)

def collectPoints():
    Abs_AlphaStar = [abs(i) for i in AlphaStar]
    global judge
    # judge = (a.rho < 0.01 and abs(a.alpha-a.beta) < 0.01)
    k_final = (AlphaStar[-1]- AlphaStar[-2]) / (Rho[-1] - Rho[-2])
    if AlphaStar[-1] > 0:
        judge = (k_final >=0 and k_final < 150)
    elif AlphaStar[-1] < 0:
        judge = (k_final <=0 and k_final > -150)
    else:
        judge = (k_final <150 and k_final > -150)
        
    if max(AlphaStar_LR) < alpha_bar and judge:
    # if max(Abs_AlphaStar) < 40 and judge:
        Left_initialX.append(x_start)
        Left_initialY.append(y_start)
        Left_initialPosture.append(theta_start)
        Left_initialRho.append(Rhoo[pointLocation])
        Left_initialAlpha.append(Alphaa[pointLocation])
        Left_initialPhi.append(Phii[pointLocation])
        Left_maxAlphaStar.append(max(Abs_AlphaStar))
        Left_Stable_flag.append(1)
    else:
        Delete_initialX.append(x_start)
        Delete_initialY.append(y_start)
        Delete_initialPosture.append(theta_start)
        Delete_initialRho.append(Rhoo[pointLocation])
        Delete_initialAlpha.append(Alphaa[pointLocation])
        Delete_initialPhi.append(Phii[pointLocation])
        Delete_maxAlphaStar.append(max(Abs_AlphaStar))
        Delete_Stable_flag.append (0)

def writeIntocsv():
    # saved format: [rho alpha phi alpha* Stable_flag]
    Left_all = [Left_initialRho,Left_initialAlpha,Left_initialPhi,Left_maxAlphaStar,Left_Stable_flag]
    Left_all = np.transpose(Left_all) 
    # np.savetxt("simulation_result.csv", Left_all, delimiter=",")
    Delete_all = [Delete_initialRho, Delete_initialAlpha, Delete_initialPhi, Delete_maxAlphaStar, Delete_Stable_flag]
    Delete_all = np.transpose(Delete_all)
    np.savetxt("simulation_result_ex.csv", np.r_[Left_all,Delete_all], delimiter=",")

    # saved format: 
    with open('simulation_result_ex.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(Left_initialRho)
        writer.writerow(Left_initialAlpha)
        writer.writerow(Left_initialPhi)
        writer.writerow(Left_maxAlphaStar)
        writer.writerow(Left_Stable_flag)
        writer.writerow(Delete_initialRho)
        writer.writerow(Delete_initialAlpha)
        writer.writerow(Delete_initialPhi)
        writer.writerow(Delete_maxAlphaStar)
        writer.writerow(Delete_Stable_flag)
    csvFile.close()

class DockingSim():
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

        # left alphaStar and right alphaStar
        y_diff_Fla = F_L_y_chair - y_a
        x_diff_Fla = F_L_x_chair - x_a
        # print(F_L_y_chair, F_L_x_chair, y_a, x_a)
        self.alphaStar_l = np.arctan2(y_diff_Fla, x_diff_Fla) - theta_a
        # print(np.arctan2(self.y_diff, self.x_diff), self.theta)
        y_diff_Fra = F_R_y_chair - y_a
        x_diff_Fra = F_R_x_chair - x_a
        self.alphaStar_r = np.arctan2(y_diff_Fra, x_diff_Fra) - theta_a
        self.alphaStar_lr = max(abs(self.alphaStar_l), abs(self.alphaStar_r))
        # print(self.alphaStar_l, self.alphaStar_r)

        Alpha.append(self.alpha*180/np.pi)
        Beta.append(self.beta*180/np.pi)
        AlphaStar.append(self.alphaStar*180/np.pi)
        AlphaStar_LR.append(self.alphaStar_lr*180/np.pi)
        # print(len(AlphaStar), len(AlphaStar_LR))

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

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal, F_L_x_chair, F_L_y_chair, F_R_x_chair, F_R_y_chair, F_x_chair, F_y_chair):
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

        while (self.rho > 0 or abs(self.alpha-self.beta) > 0) and count < 1000:
            count += 1

            self.SpeedToGo()

            # filter
            # read_update(self.v, self.w)
            # self.v, self.w = move_average()

            # for monitoring v, w a_v, a_w
            # V.append(self.v)
            # W.append(self.w)

            self.CurrentPosition()
            self.distance()
            self.Angle()
            self.AngleDot()
            self.trajCollect()

        # if count >= 2000:
        #     print("timeout")
             
        # self.collectPlot()
        # self.PlotAll()
        collectPoints()

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

        plt.xlim(-2, 2)
        plt.ylim(-2.5, 1)


    def transformation_matrix(self):
        return np.array([
            [np.cos(self.theta), -np.sin(self.theta), self.x_center],
            [np.sin(self.theta), np.cos(self.theta), self.y_center],
            [0, 0, 1]
        ])

    def main(self): 
        self.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal, F_L_x_chair, F_L_y_chair, F_R_x_chair, F_R_y_chair, F_x_chair, F_y_chair)

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


a = DockingSim()
Chair = (0, 0, np.pi/2) # this is the location of attractor
x_goal, y_goal, theta_goal, F_L_x_chair, F_L_y_chair, F_R_x_chair, F_R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(Chair)
StartPoint = []
alpha_bar = 40

Kp_rho = 0.15 # depends on the real Qolo's speed
Kp_alpha = 0.6 # 15
Kp_beta = round((Kp_rho - Kp_alpha)**2 / (4 * Kp_rho * np.sin(alpha_bar*np.pi/180)**2), 2) # depends on the linearization result
print(Kp_rho, Kp_alpha, Kp_beta)

# generate all possiable initial states
samRho = 3 # sampling number/step of rho
samAlpha = 7 # sampling number/step of alpha
samPhi = 9 # sampling number/step of phi
Rhoo = []
Alphaa = []
Phii = []
rhoo = np.linspace(0.2, 1.0, samRho)
alphaa = np.linspace(-np.pi/3, np.pi/3, samAlpha)
phii = np.linspace(-np.pi/3, np.pi/3, samPhi)
[Rhoo,Alphaa,Phii] = np.meshgrid(rhoo,alphaa,phii)
Rhoo = Rhoo.flatten() # reshape 2D array to 1D array
Alphaa = Alphaa.flatten()
Phii = Phii.flatten()

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

pointLocation = -1
five_percent = len(Rhoo)*0.05 #int()
print('total_points = ', len(Rhoo))
if __name__ == '__main__':
    # percentage = 0
    for i in StartPoint:
        pointLocation += 1
        
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
        AlphaStar_LR = []
        AlphaDot = [0]
        BetaDot = [0]
        V = [0]
        W = [0]
        if (pointLocation+1)%five_percent == 0:
            print ('finish', (pointLocation+1)//five_percent*5, 'percentage')

    plotPoints()
    writeIntocsv()

plt.show()



