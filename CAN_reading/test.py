import numpy as np

# a = [1,2,3]
# b = [2,3,4]
# c = [3,4,5]
# He = np.sum([a,b,c],axis = 0)
# print(He)


Linear_velocity = [0] # real speed calcualted from control law
Angular_velocity = [0]
wheel_L_com = [1650] # command directly sent to wheels, range (0, 5000)
wheel_R_com = [1650]

GEAR = 15.24
DISTANCE = 0.55 # 0.55  # distance bettween two wheels
RADIUS = 0.5588/2 # meter
W_ratio = 1 # a radio to limit the angular velovity (1 represents full speed)

MaxSpeed = 6.0 # max Qolo speed: km/h
Max_motor_v = MaxSpeed*1000/3600/RADIUS/(2*np.pi)*60*GEAR # max motor speed: 1200 rpm
print('Max_motor_v =', Max_motor_v)

Max_motor_v = 1000
MaxSpeed1 = Max_motor_v/1000*3600*RADIUS*(2*np.pi)/60/GEAR
print('MaxSpeed1 =', MaxSpeed1)