

import matplotlib.pyplot as plt
import numpy as np
from random import random

x_traj, y_traj = [], []

V = []
W = []
A_V = []
A_W = []
FOV = []
C_FOV =[]
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
# K4 = 5.87
# K = [3.37, 1.47]
K4 = 6.73
K = [4.88,2.24]
Kp_alpha = K[0] #15
Kp_beta = K[1] #2   # 3 is better than 5 or 10 or 15
dt = 0.1
chair_width = 0.5
chair_length = 0.5
safe_distance = 0.35 # distanc between destination and chair's front edge
x_start = 0.0
y_start = 0.0
theta_start = np.pi/2

original = 0
sequence = 3
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
    # max_index0 = FOV.index(max(FOV))
    # X_fov = x_traj[max_index0]
    # Y_fov = y_traj[max_index0]
    min_index1 = C_FOV.index(min(C_FOV))
    C_X_fov = x_traj[min_index1]
    C_Y_fov = y_traj[min_index1]
    max_index2 = L_FOV.index(max(L_FOV))
    L_X_fov = x_traj[max_index2]
    L_Y_fov = y_traj[max_index2]
    max_index3 = R_FOV.index(max(R_FOV))
    R_X_fov = x_traj[max_index3]
    R_Y_fov = y_traj[max_index3]

    # plt.scatter(C_X_fov, C_Y_fov, s=50, c='r', marker="o")
    plt.scatter(L_X_fov, L_Y_fov, s=50, c='r', marker="x")
    plt.scatter(R_X_fov, R_Y_fov, s=50, c='b', marker="x")

    # print("min C_FOV =", min(C_FOV) * 180 / np.pi, "position =", C_X_fov, C_Y_fov)
    print("max L_FOV =", max(L_FOV) * 180 / np.pi, "position =", L_X_fov, L_Y_fov)
    print("max R_FOV =", max(R_FOV) * 180 / np.pi, "position =", R_X_fov, R_Y_fov)
    print ("final_FOV_diff =", C_FOV[-1] * 180 / np.pi)

    # show velocity/aceelaration of linear and angular
    # plt.figure()
    # plt.subplot(2,1,1)
    # plt.plot(V, 'r-')
    # plt.plot(W, 'b-')
    # plt.subplot(2,1,2)
    # plt.plot(A_V, 'r-')
    # plt.plot(A_W, 'b-')

class chen():
    def __init__(self):
        # simulation parameters
        self.v0 = 0
        self.w0 = 0
        self.v = 0
        self.w = 0
        self.x = 0
        self.y = 0

        self.dest_X = 0
        self.dest_Y = 0

        self.L_fov = 0
        self.R_fov = 0

        self.AngleCenter = 0


    def setDestination(self):
        self.dest_X = x_goal
        self.dest_Y = y_goal

    def distance(self):
        self.x_diff = self.dest_X - self.x
        self.y_diff = self.dest_Y - self.y
        self.rho = np.sqrt(self.x_diff**2 + self.y_diff**2)

    # show the trajectory of qolo 
    def trajPlot(self):
        x_traj.append(self.x)
        y_traj.append(self.y)

    # detecting the angle of alpha and beta
    def Angle(self):
        self.alpha = (np.arctan2(self.y_diff, self.x_diff) - self.theta + np.pi) % (2 * np.pi) - np.pi
        self.beta = (np.arctan2(self.y_diff, self.x_diff) - theta_goal + np.pi) % (2 * np.pi) - np.pi
        # self.beta = (self.theta - theta_goal + np.pi) % (2 * np.pi) - np.pi
        # self.beta = (self.theta - self.AngleCenter + np.pi) % (2 * np.pi) - np.pi

    def SpeedToGo(self):
        self.v0 = self.v
        self.w0 = self.w

        # if self.rho < 0.05:
        #     self.v = 0.03
        #     self.w = 0
        # else:
        # self.v =  Kp_rho * self.rho - K4 * self.rho * np.sin((180 - abs(self.L_fov)-abs(self.R_fov)) * np.pi/180)
        self.v =  Kp_rho * self.rho
        # self.w = K4 * self.rho * (Kp_alpha * self.alpha + Kp_beta * self.beta)  # positive value means turn left, negative value means turn right
        # self.w = Kp_alpha * self.alpha + Kp_beta * self.beta - K4 * ((self.theta - self.AngleCenter + np.pi) % (2 * np.pi) - np.pi)
        # self.w = - Kp_beta * self.beta
        # self.w = Kp_beta * (Kp_alpha * self.alpha + self.beta) * self.rho
        self.w = (Kp_alpha * self.alpha + Kp_beta * self.beta) * self.rho
        if self.alpha > np.pi / 2 or self.alpha < -np.pi / 2:
            self.v = - self.v

        # constrians linear/angular velocity
        if self.v > v_threshold:
            self.v = v_threshold
        elif self.v < - v_threshold:
            self.v = - v_threshold
        if self.w > w_threshold:
            self.w = w_threshold
        elif self.w < - w_threshold:
            self.w = - w_threshold

        # constrains of linear/angular acceleration
        if self.v - self.v0 > a_v_threshold:
            self.v = self.v0 + a_v_threshold
        elif self.v - self.v0 < - a_v_threshold:
            self.v = self.v0 - a_v_threshold
        if self.w - self.w0 > a_w_threshold:
            self.w = self.w0 + a_w_threshold
        elif self.w - self.w0 < - a_w_threshold:
            self.w = self.w0 - a_w_threshold

    def CurrentPosition(self):
        self.theta = self.theta + self.w * dt
        self.x = self.x + self.v * np.cos(self.theta) * dt
        self.y = self.y + self.v * np.sin(self.theta) * dt

    def PlotAll(self):
        if show_animation:  # pragma: no cover
            plt.cla()
            plt.arrow(x_start, y_start, 0.35*np.cos(theta_start),
                      0.35*np.sin(theta_start), color='r', width=0.075)
            plt.arrow(x_goal, y_goal, 0.35*np.cos(theta_goal),
                      0.35*np.sin(theta_goal), color='g', width=0.075)
            rect0 = plt.Rectangle((F_x_chair, F_y_chair), chair_length, chair_width/2, angle = theta_goal * 180 / np.pi, fill=False, edgecolor = 'red',linewidth=1)
            ax.add_patch(rect0)
            rect1 = plt.Rectangle((R_x_chair, R_y_chair), chair_length, chair_width/2, angle = theta_goal * 180 / np.pi, fill=False, edgecolor = 'red',linewidth=1)
            ax.add_patch(rect1)
            # plt.scatter(F_x_chair, F_y_chair, s=50, c='r', marker="x")
            # plt.scatter(L_x_chair, L_y_chair, s=50, c='r', marker="x")
            # plt.scatter(R_x_chair, R_y_chair, s=50, c='r', marker="x")
            self.plot_vehicle()
            #plt.scatter(0,4, c='r', marker="o")

    def collect(self, L_x_chair, L_y_chair, R_x_chair, R_y_chair):
        L_x_diff = L_x_chair - self.x
        L_y_diff = L_y_chair - self.y
        # L_fov = (np.arctan2(L_x_diff, L_y_diff) - theta + np.pi) % (2 * np.pi) - np.pi
        L_line = np.arctan2(L_y_diff, L_x_diff)
        self.L_fov = np.arctan2(L_y_diff, L_x_diff) - self.theta
        R_x_diff = R_x_chair - self.x
        R_y_diff = R_y_chair - self.y
        # R_fov = (np.arctan2(R_x_diff, R_y_diff) - theta + np.pi) % (2 * np.pi) - np.pi
        R_line = np.arctan2(R_y_diff, R_x_diff)
        self.R_fov = np.arctan2(R_y_diff, R_x_diff) - self.theta
        self.AngleCenter = (np.arctan2(R_y_diff, R_x_diff) + np.arctan2(L_y_diff, L_x_diff)) / 2
        # FOV.append(abs(self.alpha))  #field of view
        C_FOV.append(abs(self.theta - theta_goal))
        L_FOV.append(abs(self.L_fov))
        R_FOV.append(abs(self.R_fov))

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair):
        self.x = x_start
        self.y = y_start
        self.theta = theta_start

        self.setDestination()
        self.distance()
        self.collect(L_x_chair, L_y_chair, R_x_chair, R_y_chair)
        self.trajPlot()

        count = 0

        while (self.rho > 0.01) and count < 100:
            count += 1
            # print("count =", count)

            self.Angle()
            self.SpeedToGo()

            # filter
            read_update(self.v, self.w)
            self.v, self.w = move_average()

            # for monitoring v, w a_v, a_w
            V.append(self.v)
            W.append(self.w)
            a_v = self.v - self.v0
            a_w = self.w - self.w0
            A_V.append(a_v)
            A_W.append(a_w)
            # print("v =", v, "w =", w)

            self.CurrentPosition()
            self.distance()
            self.collect(L_x_chair, L_y_chair, R_x_chair, R_y_chair)
            self.trajPlot()
            self.PlotAll()


        if count >= 100:
            print("timeout")

        # print ("x_traj, y_traj= ", x_traj, y_traj)
        collectPlot()
        plt.show()

    def plot_vehicle(self):  # pragma: no cover
        # Corners of triangular vehicle when pointing to the right (0 radians)
        p1_i = np.array([0.25, 0, 1]).T
        p2_i = np.array([-0.25, 0.125, 1]).T
        p3_i = np.array([-0.25, -0.125, 1]).T

        T = self.transformation_matrix()
        p1 = np.matmul(T, p1_i)
        p2 = np.matmul(T, p2_i)
        p3 = np.matmul(T, p3_i)

        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-')
        plt.plot([p2[0], p3[0]], [p2[1], p3[1]], 'k-')
        plt.plot([p3[0], p1[0]], [p3[1], p1[1]], 'k-')

        plt.plot(x_traj, y_traj, 'b--') 

        #plt.axis("equal")
        plt.xlim(-1, 3)
        plt.ylim(-1, 3)
        plt.pause(dt)

    def transformation_matrix(self):
        return np.array([
            [np.cos(self.theta), -np.sin(self.theta), self.x],
            [np.sin(self.theta), np.cos(self.theta), self.y],
            [0, 0, 1]
        ])

    def main(self): 
        self.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair)

a = chen()
Chair = [(-0.1, 1, np.pi/3)]
if __name__ == '__main__':
    for i in Chair:
        x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(i)
        # print ("FFF",x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y)
        a.main()
