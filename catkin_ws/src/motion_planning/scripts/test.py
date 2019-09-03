#! /usr/bin/env python

import path_planning5_1 as docking
import HighPrecision_ADDA as converter
import time
import math
import threading

aa = docking.chen()

while True:
    a = aa.adda.ReadChannel(3, aa.adda.data_format.voltage)
    b = aa.adda.ReadChannel(2, aa.adda.data_format.voltage)
    c = aa.adda.ReadChannel(4, aa.adda.data_format.voltage)
    d = aa.adda.ReadChannel(5, aa.adda.data_format.voltage)
    e = aa.adda.ReadChannel(6, aa.adda.data_format.voltage)
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

    # adda.SET_DAC0(500, adda.data_format.voltage)
    # adda.SET_DAC1(2500, adda.data_format.voltage)

    # adda.SET_DAC0(2500, adda.data_format.voltage)
    # adda.SET_DAC1(2500, adda.data_format.voltage)

    print("a=",a, "b=",b,"c=",c,"d=",d, "e=",e)
    # print("a=", a, "b=", b)
    # print "q"

    time.sleep(0.1)

# adda.SET_DAC0(4500, adda.data_format.voltage)
# adda.SET_DAC1(2500, adda.data_format.voltage)