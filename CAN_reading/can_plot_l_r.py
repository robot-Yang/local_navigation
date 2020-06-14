# import os

# location = './'
# for filename in os.listdir(location):
#     if filename == 'some.log':
#        f  = open(os.path.join(location, 'some.log'), "r")
       # print (f.read())

#!/usr/bin/python

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
Real_L_speed0 =[]
Real_R_speed1 =[]

D = 0.5588
d = 0.55 # 0.575

# plot real velocity
Command_L = 300 # 1350
Command_R = 300 # 1350 # 1700

Command_LEFT = []
Command_RIGHT = []
Velocity_LEFT = []
Velocity_RIGHT = []

def RegEx():
    # ANALOG
    # myFile = './Raspberry_code/0.3-1_1907-1907.txt'
    # myFile = './Raspberry_code/0-1_1886-1413.txt'
    # myFile = './Raspberry_code/0--1_1886-1413.txt'
    # myFile = './Raspberry_code/1-0_2509-2509.txt'
    # myFile = './Raspberry_code/-1-0_790-790.txt'
    # myFile = './Raspberry_code/test.txt' 
    # myFile = './Raspberry_code/ANALOG/1-0_2509-2509-plus0.02.txt' -1-0_856-856.txt 

    # ANALOG+0.02
    # myFile = './Raspberry_code/ANALOG+0.02/1-0_2509-2509.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/-1-0_856-856.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/0-1_1479-1952.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/0--1_1952-1497.txt' 

    # ANALOG+0.02+MaxSpeed
    # myFile = './Raspberry_code/ANALOG+0.02+MaxSpeed/0--1_2174-1263.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02+MaxSpeed/0--1_1981_1457.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/-1-0_856-856.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/0-1_1479-1952.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/0--1_1952-1497.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02+MaxSpeed/1-0_2678-2659.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02+MaxSpeed/-0.3-0_1470-1479.txt' 
    
    # control_law 
    # myFile = './Raspberry_code/control_law/4trail.txt' 

    myFile = './bothwheel-300to3000-threshold-0.5-200.txt' 

    # ANALOG+0.0203
    # myFile = './Raspberry_code/ANALOG+0.02/1-0_2509-2509.txt' v
    # myFile = './Raspberry_code/ANALOG+0.02/-1-0_856-856.txt' 
    # myFile = './Raspberry_code/ANALOG+0.02/0-1_1479-1952.txt' 0--1_1955-1480
    # myFile = './Raspberry_code/ANALOG+0.0203/0--1_1955-1480.txt' 

    # ANALOG-20-01-02
    # myFile = './Raspberry_code/ANALOG-20-01-02/1-0_2509-2509-5052.txt'

    openFile = open(myFile, 'r')
    myResList0 = []
    myResList1 = []
    myResList2 = []
    myList = openFile.readlines()
    myReg0 = re.compile(r'1FF11011')
    myReg1 = re.compile(r'1FF12021')
    myReg2 = re.compile(r'1FF12022')
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

def plot_all():
    global Real_L_speed0
    global Real_R_speed0
    plt.figure('left-right')
    plt.subplot(2,1,1)
    # plt.plot(com_L_speed, 'b')
    # plt.plot(Reci_L_speed, 'g')
    Real_L_speed0 = [(i)/60*(np.pi*D) for i in Real_L_speed]
    plt.plot(Real_L_speed0, 'r')
    plt.subplot(2,1,2)
    # plt.plot(com_R_speed, 'b')
    # plt.plot(Reci_R_speed, 'g')
    Real_R_speed0 = [(i)/60*(np.pi*D) for i in Real_R_speed]
    plt.plot(Real_R_speed0, 'r')

def plot_separated():
    global Real_L_speed0
    global Real_R_speed0
    global Command_L
    global Command_R
    start_point = 600  # start point to count
    step = int(3.0/0.0025)
    space = int(step*3/4.0)
    print('step =', step)
    print('space =', space)

    plt.figure('left-right-separated')
    plt.subplot(2,1,1)
    LENGTH = len(Real_L_speed0)
    Location = start_point
    while  Location < (LENGTH-step):
        Interval = np.linspace(Location, Location+space, space)
        plt.plot(Interval, Real_L_speed0[Location:Location+space], 'r')
        Location += step 
        velocity = np.mean(Real_L_speed0[Location:Location+space])
        print('Command_L =', Command_L, 'left velocy =', velocity)
        Command_LEFT.append(Command_L)
        Velocity_LEFT.append(velocity)
        Command_L += 10
        
    plt.subplot(2,1,2)
    LENGTH = len(Real_R_speed0)
    Location = start_point
    while  Location < (LENGTH-step):
        Interval = np.linspace(Location, Location+space, space)
        plt.plot(Interval, Real_R_speed0[Location:Location+space], 'r')
        Location += step 
        velocity = np.mean(Real_R_speed0[Location:Location+space])
        print('Command_R =', Command_R, 'right velocy =', velocity)
        Command_RIGHT.append(Command_R)
        Velocity_RIGHT.append(velocity)
        Command_R += 10
        

def writeIntocsv():
    New_list = []
    LENGTH = min(len(Command_LEFT), len(Command_RIGHT))
    i = 0
    while i < LENGTH:
        New_list.append([Command_LEFT[i],Velocity_LEFT[i], Command_RIGHT[i], Velocity_RIGHT[i]])
        i += 1
    with open('record.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        for i in New_list:
            writer.writerow(i)
    csvFile.close()

def main():
    plot_all()
    plot_separated()
    writeIntocsv()

main()
plt.show()




