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
    myFile = './nishizhen.txt'
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

RegEx()
plot_vel()

D = 0.5588
d = 0.575
v_len = min(len(Real_L_speed), len(Real_R_speed))
# linear and angular velocity of Qolo
v = [(float(Real_L_speed[i]) + float(Real_R_speed[i])) / float(60) * (np.pi*D) / float(2) for i in range(v_len)] 
w = [(- float(Real_L_speed[i]) + float(Real_R_speed[i])) / float(60) * (np.pi*D) / d for i in range(v_len)] 

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
plt.show()
