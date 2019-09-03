import HighPrecision_ADDA as converter
import time
import math
import threading

conv = converter.AD_DA()

forward = 500
rotate = 500

count = 0
while count < 10:
    conv.SET_DAC0(2500, conv.data_format.voltage)
    conv.SET_DAC1(2500, conv.data_format.voltage)
    time.sleep(1)
    count += 1

print ("start")

while rotate <= 4500:

    while forward <= 4500:
        conv.SET_DAC0(forward, conv.data_format.voltage)
        conv.SET_DAC1(rotate, conv.data_format.voltage)
        time.sleep(8)

        conv.SET_DAC0(2500, conv.data_format.voltage)
        conv.SET_DAC1(2500, conv.data_format.voltage)
        time.sleep(3)

        print ("current speed =", forward, rotate)

        forward += 100

    rotate += 100
    forward = 500
    print ("----------------------------")

print ("finish")