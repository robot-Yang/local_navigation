"""

Move to specified pose

Author: Daniel Ingram (daniel-s-ingram)
        Atsushi Sakai(@Atsushi_twi)

P. I. Corke, "Robotics, Vision & Control", Springer 2017, ISBN 978-3-319-54413-7

"""

import matplotlib.pyplot as plt
import numpy as np
from random import random

x_traj, y_traj = [], []

V = []
W = []
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

Kp_rho = 0.3 # linear velocity

dt = 0.1 # frequency
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

class chen():
    def __init__(self):
        # simulation parameters
        self.K = [17.02, 3.51, 5]
        self.Kp_alpha = self.K[0] #15
        self.Kp_beta = self.K[1] #2   # 3 is better than 5 or 10 or 15
        self.K4 = self.K[2]

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

        self.L_FOV = []
        self.R_FOV = []

        self.x_traj = []
        self.y_traj = []

    # def __del__(self):
    #     print ('__del__')

    def setDestination(self):
        self.dest_X = x_goal
        self.dest_Y = y_goal

    def setDestination_close(self):
        self.dest_X = chair_back_x
        self.dest_Y = chair_back_y

    def distance(self):
        self.x_diff = self.dest_X - self.x
        self.y_diff = self.dest_Y - self.y
        back_x_diff = chair_back_x - self.x
        back_y_diff = chair_back_y - self.y
        self.rho = np.sqrt(back_x_diff**2 + back_y_diff**2)

    def trajPlot(self):
        self.x_traj.append(self.x)
        self.y_traj.append(self.y)

    def Angle(self):
        self.alpha = (np.arctan2(self.y_diff, self.x_diff) - self.theta + np.pi) % (2 * np.pi) - np.pi
        self.beta = (np.arctan2(self.y_diff, self.x_diff) - theta_goal + np.pi) % (2 * np.pi) - np.pi

    def SpeedToGo(self):
        self.v0 = self.v
        self.w0 = self.w

        if self.rho < 0.95:
            self.v = 0.03
        #     self.w = 0
        # elif self.rho < 1.1:
        #     self.setDestination_close()
        #     # self.v =  Kp_rho * self.rho - self.K4 * self.rho * np.sin((180 - abs(self.L_fov)-abs(self.R_fov)) * np.pi/180)
        #     self.v =  Kp_rho * self.rho
        #     # self.w = self.K4 * self.rho * (self.Kp_alpha * self.alpha + self.Kp_beta * self.beta)  # positive value means turn left, negative value means turn right
        #     self.w = self.Kp_alpha * self.alpha + self.Kp_beta * self.beta
        #     if self.alpha > np.pi / 2 or self.alpha < -np.pi / 2:
        #         self.v = - self.v
        else:
            # self.v =  Kp_rho * self.rho - self.K4 * self.rho * np.sin((180 - abs(self.L_fov)-abs(self.R_fov)) * np.pi/180)
            self.v =  Kp_rho * self.rho
            # self.w = self.K4 * self.rho * (self.Kp_alpha * self.alpha + self.Kp_beta * self.beta)  # positive value means turn left, negative value means turn right
            self.w = self.Kp_alpha * self.alpha + self.Kp_beta * self.beta
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
        # FOV.append(abs(self.alpha))  #field of view
        C_FOV.append(abs(self.theta - theta_goal))
        self.L_FOV.append(abs(self.L_fov))
        self.R_FOV.append(abs(self.R_fov))

    def move_to_pose(self, x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair):
        """
        rho is the distance between the robot and the goal position
        alpha is the angle to the goal relative to the heading of the robot
        beta is the angle between the robot's position and the goal position plus the goal angle

        Kp_rho*rho and Kp_alpha*alpha drive the robot along a line towards the goal
        Kp_beta*beta rotates the line so that it is parallel to the goal angle
        """
        self.x = x_start
        self.y = y_start
        self.theta = theta_start

        self.setDestination()
        self.distance()
        self.collect(L_x_chair, L_y_chair, R_x_chair, R_y_chair)
        self.trajPlot()

        count = 0

        while (self.rho > 0.78) and count < 100:
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
            # self.PlotAll()

        max_L = max(self.L_FOV)
        max_R = max(self.R_FOV)
        max_FOV = max(max_L, max_R)

        if count >= 100:
            return 90
        else:
            return max_FOV * 180 / np.pi


    def main(self, K_alpha, K_beta, K4):
        global A, B, original, sequence
        self.Kp_alpha = K_alpha
        self.Kp_beta = K_beta
        self.K4 = K4
        # print (self.v0, self.w0, self.v, self.w, self.x, self.y, self.L_FOV, self.R_FOV)
        # Chair = [(2, 5, np.pi/4)]
        # for i in Chair:
        #     x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(i)
        max_FOV = self.move_to_pose(x_start, y_start, theta_start, x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair)

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
        V = []
        W = []
        A_V = []
        A_W = []
        FOV = []
        C_FOV =[]
        A = [original] * sequence
        B = [original] * sequence
        self.L_FOV = []
        self.R_FOV = []
        self.x_traj, self.y_traj = [], []
        return max_FOV

a = chen()
Chair = [(-0.1, 1, np.pi/3)]
# if __name__ == '__main__':
for i in Chair:
    x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y = chair_info(i)
#         print ("FFF",x_goal, y_goal, theta_goal, L_x_chair, L_y_chair, R_x_chair, R_y_chair, F_x_chair, F_y_chair, chair_bottom_x, chair_bottom_y, chair_back_x, chair_back_y)
#         a.main()

