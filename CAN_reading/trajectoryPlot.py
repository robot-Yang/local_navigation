# -*- coding: utf-8 -*-
import os
import re
from matplotlib import pyplot as plt
import csv
import numpy as np
import matplotlib

matplotlib.rcParams['font.family'] = 'Times New Roman'

com_R_speed = []
com_L_speed = []
Reci_R_speed = []
Reci_L_speed = []
Real_R_speed = []
Real_L_speed = []

myResList0 = []
myResList1 = []
myResList2 = []

com_time = []
Right_time = []
Left_time = []

Linear = []
Angular = []

# find lines which including needed value
def RegEx():
    myFile = './Torso_Control_experiment/shindo3/shindo1.txt'
    # myFile = './Torso_Control_experiment/shindo3/shindo2.txt'
    myFile = './Torso_Control_experiment/shindo3/shindo4.txt'
    myFile = './Torso_Control_experiment/shindo3/shindo6.txt'
    
    myFile = './Torso_Control_experiment/Li/Li1.txt'
    myFile = './Torso_Control_experiment/Li/Li2.txt'
    myFile = './Torso_Control_experiment/Li/Li4.txt'
    myFile = './Torso_Control_experiment/Li/Li6.txt'

    myFile = './Torso_Control_experiment/Luis2/luis_torso_ni.txt'
    myFile = './Torso_Control_experiment/Luis2/luis_torso_shun.txt'
    myFile = './Torso_Control_experiment/Luis2/luis_joystick_ni.txt'
    myFile = './Torso_Control_experiment/Luis2/luis_joystick_shun.txt'

    myFile = './Torso_Control_experiment/Yuki/yuki1.txt'
    myFile = './Torso_Control_experiment/Yuki/yuki2.txt'
    myFile = './Torso_Control_experiment/Yuki/yuki3.txt'
    myFile = './Torso_Control_experiment/Yuki/yuki4.txt'

    myFile = './Torso_Control_experiment/KAN/1.txt'
    # myFile = './Torso_Control_experiment/KAN/2.txt'
    # myFile = './Torso_Control_experiment/KAN/3.txt'
    # myFile = './Torso_Control_experiment/KAN/4.txt'

    myFile = './Torso_Control_experiment/Bruno2/bruno_joystick_ni.txt'
    myFile = './Torso_Control_experiment/Bruno2/bruno_torso_ni.txt'
    # myFile = './Torso_Control_experiment/Bruno2/bruno_joystick_shun.txt'
    # myFile = './Torso_Control_experiment/Bruno2/bruno_torso_shun.txt'

    myFile = './Torso_Control_experiment/CHUN/1.txt'
    myFile = './Torso_Control_experiment/CHUN/2.txt'
    # myFile = './Torso_Control_experiment/CHUN/3.txt'
    # myFile = './Torso_Control_experiment/CHUN/4.txt'

    # myFile = './Torso_Control_experiment/Ichikawa/Ichikawa_shun.txt'
    # myFile = './Torso_Control_experiment/Ichikawa/Ichikawa_ni.txt'
    # myFile = './Torso_Control_experiment/Ichikawa/Ichikawa_shun_joystick.txt'
    # myFile = './Torso_Control_experiment/Ichikawa/Ichikawa_ni_joystick.txt'

    openFile = open(myFile, 'r')
    myList = openFile.readlines()
    myReg0 = re.compile(r'1FF11011')
    myReg1 = re.compile(r'1FF12021') # right wheel
    myReg2 = re.compile(r'1FF12022') # left wheel
    for i in (myList):
        result0 = myReg0.search(i)
        result1 = myReg1.search(i)
        result2 = myReg2.search(i)
        if result0 != None:
                myResList0.append(i.rstrip())
        elif result1 != None:
                myResList1.append(i.rstrip())
        elif result2 != None:
                myResList2.append(i.rstrip())

# seperate the value out from the line
def plot_vel():    
    obj = '#'
    for k in myResList0:
        Loca = k.index(obj)
        speed0 = k[Loca+1:Loca+5]
        speed1 = k[Loca+5:Loca+9]
        speed0 = int(speed0, 16) / 152.4
        speed1 = int(speed1, 16) / 152.4
        if (speed0 >= 300):
            speed0 = - int('0xFFFF', 16) / 152.4 + speed0
        if (speed1 >= 300):
            speed1 = - int('0xFFFF', 16) / 152.4 + speed1
        com_R_speed.append(round(speed0, 2))
        com_L_speed.append(round(speed1, 2))
    print('myResList0 finish')
    for k in myResList1:
        Loca = k.index(obj)
        speed0 = k[Loca+1:Loca+5]
        speed1 = k[Loca+5:Loca+9]
        speed0 = int(speed0, 16) / 152.4
        speed1 = int(speed1, 16) / 152.4
        if (speed0 >= 300):
            speed0 = - int('0xFFFF', 16) / 152.4 + speed0
        if (speed1 >= 300):
            speed1 = - int('0xFFFF', 16) / 152.4 + speed1
        Reci_R_speed.append(round(speed0, 2))
        Real_R_speed.append(round(speed1, 2))
    print('myResList1 finish')
    for k in myResList2:
        Loca = k.index(obj)
        speed0 = k[Loca+1:Loca+5]
        speed1 = k[Loca+5:Loca+9]
        speed0 = int(speed0, 16) / 152.4
        speed1 = int(speed1, 16) / 152.4
        if (speed0 >= 300):
            speed0 = - int('0xFFFF', 16) / 152.4 + speed0
        if (speed1 >= 300):
            speed1 = - int('0xFFFF', 16) / 152.4 + speed1
        Reci_L_speed.append(round(speed0, 2))
        Real_L_speed.append(round(speed1, 2))
    print('myResList2 finish')

RegEx()
plot_vel()

D = 0.566 #0.5588 # diameter of wheel: 22 inch
d = 0.58 # distance of two wheel

def plot_velocity(L, R):
    global Linear, Angular
    v_len = min(len(L), len(R))
    # linear and angular velocity of Qolo
    v = [(float(L[i]) + float(R[i])) / float(60) * (np.pi*D) / float(2) for i in range(v_len)] 
    w = [(- float(L[i]) + float(R[i])) / float(60) * (np.pi*D) / d for i in range(v_len)] 
    Linear = v
    Angular = w
    print(Linear[0:10])
    t = np.linspace(1, 0.0025*v_len, v_len)
    plt.subplot(2,1,1)
    plt.plot(t, v)
    # plt.xlabel('Time [s]',fontsize=15)
    plt.ylabel('Linear velocity [m/s]',fontsize=15)
    plt.tick_params(labelsize=15)
    plt.subplot(2,1,2)
    plt.plot(t, w)
    plt.xlabel('Time [s]',fontsize=15)
    plt.ylabel('Angular velocity [rad/s]',fontsize=15)
    plt.tick_params(labelsize=15)

def plot_traj(L, R):
    v_len = min(len(L), len(R))
    # linear and angular velocity of Qolo
    v = [(float(L[i]) + float(R[i])) / float(60) * (np.pi*D) / float(2) for i in range(v_len)] 
    w = [(- float(L[i]) + float(R[i])) / float(60) * (np.pi*D) / d for i in range(v_len)] 

    # put trajectory point into list and plot
    W = np.pi/2 # starting point angle
    posture = []
    position_x = 0 # starting point x
    position_y = 0 # starting point y
    traj_x = [position_x]
    traj_y = [position_y]
    for i in range(v_len):
      W = W + w[i] * 0.0025
      position_x = position_x + v[i] * 0.0025 * np.cos(W)
      position_y = position_y + v[i] * 0.0025 * np.sin(W)
      posture.append(W)
      traj_x.append(position_x)
      traj_y.append(position_y)
    plt.plot(traj_x, traj_y)
    plt.axis("equal")
    plt.xlabel('X axis [m]',fontsize=15)
    plt.ylabel('Y axis [m]',fontsize=15)
    plt.legend(prop={'size': 15})
    plt.tick_params(labelsize=15)

Acc = []
AccDot = []
Theta2Dot = []
Theta3Dot = []
J = []

def jerk():
    # print(len(Linear))
    for i in range(1, len(Linear)):
        acc = (Linear[i] - Linear[i-1]) / 0.0025
        Acc.append(acc)
    for i in range(1, len(Acc)):
        accDot = (Acc[i] - Acc[i-1]) / 0.0025
        AccDot.append(accDot)

    for i in range(1, len(Angular)):
        theta2Dot = (Angular[i] - Angular[i-1]) / 0.0025
        Theta2Dot.append(theta2Dot)
    for i in range(1, len(Theta2Dot)):
        theta3Dot = (Theta2Dot[i] - Theta2Dot[i-1]) / 0.0025
        Theta3Dot.append(theta3Dot)
    print(len(AccDot), len(Theta3Dot))
    for i in range(1, len(AccDot)):
        j = abs(AccDot[i]) + abs(Theta3Dot[i]) * 0.0025
        J.append(j)
    JerkValue = sum(J) / (len(Theta3Dot) * 0.0025)
    print('len Je =', len(J))
    print('jerkvalue =', JerkValue)
    print("%e" % JerkValue)

    # plt.figure('Acc')
    # plt.subplot(2,1,1)
    # plt.plot(Acc)
    # plt.xlabel('time(s)')
    # plt.ylabel('linear accelaration')
    # plt.subplot(2,1,2)
    # plt.plot(Theta2Dot)
    # plt.xlabel('time(s)')
    # plt.ylabel('angular accelaration')

    # plt.figure('AccDot')
    # plt.subplot(2,1,1)
    # plt.plot(AccDot)
    # plt.xlabel('time(s)')
    # plt.ylabel('linear accelaration dot')
    # plt.subplot(2,1,2)
    # plt.plot(Theta3Dot)
    # plt.xlabel('time(s)')
    # plt.ylabel('angular accelaration dot')


# plt.figure(0)
# plot_traj(com_L_speed, com_R_speed)
# plt.figure(1)
# plot_traj(Reci_L_speed, Real_R_speed)
plt.figure('trajectory')
plot_traj(Real_L_speed, Real_R_speed)
plt.figure('Real_velocity')
plot_velocity(Real_L_speed, Real_R_speed)

jerk()
plt.show()