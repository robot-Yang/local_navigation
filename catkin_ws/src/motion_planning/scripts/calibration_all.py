import HighPrecision_ADDA as converter
import time
import heapq
import numpy as np

conv = converter.AD_DA()

AA = []
BB = []
CC = []
DD = []
EE = []
OX = []

# conv.SET_DAC0(2500, conv.data_format.voltage)
# conv.SET_DAC1(2500, conv.data_format.voltage)

number = 50
def collect():
    counter = 0
    while counter < number:
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
        AA.append(a)
        BB.append(b)
        CC.append(c)
        DD.append(d)
        EE.append(e)

        conv.SET_DAC1(4500, conv.data_format.voltage)

        print("a=", a, "b=", b, "c=", c, "d=", d, "e=", e)

        counter += 1
        time.sleep(0.1)

    conv.SET_DAC1(2500, conv.data_format.voltage)
    time.sleep(2)

def pos_deal():
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

    print("ox_* = ", ox_l2, ox_l1, ox_0, ox_r1, ox_r2)
    print("p_* = ", ox_l2 + 0.2, ox_0 - 0.3, ox_0 + 0.3, ox_r2 - 0.2)

def main():
    conv.SET_DAC1(2500, conv.data_format.voltage)
    switch = conv.ReadChannel(7, conv.data_format.voltage)
    if switch > 1000:
        time.sleep(2)
        counter0 = 0
        while counter0 < 10:
            collect()
            counter0 += 1
        pos_deal()

try:
    while True:
        main()
except KeyboardInterrupt:
    pass

