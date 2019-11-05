import numpy as np
# import matplotlib.pyplot as plt
import signal
import time
# A = []
# def add():
# 	A.append(1)

# l= 0.1
# d =0.6
# rho = 
# OB = rho * np.sin(beta) / np.sin(np.pi-alpha-beta)
# BC = rho * np.sin(alpha) / np.sin(np.pi-alpha-beta)
# AB = OB - l
# BD = BC + d
# AD = AB**2 + BD**2 - 2*AB*BD*np.cos(np.pi-self.alpha-self.beta)
# self.alphaStar = np.arcsin(BD*np.sin(np.pi-self.alpha-self.beta) / AD)

GEAR = 12.64
DISTANCE = 0.62  # distance bettween two wheels
RADIUS = 0.304/2 # meter
W_ratio = 4 # a radio to limit the angular velovity (1 represents full speed)

def transformTo_Lowevel(linear_speed, angular_speed):
    global DISTANCE, RADIUS
    # Command_W = 5000
    MaxSpeed = 5.44 # max Qolo speed: km/h
    MaxAngularVlocity = MaxSpeed*1000/3600/(DISTANCE/2)
    Max_motor_v = MaxSpeed*1000/3600/RADIUS/(2*np.pi)*60*GEAR # max motor speed: 1200 rpm

    speed_L = linear_speed - DISTANCE*angular_speed/2
    speed_R = linear_speed + DISTANCE*angular_speed/2

    motor_L = Max_motor_v*speed_L / (MaxSpeed*1000/3600)
    motor_R = Max_motor_v*speed_R / (MaxSpeed*1000/3600)
    # print("left wheel = ",speed_L, "right wheel = ",speed_R)
    # print("left wheel = ",motor_L, "right wheel = ",motor_R)
    # print(MaxAngularVlocity)
    # print("left wheel = ",rpm_L, "right wheel = ",rpm_R)
    Command_L = 5000*motor_L/(2*Max_motor_v) + 2500
    Command_R = 5000*motor_R/(2*Max_motor_v) + 2500
    Command_L = round(Command_L, 2)
    Command_R = round(Command_R, 2)
    # print(Command_L, Command_R)
    return Command_L, Command_R
# for interruption
def exit(signum, frame):
    # conv.SET_DAC0(2500, conv.data_format.voltage)
    # conv.SET_DAC1(2500, conv.data_format.voltage)
    # conv.SET_DAC2(0, conv.data_format.voltage)
    print("...")
    exit()

# for interruption
# signal.signal(signal.SIGINT, exit)
# signal.signal(signal.SIGTERM, exit)

def main():
    while True:
        linear_speed = 3 # m/s
        angular_speed = 0 # radian/s
        Command_L, Command_R = transformTo_Lowevel(linear_speed, angular_speed)
        # conv.SET_DAC0(Command_L, conv.data_format.voltage)
        # conv.SET_DAC1(Command_R, conv.data_format.voltage)
        print("left wheel = ",Command_L, "right wheel = ",Command_R)

        time.sleep(0.1)


try:
    while True:
        main()
except KeyboardInterrupt:
    pass

print("...")