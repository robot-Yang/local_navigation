#! /usr/bin/env python

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import rospy
import time

import HighPrecision_ADDA as converter
import time
import math
import signal
import matplotlib.pyplot as plt

Linear_velocity_com = [2500]
Angular_velocity_com = [2500]

class chen:
    def __init__(self):
        self.tf_angle = - 5.0  # tf_plane: 0*x + y - tan(theta * math.pi / 180)*z = 0
        self.tf_A = 0.0
        self.tf_B = 1.0
        self.tf_C = - math.tan(self.tf_angle * math.pi / 180.0)
        self.tf_D = 0.0
        # self.k = 4.0
        self.k = 0.35
        self.dest_X = 0.0
        self.dest_Z = 0.0
        self.dest_Distance = 0.0
        self.back_Distance = 0.0
        self.dest_theta = 0.0
        self.bottom_p_projected_x = 0.00
        self.bottom_p_projected_y = 0.00
        self.bottom_p_projected_z = 0.00
        self.back_p_projected_x = 0.00
        self.back_p_projected_y = 0.00
        self.back_p_projected_z = 0.00
        self.bottom_p_x = 0.00
        self.bottom_p_y = 0.00
        self.bottom_p_z = 0.00
        self.back_p_x = 0.00
        self.back_p_y = 0.00
        self.back_p_z = 0.00
        self.angle_1 = 0.0
        self.angle_2 = 0.0
        self.Kp_rho = 250
        self.L_Kp_alpha = 10.25 * 4.85
        self.L_Kp_beta = 10.25
        self.R_Kp_alpha = 10.81 * 4.85
        self.R_Kp_beta = 10.81
        self.alpha = 0.0
        self.beta = 0.0
        self.linear_speed = 2500
        self.rotate_speed = 2500
        self.adda = converter.AD_DA()
        self.sequence = 4
        self.A = [2500] * self.sequence #filter
        self.B = [2500] * self.sequence
        self.threshold_1 = 0.05
        self.threshold_2 = 0.3
        # self.Linear_velocity_com = [2500]
        # self.Angular_velocity_com = [2500]

    def project(self, bottom_p_x, bottom_p_y, bottom_p_z, back_p_x, back_p_y, back_p_z):
        self.bottom_p_projected_x = ((self.tf_B**2 + self.tf_C**2) * bottom_p_x - self.tf_A * (self.tf_B * bottom_p_y + self.tf_C * bottom_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.bottom_p_projected_y = ((self.tf_A**2 + self.tf_C**2) * bottom_p_y - self.tf_B * (self.tf_A * bottom_p_x + self.tf_C * bottom_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.bottom_p_projected_z = ((self.tf_A**2 + self.tf_B**2) * bottom_p_z - self.tf_C * (self.tf_A * bottom_p_x + self.tf_B * bottom_p_y + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.back_p_projected_x = ((self.tf_B**2 + self.tf_C**2) * back_p_x - self.tf_A * (self.tf_B * back_p_y + self.tf_C * back_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.back_p_projected_y = ((self.tf_A**2 + self.tf_C**2) * back_p_y - self.tf_B * (self.tf_A * back_p_x + self.tf_C * back_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.back_p_projected_z = ((self.tf_A**2 + self.tf_B**2) * back_p_z - self.tf_C * (self.tf_A * back_p_x + self.tf_B * bottom_p_y + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)

    def setDestination(self):
        if self.bottom_p_projected_z == 0.0 and self.back_p_projected_z == 0.0:
            self.dest_X = 0.0
            self.dest_Z = 0.0
        if self.bottom_p_projected_z == self.back_p_projected_z:
            self.dest_X = self.bottom_p_projected_x
            self.dest_Z = self.bottom_p_projected_z
        else:
            self.dest_X = self.bottom_p_projected_x + self.k * (self.bottom_p_projected_x - self.back_p_projected_x) / abs(self.bottom_p_projected_z - self.back_p_projected_z)
            self.dest_Z = self.bottom_p_projected_z + self.k * (self.bottom_p_projected_z - self.back_p_projected_z) / abs(self.bottom_p_projected_z - self.back_p_projected_z)
        self.dest_Distance = (self.dest_X**2 + self.dest_Z**2) ** 0.5
        self.back_Distance = (self.back_p_projected_x**2 + self.back_p_projected_z**2) ** 0.5
        print "destination", self.dest_X, self.dest_Z

    def setDestination_close(self):
        if self.bottom_p_projected_z == 0.0 and self.back_p_projected_z == 0.0:
            self.dest_X = 0.0
            self.dest_Z = 0.0
        if self.bottom_p_projected_z == self.back_p_projected_z:
            self.dest_X = self.bottom_p_projected_x
            self.dest_Z = self.bottom_p_projected_z
        else:
            self.dest_X = self.back_p_projected_x
            self.dest_Z = self.back_p_projected_z
        self.dest_Distance = (self.dest_X**2 + self.dest_Z**2) ** 0.5
        self.back_Distance = (self.back_p_projected_x**2 + self.back_p_projected_z**2) ** 0.5
        print "destination_close", self.dest_X, self.dest_Z

    def AngleAlpha(self):
        if self.dest_X == 0:
            angle_0 = 90.0
        else:
            angle_0 = math.degrees(math.atan(self.dest_Z / self.dest_X))
        if angle_0 < 0:
            angle_0 = angle_0 + 180.0
        self.alpha = angle_0 - 90.0
        print "alpha", self.alpha

    def AngleBeta(self):
        # destination angle
        if self.dest_X == 0:
            angle_0 = 90.0
        else:
            angle_0 = math.degrees(math.atan(self.dest_Z / self.dest_X))
        if angle_0 < 0:
            angle_0 = angle_0 + 180.0
        # chair angle
        if self.back_p_projected_x - self.bottom_p_projected_x == 0:
            angle_2 = 90.0
        else:
            angle_2 = math.degrees(math.atan((self.back_p_projected_z - self.bottom_p_projected_z) / (
                        self.back_p_projected_x - self.bottom_p_projected_x)))
        if angle_2 < 0:
            angle_2 = angle_2 + 180.0
        self.beta =  angle_0 - angle_2
        print "beta", self.beta

    def SpeedTOGo(self):
        self.linear_speed = 1500 # 1875  - self.Kp_rho * self.dest_Distance
        print "SpeedToGO", self.linear_speed

    def AngleToGo(self, angle_1, angle_2):
        L_rotate_speed = 2500 + self.L_Kp_alpha * self.alpha + self.L_Kp_beta * self.beta
        R_rotate_speed = 2500 + self.R_Kp_alpha * self.alpha + self.R_Kp_beta * self.beta
        if L_rotate_speed >= 2500:
            self.rotate_speed = L_rotate_speed
        else:
            self.rotate_speed = R_rotate_speed
        print "rotate value", self.rotate_speed

    # for both move_average and butterworth filter
    def read_update(self, a, b):
        self.A.append(a)
        self.B.append(b)
        self.A.pop(0)
        self.B.pop(0)

    # move_average filter
    def move_average(self):
        self.linear_speed = sum(self.A) / self.sequence
        self.rotate_speed = sum(self.B) / self.sequence

    def setMov(self, speed, direction):
        if speed <= 1000:
            speed = 1000
        elif speed >= 2500:
            speed = 2500
        if direction >= 4000:
            direction = 4000
        elif direction <= 1000:
            direction = 1000
        print "          ----> DAC0", speed, "    DAC1: ", direction
        self.adda.SET_DAC0(int(speed), self.adda.data_format.voltage)
        self.adda.SET_DAC1(int(direction), self.adda.data_format.voltage)

    def callback_pointcloud1(self, data):
        assert isinstance(data, PointCloud2)
        gen = point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)
        # time.sleep(1)
        # print type(gen)
        for p in gen:
            self.bottom_p_x = round(p[0], 3)
            self.bottom_p_y = round(p[1], 3)
            self.bottom_p_z = round(p[2], 3)
            # print " bottom:  x : %.3f  y: %.3f  z: %.3f" % (p[0], p[1], p[2])

    def callback_pointcloud2(self, data):
        assert isinstance(data, PointCloud2)
        gen = point_cloud2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)
        # time.sleep(1)
        # print type(gen)
        for p in gen:
            self.back_p_x = round(p[0], 3)
            self.back_p_y = round(p[1], 3)
            self.back_p_z = round(p[2], 3)
            # print " back:  x : %.3f  y: %.3f  z: %.3f" % (p[0], p[1], p[2])

    def main(self):
        print("signal 0")
        rospy.init_node('docking', anonymous=True)

        while not rospy.is_shutdown():
            print("signal 1")
            rospy.Subscriber('/centroid_bottom', PointCloud2, self.callback_pointcloud1)
            rospy.Subscriber('/centroid_back', PointCloud2, self.callback_pointcloud2)
            self.project(self.bottom_p_x, self.bottom_p_y, self.bottom_p_z, self.back_p_x, self.back_p_y, self.back_p_z)
            self.setDestination()

            # check b, d
            b = self.adda.ReadChannel(2, self.adda.data_format.voltage)
            a = self.adda.ReadChannel(3, self.adda.data_format.voltage)
            c = self.adda.ReadChannel(4, self.adda.data_format.voltage)
            d = self.adda.ReadChannel(5, self.adda.data_format.voltage)
            e = self.adda.ReadChannel(6, self.adda.data_format.voltage)
            if b < 3000 or d < 3000 or c > 100:
                print("docking pause-------")
                break

            while self.back_Distance > self.threshold_2:
                print("signal 2")
                b = self.adda.ReadChannel(2, self.adda.data_format.voltage)
                a = self.adda.ReadChannel(3, self.adda.data_format.voltage)
                c = self.adda.ReadChannel(4, self.adda.data_format.voltage)
                d = self.adda.ReadChannel(5, self.adda.data_format.voltage)
                e = self.adda.ReadChannel(6, self.adda.data_format.voltage)
                if b < 3000 or d < 3000 or c >100:
                    break

                # rotate value calculate
                if self.back_Distance <= 1.10:
                    self.setDestination_close()
                    self.SpeedTOGo()
                    self.AngleAlpha()
                    self.AngleBeta()
                    self.AngleToGo(self.alpha, self.beta)
                elif self.back_Distance <= 0.95:
                    self.linear_speed = 1800
                    self.rotate_speed = 2500
                else:
                    self.SpeedTOGo()
                    self.AngleAlpha()
                    self.AngleBeta()
                    self.AngleToGo(self.alpha, self.beta)

                # self.SpeedTOGo()
                self.read_update(self.linear_speed, self.rotate_speed)
                self.move_average()
                self.setMov(self.linear_speed, self.rotate_speed)
                Linear_velocity_com.append(self.linear_speed)
                Angular_velocity_com.append(self.rotate_speed)

                rospy.Subscriber('/centroid_bottom', PointCloud2, self.callback_pointcloud1)
                rospy.Subscriber('/centroid_back', PointCloud2, self.callback_pointcloud2)
                self.project(self.bottom_p_x, self.bottom_p_y, self.bottom_p_z, self.back_p_x, self.back_p_y,
                             self.back_p_z)
                self.setDestination()

                # self.threshold_1 = #0.05
                self.threshold_2 = 0.78 #0.3

                rospy.sleep(0.1)

            self.linear_speed = 2500
            self.rotate_speed = 2500
            self.read_update(self.linear_speed, self.rotate_speed)
            self.move_average()
            self.setMov(self.linear_speed, self.rotate_speed)
            Linear_velocity_com.append(self.linear_speed)
            Angular_velocity_com.append(self.rotate_speed)

            rospy.sleep(1)


# # for interruption
# def exit(signum, frame):
#     print('      >>>>>>> You choose to stop me.')
#     print("Linear_velocity_com = ", Linear_velocity_com)
#     print("Angular_velocity_com = ", Angular_velocity_com)
#     exit()
#
# # for interruption
# signal.signal(signal.SIGINT, exit)
# signal.signal(signal.SIGTERM, exit)

# a = chen()
# a.main()