#! /usr/bin/env python

import HighPrecision_ADDA as converter
import time
import math
from itertools import groupby
# import threading
# import RPi.GPIO as GPIO
import numpy as np
# from scipy.signal import butter, lfilter, freqz
# import matplotlib.pyplot as plt
import heapq

conv = converter.AD_DA()

# coefficient for vmax and wmax(outout curve)
forward_coefficient = 1
left_turning_coefficient = 1
right_turning_coefficient = 1
backward_coefficient = 0.5

# # default value for pre-configuration
# k1 = 8
# k2 = 0.5
# k3 = 1
# k4 = 1
# k5 = 4
# default value for pre-configuration
k1 = 6.2
k2 = 0.89
k3 = 1
k4 = 0.88
k5 = 10

# # coefficient for calculate center of pressure: ox
# r1 = -3
# r2 = -1.5
# r3 = 0
# r4 = 1.5
# r5 = 3
# coefficient for calculate center of pressure: ox
r1 = -2
r2 = -1
r3 = 0
r4 = 1
r5 = 2

# # classification point for center of pressure ox(calibration needed)
# pl2 = -2.7
# pl1 = -0.6
# pr1 = 0.6
# pr2 = 2.5
# classification point for center of pressure ox(calibration needed)
pl2 = -1.2
pl1 = -0.4
pr1 = 0.4
pr2 = 1.2

# for both move_average and butterworth filter
counter1 = 0
sequence = 2
original = 20
A = [original] * sequence
B = [original] * sequence
C = [original] * sequence
D = [original] * sequence
E = [original] * sequence

A1 = [original] * sequence
B1 = [original] * sequence
C1 = [original] * sequence
D1 = [original] * sequence
E1 = [original] * sequence

# record sensor reading
AA = []
BB = []
CC = []
DD = []
EE = []
OX = []
COM_DAC0 = []
COM_DAC1 = []

# read data from ADDA board
def read():
    global original
    b = conv.ReadChannel(2, conv.data_format.voltage)
    a = conv.ReadChannel(3, conv.data_format.voltage)
    c = conv.ReadChannel(4, conv.data_format.voltage)
    d = conv.ReadChannel(5, conv.data_format.voltage)
    e = conv.ReadChannel(6, conv.data_format.voltage)
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    e = float(e)
    a = round(a, 2)
    b = round(b, 2)
    c = round(c, 2)
    d = round(d, 2)
    e = round(e, 2)
    # a = a - original + 1 # +1 because if without 1 a+b+c+d+e = 0 could happen!
    # b = b - original + 1
    # c = c - original + 1
    # d = d - original + 1
    # e = e - original + 1
    AA.append(a)
    BB.append(b)
    CC.append(c)
    DD.append(d)
    EE.append(e)
    print("a=", a, "b=", b, "c=", c, "d=", d, "e=", e)
    return a,b,c,d,e

# pre_calibration with default value
def pre_calibration(a,b,c,d,e):
    global k1, k2, k3, k4, k5
    a = k1 * a
    b = k2 * b
    c = k3 * c
    d = k4 * d
    e = k5 * e
    return a,b,c,d,e

# for both move_average and butterworth filter
def read_update(a,b,c,d,e):
    A.append(a)
    B.append(b)
    C.append(c)
    D.append(d)
    E.append(e)
    A.pop(0)
    B.pop(0)
    C.pop(0)
    D.pop(0)
    E.pop(0)
    # return A, B, C, D, E

# move_average filter
def move_average():
    global A, B, C, D, E
    a1 = sum(A) / sequence
    b1 = sum(B) / sequence
    c1 = sum(C) / sequence
    d1 = sum(D) / sequence
    e1 = sum(E) / sequence
    return a1, b1, c1, d1, e1

# online pre_calibration
def online_pre_calibration():
    global k1, k2, k3, k4, k5
    print k1, k2, k3, k4, k5
    print 'start online pre_calibration'
    counter = 1
    A = []
    B = []
    C = []
    D = []
    E = []

    while counter <= 500:
        a, b, c, d, e = read()
        A.append(a)
        B.append(b)
        C.append(c)
        D.append(d)
        E.append(e)
        counter += 1
        time.sleep(0.01)

    A = heapq.nlargest(len(A) / 4, A)
    B = heapq.nlargest(len(B) / 4, B)
    C = heapq.nlargest(len(C) / 4, C)
    D = heapq.nlargest(len(D) / 4, D)
    E = heapq.nlargest(len(E) / 4, E)
    k1 = (4500 - 2500) / np.mean(A)
    k2 = (4500 - 2500) / np.mean(B)
    k3 = (4500 - 2500) / np.mean(C)
    k4 = (4500 - 2500) / np.mean(D)
    k5 = (4500 - 2500) / np.mean(E)
    print k1, k2, k3, k4, k5
    print 'online pre_calibration_automated'

# calibration for pl2, pl1, pr1, pr2
def calibration():
    global pl2, pl1, pr1, pr2
    global forward_coefficient, left_turning_coefficient, right_turning_coefficient
    print pl2, pl1, pr1, pr2
    print 'start calibrating'
    counter = 1
    OX = []
    Drive = []
    Drive1 = []
    Drive2 = []
    Drive3 = []
    while counter <= 500:
        a, b, c, d, e = read()
        a, b, c, d, e = pre_calibration(a,b,c,d,e)
        drive = max(a,b,c,d,e)
        Drive.append(drive)
        ox = (r1*a + r2*b + r3*c + r4*d + r5*e) / (a + b + c + d + e)  # calibration needed(in the furure)
        ox = round(ox, 2)
        OX.append(ox)
        counter += 1
        time.sleep(0.01)

    OX1 = sorted(OX)
    Len_OX1 = len(OX1)
    print Len_OX1
    dic0 = {}
    dic1 = {}

    for k, g in groupby(OX1, key=lambda x: (x - 1) // 0.5):
        dic0['{}-{}'.format(k * 0.5, (k + 1) * 0.5)] = len(list(g))  # len(list(g))

    for k, g in groupby(OX1, key=lambda x: (x - 1) // 0.5):
        dic1['{}-{}'.format(k * 0.5, (k + 1) * 0.5)] = list(g)

    a = dic0.keys()
    b = dic0.values()
    c = dic1.values()

    i = 0
    average_value = []
    while i < len(b):
        if float(b[i]) / float(Len_OX1) >= 0.1:
            average_value.append(float(sum(c[i])) / float(len(c[i])))
        i += 1

    pl2 = min(average_value) + 0.3
    pr2 = max(average_value) - 0.3
    pl1 = pl2 + (pr2 - pl2) / 4
    pr1 = pr2 - (pr2 - pl2) / 4

    for k in range(len(OX)):
        if OX[k] >= pl1 and OX[k] <= pr1:
            Drive1.append(Drive[k])
        elif OX[k] <= pl2:
            Drive2.append(Drive[k])
        elif OX[k] >= pr2:
            Drive3.append(Drive[k])

    Drive1 = heapq.nlargest(len(Drive1)/4, Drive1)
    Drive2 = heapq.nlargest(len(Drive2)/4, Drive2)
    Drive3 = heapq.nlargest(len(Drive3)/4, Drive3)

    drive = np.mean(Drive1)
    forward_coefficient = (4500 - 2500)/drive
    forward_coefficient = round(forward_coefficient, 2)
    drive = np.mean(Drive2)
    left_turning_coefficient = (4500 - 2500)/drive
    left_turning_coefficient = round(left_turning_coefficient, 2)
    drive = np.mean(Drive3)
    right_turning_coefficient = (4500 - 2500)/drive
    right_turning_coefficient = round(right_turning_coefficient, 2)

    # print averge_value
    print max(average_value), min(average_value), forward_coefficient, left_turning_coefficient, right_turning_coefficient
    print pl2, pl1, pr1, pr2
    # return 0

# output curve: Linear/Angular Velocity-Pressure Center
def output(a, b, c, d, e, ox):
    global forward_coefficient, left_turning_coefficient, right_turning_coefficient, backward_coefficient
    #sending value setting
    # static_value = 20
    dynamic_value = max(a,b,c,d,e)
    # drive = dynamic_value - static_value
    drive = dynamic_value

    forward = 2500 + forward_coefficient * drive
    if ox > 0 or ox < 0:
        left_around = 2500 + left_turning_coefficient * drive * ox / abs(ox)
    else:
        left_around = 2500
    if ox > 0 or ox < 0:
        right_around = 2500 + right_turning_coefficient * drive * ox / abs(ox)
    else:
        right_around = 2500

    global pl2, pl1, pr1, pr2

    wl = math.pi / (pl2 - pl1) # w for smooth fucntion: sin(wx)
    fai_l_for = math.pi / 2 - wl * pl1
    fai_l_turn = math.pi / 2 - wl * pl2

    wr = math.pi / (pr2 - pr1) # w for smooth fucntion: sin(wx)
    fai_r_for = math.pi / 2 - wr * pr1
    fai_r_turn = math.pi / 2 - wr * pr2

    left_angle_for = 2500 + forward_coefficient * drive / 2 + forward_coefficient * drive / 2 * math.sin(wl * ox + fai_l_for)
    left_angle_turn = 2500 - left_turning_coefficient * drive / 2 - left_turning_coefficient * drive / 2 * math.sin(wl * ox + fai_l_turn)
    right_angle_for = 2500 + forward_coefficient * drive / 2 + forward_coefficient * drive / 2 * math.sin(wr * ox + fai_r_for)
    right_angle_turn = 2500 + right_turning_coefficient * drive / 2 + right_turning_coefficient * drive / 2 * math.sin(wr * ox + fai_r_turn)

    backward = 2500 - backward_coefficient * drive

    # threshold value for keep safety(beyond this value, the joystick will report an error)
    if forward >= 4800:
        forward = 4800
    if left_angle_for >= 4800:
        left_angle_for = 4800
    if right_angle_for >= 4800:
        right_angle_for = 4800
    if right_around >= 4800:
        right_around = 4800
    if left_around <= 300:
        left_around = 300
    if right_angle_turn >= 4800:
        right_angle_turn = 4800
    if left_angle_turn <= 300:
        left_angle_turn = 300
    if backward <= 800:
        backward = 800

    return forward, backward, left_angle_for, left_angle_turn, right_angle_for, right_angle_turn, left_around, right_around

# execution command to DAC board based on the output curve
def execution(a, b, c, d, e, ox):
    treshold  = 300
    global pl2, pl1, pr1, pr2
    forward, backward, left_angle_for, left_angle_turn, right_angle_for, right_angle_turn, left_around, right_around = output(a, b, c, d, e, ox)
    forward = round(forward, 0)
    backward = round(backward, 0)
    left_angle_for = round(left_angle_for, 0)
    left_angle_turn = round(left_angle_turn, 0)
    right_angle_for = round(right_angle_for, 0)
    right_angle_turn = round(right_angle_turn, 0)
    left_around = round(left_around, 0)
    right_around = round(right_around, 0)

    if ox <= pr1 and ox >= pl1 and c >= treshold:
        # print("forward")
        conv.SET_DAC0(forward, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        COM_DAC0.append(forward)
        COM_DAC1.append(2500)
        print("forward", forward)
        # continue
    # turn an angle
    elif (ox <= pl1 and ox >= pl2 and e <= treshold):
        # print("angle")
        conv.SET_DAC0(left_angle_for, conv.data_format.voltage)
        conv.SET_DAC1(left_angle_turn, conv.data_format.voltage)
        print("left_angle", left_angle_for, left_angle_turn)
        COM_DAC0.append(left_angle_for)
        COM_DAC1.append(left_angle_turn)
        # continue
    elif (ox >= pr1 and ox <= pr2 and a <= treshold):
        # print("angle")
        conv.SET_DAC0(right_angle_for, conv.data_format.voltage)
        conv.SET_DAC1(right_angle_turn, conv.data_format.voltage)
        COM_DAC0.append(right_angle_for)
        COM_DAC1.append(right_angle_turn)
        print("right_angle", right_angle_for, right_angle_turn)
        # continue
    # turn around
    elif (ox <= pl2 and e <= treshold):
        # print("around")
        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(left_around, conv.data_format.voltage)
        COM_DAC0.append(2500)
        COM_DAC1.append(left_around)
        print("left_around", left_around)
        # continue
    elif (ox >= pr2 and a<=treshold):
        # print("around")
        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(right_around, conv.data_format.voltage)
        COM_DAC0.append(2500)
        COM_DAC1.append(right_around)
        print("right_around", right_around)
    # backward
    elif a >= treshold and e >= treshold and c < 300:
        conv.SET_DAC0(backward, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        COM_DAC0.append(backward)
        COM_DAC1.append(2500)
        print("backward", backward)
    else:
        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        COM_DAC0.append(2500)
        COM_DAC1.append(2500)
        print("stop")


def main():
    global A1, B1, C1, D1, E1
    global r1, r2, r3, r4, r5
    global counter1
    a, b, c, d, e = read()
    a, b, c, d, e = pre_calibration(a,b,c,d,e)
    # read_update(a, b, c, d, e)
    # print("a=",a, "b=",b,"c=",c,"d=",d, "e=",e, "ox=", ox)

    # calibration
    # if b>=3000 and d>=3000:
    #     calibration()

    # move_average filter execution
    # a, b, c, d, e = move_average()
    ox = (r1*a + r2*b + r3*c + r4*d + r5*e) / (a + b + c + d + e)
    ox = round(ox, 2)
    OX.append(ox)
    print ox
    execution(a, b, c, d, e, ox)

    # butterworth filter execution
    # global counter
    # if counter == 2:
    #     counter = 0
    #     butterworth()
    # a = A1[counter]
    # b = B1[counter]
    # c = C1[counter]
    # d = D1[counter]
    # e = E1[counter]
    # ox = (r1*a + r2*b + r3*c + r4*d + r5*e) / (a + b + c + d + e)
    # ox = round(ox, 2)
    # execution(a, b, c, d, e, ox)
    # counter += 1

    counter1 += 1  # for calculate frequency

    time.sleep(0.01)

start = time.time()  # for calculate frequency
try:
    while True:
        main()
except KeyboardInterrupt:
    pass
end = time.time()  # for calculate frequency

print float(counter1) / float(end - start) # for calculate frequency
# print counter

print("AA = ", AA)
print("----------------")
print("BB = ", BB)
print("----------------")
print("CC = ", CC)
print("----------------")
print("DD = ", DD)
print("----------------")
print("EE = ", EE)
print("----------------")
print("OX = ", OX)
print("----------------")
print("COM_DAC0 = ", COM_DAC0)
print("----------------")
print("COM_DAC1 = ", COM_DAC1)
print("----------------")