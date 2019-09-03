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

def main():
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

    conv.SET_DAC0(2500, conv.data_format.voltage)
    conv.SET_DAC1(2500, conv.data_format.voltage)

    print("a=", a, "b=", b, "c=", c, "d=", d, "e=", e)

    time.sleep(0.1)

try:
    while True:
        main()
except KeyboardInterrupt:
    pass


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
# print("OX = ", OX)
# print("----------------")

AA1 = heapq.nlargest(len(AA)/10, AA)
BB1 = heapq.nlargest(len(BB)/10, BB)
CC1 = heapq.nlargest(len(CC)/10, CC)
DD1 = heapq.nlargest(len(DD)/10, DD)
EE1 = heapq.nlargest(len(EE)/10, EE)

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

