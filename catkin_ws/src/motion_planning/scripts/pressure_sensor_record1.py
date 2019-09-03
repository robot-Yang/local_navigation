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
import logging
from logging import handlers

conv = converter.AD_DA()

# coefficient for vmax and wmax(outout curve)
forward_coefficient = 1
left_turning_coefficient = 1
right_turning_coefficient = 1
backward_coefficient = 0.5

# default value for pre-configuration
k1, k2, k3, k4, k5 =   0.84, 0.72, 0.7, 0.72, 0.7 # 2.48, 0.91, 1.59, 1.75, 1.46

# # coefficient for calculate center of pressure: ox
r1 = -2
r2 = -1
r3 = 0
r4 = 1
r5 = 2

# classification point for center of pressure ox(calibration needed)
pl2, pl1, pr1, pr2 =   -0.95, -0.32999999999999996, 0.27, 0.88999999999999996  # -0.275, 0.535, 1.1800000000000002       -0.97, -0.2, 0.2, 1.17

# read k* and p* from txt file
f1 = open('k*+p*write.txt')
lines = f1.readlines()
K = lines[0].strip('\n')
K = K.split(',')
P = lines[1].strip('\n')
P = P.split(',')
k1, k2, k3, k4, k5 = float(K[0]),float(K[1]),float(K[2]),float(K[3]),float(K[4])
pl2, pl1, pr1, pr2 = float(P[0]),float(P[1]),float(P[2]),float(P[3])
print(k1, k2, k3, k4, k5)
print(pl2, pl1, pr1, pr2 )
f1.close()

Command_DAC0 = 2500
Command_DAC1 = 2500

counter1 = 0
number = 100

AA = []
BB = []
CC = []
DD = []
EE = []
OX = []

level_relations = {
        # 'debug':logging.DEBUG,
        'info':logging.INFO,
        # 'warning':logging.WARNING,
        # 'error':logging.ERROR,
        # 'crit':logging.CRITICAL
    }

def log(a0, b0, c0, d0, e0, a, b, c, d, e, ox, Command_DAC0, Command_DAC1, filename,level,fmt='%(created).6f %(message)s'):
    logger = logging.getLogger(filename)
    format_str = logging.Formatter(fmt)
    logger.setLevel(level_relations.get(level))
    sh = logging.StreamHandler()
    sh.setFormatter(format_str)
    th = logging.handlers.TimedRotatingFileHandler(filename=filename,encoding='utf-8')
    th.setFormatter(format_str)
    logger.addHandler(sh)
    logger.addHandler(th)
    logger.info("%s %s %s %s %s %s %s %s %s %s %s %s %s", a0, b0, c0, d0, e0, a, b, c, d, e, ox, Command_DAC0, Command_DAC1)
    logger.removeHandler(sh)
    logger.removeHandler(th)

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

def collect():
    counter = 0
    while counter < number:
        a, b, c, d, e = read()

        AA.append(a)
        BB.append(b)
        CC.append(c)
        DD.append(d)
        EE.append(e)

        conv.SET_DAC1(4500, conv.data_format.voltage)

        counter += 1
        time.sleep(0.01)

    conv.SET_DAC1(2500, conv.data_format.voltage)
    time.sleep(2)

def pos_deal():
    global k1, k2, k3, k4, k5
    global pl2, pl1, pr1, pr2
    # pre-calibration
    AA1 = heapq.nlargest(len(AA) / 10, AA)
    BB1 = heapq.nlargest(len(BB) / 10, BB)
    CC1 = heapq.nlargest(len(CC) / 10, CC)
    DD1 = heapq.nlargest(len(DD) / 10, DD)
    EE1 = heapq.nlargest(len(EE) / 10, EE)

    aa = np.mean(AA1)
    bb = np.mean(BB1)
    cc = np.mean(CC1)
    dd = np.mean(DD1)
    ee = np.mean(EE1)

    print("AA1 = ", AA1)
    print("----------------")
    print("BB1 = ", BB1)
    print("----------------")
    print("CC1 = ", CC1)
    print("----------------")
    print("DD1 = ", DD1)
    print("----------------")
    print("EE1 = ", EE1)
    print("----------------")

    print("max_average = ", aa, bb, cc, dd, ee)
    k1 = round((4500 - 2500) / aa, 2)
    k2 = round((4500 - 2500) / bb, 2)
    k3 = round((4500 - 2500) / cc, 2)
    k4 = round((4500 - 2500) / dd, 2)
    k5 = round((4500 - 2500) / ee, 2)
    print("coefficient = ", k1, k2, k3, k4, k5)

    # post-calibration
    AA2 = [AA[i] * k1 for i in range(len(AA))]
    BB2 = [BB[i] * k2 for i in range(len(AA))]
    CC2 = [CC[i] * k3 for i in range(len(AA))]
    DD2 = [DD[i] * k4 for i in range(len(AA))]
    EE2 = [EE[i] * k5 for i in range(len(AA))]

    ox = [(-2 * AA2[i] - BB2[i] + 0 * CC2[i] + DD2[i] + 2 * EE2[i]) / (AA2[i] + BB2[i] + CC2[i] + DD2[i] + EE2[i]) for i
          in range(len(AA))]

    ox_l2 = (np.mean(ox[0:number]) + np.mean(ox[9 * number:10 * number])) / 2
    ox_l1 = (np.mean(ox[number:2 * number]) + np.mean(ox[8 * number:9 * number])) / 2
    ox_0 = (np.mean(ox[2 * number:3 * number]) + np.mean(ox[7 * number:8 * number])) / 2
    ox_r1 = (np.mean(ox[3 * number:4 * number]) + np.mean(ox[6 * number:7 * number])) / 2
    ox_r2 = (np.mean(ox[4 * number:5 * number]) + np.mean(ox[5 * number:6 * number])) / 2
    ox_l2 = round(ox_l2, 2)
    ox_l1 = round(ox_l1, 2)
    ox_0 = round(ox_0, 2)
    ox_r1 = round(ox_r1, 2)
    ox_r2 = round(ox_r2, 2)

    pl2, pl1, pr1, pr2 = ox_l2 + 0.2, ox_0 - 0.3, ox_0 + 0.3, ox_r2 - 0.2
    print("ox_* = ", ox_l2, ox_l1, ox_0, ox_r1, ox_r2)
    print("p_*0 = ", ox_l2 + 0.2, ox_0 - 0.3, ox_0 + 0.3, ox_r2 - 0.2)
    print("p_*1 = ", (ox_l2 + ox_l1)/2, (ox_l1 + ox_0)/2, (ox_0 + ox_r1)/2, (ox_r1 + ox_r2)/2)

    f0 = open('k*+p*add.txt', 'a')
    f0.writelines(str(k1) + ',' + str(k2) + ',' + str(k3) + ',' + str(k4) + ',' + str(k5))
    f0.write('\n')
    f0.writelines(str(pl2) + ',' + str(pl1) + ',' + str(pr1) + ',' + str(pr2))
    f0.write('\n')
    f0.close()
    f1 = open('k*+p*write.txt', 'w')
    f1.writelines(str(k1) + ',' + str(k2) + ',' + str(k3) + ',' + str(k4) + ',' + str(k5))
    f1.write('\n')
    f1.writelines(str(pl2) + ',' + str(pl1) + ',' + str(pr1) + ',' + str(pr2))
    f1.write('\n')
    f1.close()

# online calibration
def calibration():
    AA = []
    BB = []
    CC = []
    DD = []
    EE = []
    conv.SET_DAC1(2500, conv.data_format.voltage)
    time.sleep(3)
    counter0 = 0
    while counter0 < 10:
        collect()
        counter0 += 1
    pos_deal()
    print 'online calibration finished'
    time.sleep(3)

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
    treshold  = 1000 # avoid unstoppable and undistinguishable
    global pl2, pl1, pr1, pr2
    global Command_DAC0, Command_DAC1
    forward, backward, left_angle_for, left_angle_turn, right_angle_for, right_angle_turn, left_around, right_around = output(a, b, c, d, e, ox)
    forward = round(forward, 0)
    backward = round(backward, 0)
    left_angle_for = round(left_angle_for, 0)
    left_angle_turn = round(left_angle_turn, 0)
    right_angle_for = round(right_angle_for, 0)
    right_angle_turn = round(right_angle_turn, 0)
    left_around = round(left_around, 0)
    right_around = round(right_around, 0)

    if ox <= pr1 and ox >= pl1 and c >= 700:
        # print("forward")
        conv.SET_DAC0(forward, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        Command_DAC0 = forward
        Command_DAC1 = 2500
        print("forward", forward)
        # continue
    # turn an angle
    elif (ox <= pl1 and ox >= pl2 and e <= treshold and b >= treshold):
        # print("angle")
        conv.SET_DAC0(left_angle_for, conv.data_format.voltage)
        conv.SET_DAC1(left_angle_turn, conv.data_format.voltage)
        print("left_angle", left_angle_for, left_angle_turn)
        Command_DAC0 = left_angle_for
        Command_DAC1 = left_angle_turn
        # continue
    elif (ox >= pr1 and ox <= pr2 and a <= treshold and d >= treshold):
        # print("angle")
        conv.SET_DAC0(right_angle_for, conv.data_format.voltage)
        conv.SET_DAC1(right_angle_turn, conv.data_format.voltage)
        Command_DAC0 = right_angle_for
        Command_DAC1 = right_angle_turn
        print("right_angle", right_angle_for, right_angle_turn)
        # continue
    # turn around
    elif (ox <= pl2 and e <= treshold and a >= treshold):
        # print("around")
        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(left_around, conv.data_format.voltage)
        Command_DAC0 = 2500
        Command_DAC1 = left_around
        print("left_around", left_around)
        # continue
    elif (ox >= pr2 and a<=treshold and e >= treshold):
        # print("around")
        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(right_around, conv.data_format.voltage)
        Command_DAC0 = 2500
        Command_DAC1 = right_around
        print("right_around", right_around)
    # backward
    elif a >= treshold and e >= treshold and c < 300:
        conv.SET_DAC0(backward, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        Command_DAC0 = backward
        Command_DAC1 = 2500
        print("backward", backward)
    else:
        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        Command_DAC0 = 2500
        Command_DAC1 = 2500
        print("stop")

def main():
    global A1, B1, C1, D1, E1
    global r1, r2, r3, r4, r5
    global Command_DAC0, Command_DAC1
    global counter1
    a, b, c, d, e = read()
    a0, b0, c0, d0, e0 = a, b, c, d, e

    switch = conv.ReadChannel(7, conv.data_format.voltage)
    if switch > 1000:
        calibration()

    a, b, c, d, e = pre_calibration(a,b,c,d,e)

    ox = (r1*a + r2*b + r3*c + r4*d + r5*e) / (a + b + c + d + e)
    ox = round(ox, 2)
    print ox
    execution(a, b, c, d, e, ox)

    counter1 += 1  # for calculate frequency

    # log file
    a0, b0, c0, d0, e0 = str(a0),str(b0),str(c0),str(d0),str(e0)
    a0, b0, c0, d0, e0 = a0.ljust(8),b0.ljust(8),c0.ljust(8),d0.ljust(8),e0.ljust(8)
    a, b, c, d, e, ox, = str(a),str(b),str(c),str(d),str(e),str(ox)
    a, b, c, d, e, ox, = a.ljust(8),b.ljust(8),c.ljust(8),d.ljust(8),e.ljust(8),ox.ljust(8)
    Command_DAC0, Command_DAC1 = str(Command_DAC0),str(Command_DAC1)
    Command_DAC0, Command_DAC1 = Command_DAC0.ljust(8), Command_DAC1.ljust(8)
    log(a0, b0, c0, d0, e0, a, b, c, d, e, ox, Command_DAC0, Command_DAC1, 'info_luis_ni2.log', level='info')

    time.sleep(0.01)

start = time.time()  # for calculate frequency
try:
    while True:
        main()
except KeyboardInterrupt:
    pass
end = time.time()  # for calculate frequency

print float(counter1) / float(end - start) # for calculate frequency
