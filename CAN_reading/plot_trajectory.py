# -*- coding: utf-8 -*-


import os
import re
from matplotlib import pyplot as plt
import csv
import numpy as np
# myFile = './some.txt'
# openFile = open(myFile, 'r')

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

# find lines which including needed value
def RegEx():
    # myFile = './nishizhen.txt'
    myFile = './Raspberry_code/control_law/3trail.txt'
    openFile = open(myFile, 'r')
#     myResList0 = []
#     myResList1 = []
#     myResList2 = []
    myList = openFile.readlines()
    myReg0 = re.compile(r'1FF11011')
    myReg1 = re.compile(r'1FF12021') # right wheel
    myReg2 = re.compile(r'1FF12022') # left wheel
    for i in (myList):
        #print(i, end='')
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

# seperate the time from the line(actually not used here)
def plot_traj():
    for k in myResList0:
        time0 = k[1:17]
        com_time.append(time0)
    print('com_time finish')
    for k in myResList1:
        time1 = k[1:17]
        Right_time.append(time1)
    print('Reci_time finish')
    for k in myResList2:
        time2 = k[1:17]
        Left_time.append(time2)
    print('Real_time finish')


RegEx()
plot_vel()
plot_traj()

com_time0 = com_time[:-1]
com_time1 = com_time[1:]
com_time2 = [float(com_time1[i]) - float(com_time0[i]) for i in range(len(com_time0))]

Right_time0 = Right_time[:-1]
Right_time1 = Right_time[1:]
Right_time2 = [float(Right_time1[i]) - float(Right_time0[i]) for i in range(len(Right_time0))]

Left_time0 = Left_time[:-1]
Left_time1 = Left_time[1:]
Left_time2 = [float(Left_time1[i]) - float(Left_time0[i]) for i in range(len(Left_time0))]

R_step = [float(Right_time2[i]) * float(Real_R_speed[i]) for i in range(len(Right_time2))]
L_step = [float(Left_time2[i]) * float(Real_L_speed[i]) for i in range(len(Left_time2))]

print(len(R_step))
print(len(L_step))
print(len(Real_R_speed))
print(len(Real_L_speed))
print(sum(Right_time2)/len(Right_time2))
print(sum(Left_time2)/len(Left_time2))

D = 0.5588
d = 0.575
v_len = min(len(Real_L_speed), len(Real_R_speed))
v = [(float(Real_L_speed[i]) + float(Real_R_speed[i])) / float(60) * (np.pi*D) / float(2) for i in range(v_len)] 
w = [(- float(Real_L_speed[i]) + float(Real_R_speed[i])) / float(60) * (np.pi*D) / d for i in range(v_len)] 
# v = (L + R)/60*(pi*D)/2
# w = (L - R)/60*(pi*D)/d * 180/pi

W = np.pi/2
posture = []
position_x = 0
position_y = 0
traj_x = [position_x]
traj_y = [position_y]
for i in range(v_len):
  W = W + w[i] * 0.0025
  position_x = position_x - v[i] * 0.0025 * np.cos(W)
  position_y = position_y - v[i] * 0.0025 * np.sin(W)
  posture.append(W)
  traj_x.append(position_x)
  traj_y.append(position_y)
  # print(position_x)

# print(traj_x)
# print(round(posture,2))

plt.plot(traj_x, traj_y)
# plt.xlim(-0.1, 1)
# plt.ylim(0, 2)
plt.axis("equal")













# RegEx()
# plot_vel()

# plt.subplot(2,1,1)
# plt.plot(com_R_speed[0:20000], 'b')
# plt.plot(Reci_R_speed[0:20000], 'y')
# plt.plot(Real_R_speed[0:20000], 'r')
# plt.subplot(2,1,2)
# plt.plot(com_L_speed[0:20000], 'b')
# plt.plot(Reci_L_speed[0:20000], 'y')
# plt.plot(Real_L_speed[0:20000], 'r')
plt.show()
