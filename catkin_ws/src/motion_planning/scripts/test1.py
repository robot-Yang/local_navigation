import HighPrecision_ADDA as converter
import time
import math
import threading
import RPi.GPIO as GPIO

conv = converter.AD_DA()

while True:

    b = conv.ReadChannel(3, conv.data_format.voltage)
    a = conv.ReadChannel(2, conv.data_format.voltage)
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

    print("a=",a, "b=",b,"c=",c,"d=",d, "e=",e)
    # print("a=", a, "b=", b)

    time.sleep(0.1)