#! /usr/bin/env python

from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2
import rospy
import time

import HighPrecision_ADDA as converter
import time
import math



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
        self.angle_3 = 0.0
        self.angle_4 = 0.0
        self.angle_6 = 90.0
        self.angle_turn = 0.0
        self.angle_go = 0.0
        self.linear_speed = 0.0
        self.basic_speed = -950
        self.rotate_speed = 0.0
        self.adda = converter.AD_DA()
        self.sequence = 4
        self.A = [0.0] * self.sequence #filter
        self.B = [0.0] * self.sequence
        self.threshold_1 = 0.05
        self.threshold_2 = 0.3

    def project(self, bottom_p_x, bottom_p_y, bottom_p_z, back_p_x, back_p_y, back_p_z):
        self.bottom_p_projected_x = ((self.tf_B**2 + self.tf_C**2) * bottom_p_x - self.tf_A * (self.tf_B * bottom_p_y + self.tf_C * bottom_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.bottom_p_projected_y = ((self.tf_A**2 + self.tf_C**2) * bottom_p_y - self.tf_B * (self.tf_A * bottom_p_x + self.tf_C * bottom_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.bottom_p_projected_z = ((self.tf_A**2 + self.tf_B**2) * bottom_p_z - self.tf_C * (self.tf_A * bottom_p_x + self.tf_B * bottom_p_y + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.back_p_projected_x = ((self.tf_B**2 + self.tf_C**2) * back_p_x - self.tf_A * (self.tf_B * back_p_y + self.tf_C * back_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.back_p_projected_y = ((self.tf_A**2 + self.tf_C**2) * back_p_y - self.tf_B * (self.tf_A * back_p_x + self.tf_C * back_p_z + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)
        self.back_p_projected_z = ((self.tf_A**2 + self.tf_B**2) * back_p_z - self.tf_C * (self.tf_A * back_p_x + self.tf_B * bottom_p_y + self.tf_D)) / (self.tf_A**2 + self.tf_B**2 + self.tf_C**2)

    def AngleToTurn(self):
        if self.back_p_projected_x - self.bottom_p_projected_x == 0:
            self.angle_1 = 90.0
        else:
            self.angle_1 = math.degrees(math.atan((self.back_p_projected_z - self.bottom_p_projected_z) / (
                        self.back_p_projected_x - self.bottom_p_projected_x)))

        if self.dest_X == 0:
            angle_2 = 90.0
        else:
            angle_2 = math.degrees(math.atan(self.dest_Z / self.dest_X))

        if self.angle_1 < 0:
            self.angle_1 = self.angle_1 + 180.0
        if angle_2 < 0:
            angle_2 = angle_2 + 180.0

        self.angle_4 = angle_2 - 90.0
        self.angle_3 = angle_2 - self.angle_1

        self.angle_turn = self.angle_4 +self.angle_3

        if self.bottom_p_projected_x == 0:
            self.angle_6 = 90.0
        else:
            self.angle_6 = math.degrees(math.atan(self.bottom_p_projected_z / self.bottom_p_projected_x))
        if abs(self.angle_6) < 70:
            self.angle_turn = 0.0

        print "AngleToTurn", self.angle_turn

    def setDestination(self):
        if self.bottom_p_projected_z == 0.0 and self.back_p_projected_z == 0.0:
            self.dest_X = 0.0
            self.dest_Z = 0.0
        else:
            self.dest_X = self.bottom_p_projected_x + self.k * (self.bottom_p_projected_x - self.back_p_projected_x) / abs(self.bottom_p_projected_z - self.back_p_projected_z)
            self.dest_Z = self.bottom_p_projected_z + self.k * (self.bottom_p_projected_z - self.back_p_projected_z) / abs(self.bottom_p_projected_z - self.back_p_projected_z)

        print "destination", self.dest_X, self.dest_Z

    def AngleToGO(self):
        if self.dest_X == 0:
            angle_1 = 90.0
        else:
            angle_1 = math.degrees(math.atan(self.dest_Z / self.dest_X))

        if angle_1 < 0:
            angle_1 = angle_1 + 180.0
        self.angle_go =  angle_1 - 90.0
        print "AngleToGO", self.angle_go

    def SpeedTOGo(self):
        if abs(self.angle_turn) > 30:
            self.linear_speed = 0.0
        else:
            self.linear_speed = self.basic_speed

        print "SpeedToGO", self.linear_speed

    def direction(self, angle_1, angle_2):
        # if self.dest_Z <= 0.1:
        #     self.rotate_speed = (90 - self.angle_1) * 25
        # else:
        self.rotate_speed = (angle_1*0.4 + angle_2) * 35.0 * (0.5 + self.dest_Z * 0.6)
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
        if direction >= 1500:
            direction = 1500
        elif direction <= -1500:
            direction = -1500
        print "          ----> DAC0", (2500 + speed), "    DAC1: ", 2500 + direction
        self.adda.SET_DAC0(2500 + int(speed), self.adda.data_format.voltage)
        self.adda.SET_DAC1(2500 + int(direction), self.adda.data_format.voltage)

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
        rospy.init_node('docking', anonymous=True)

        while not rospy.is_shutdown():

            rospy.Subscriber('/centroid_bottom', PointCloud2, self.callback_pointcloud1)
            rospy.Subscriber('/centroid_back', PointCloud2, self.callback_pointcloud2)
            self.project(self.bottom_p_x, self.bottom_p_y, self.bottom_p_z, self.back_p_x, self.back_p_y, self.back_p_z)
            self.setDestination()

            while self.dest_Z > self.threshold_2:

                if self.dest_Z <= 0.4:
                    self.angle_turn = 0.0
                    self.AngleToGO()
                    self.direction(self.angle_turn, self.angle_go)
                elif self.dest_Z <= 0.35:
                    self.angle_turn = 0.0
                    self.dest_X = 0.0
                    self.rotate_speed = 0.0
                else:
                    self.AngleToTurn()
                    self.AngleToGO()
                    self.direction(self.angle_turn, self.angle_go)

                # self.AngleToTurn()
                # self.AngleToGO()
                # self.direction(self.angle_turn, self.angle_go)

                self.SpeedTOGo()
                self.read_update(self.linear_speed, self.rotate_speed)
                self.move_average()
                self.setMov(self.linear_speed, self.rotate_speed)

                rospy.Subscriber('/centroid_bottom', PointCloud2, self.callback_pointcloud1)
                rospy.Subscriber('/centroid_back', PointCloud2, self.callback_pointcloud2)
                self.project(self.bottom_p_x, self.bottom_p_y, self.bottom_p_z, self.back_p_x, self.back_p_y,
                             self.back_p_z)
                self.setDestination()

                self.threshold_1 = 0.05
                self.threshold_2 = 0.3

                rospy.sleep(0.2)

            self.setMov(0, 0)
            rospy.sleep(1)
            # rospy.spin()


a = chen()
a.main()
# while not rospy.is_shutdown():
#     a.main()

# rospy.on_shutdown(a.main())

# try:
#     while True:
#         a.main()
#
# except KeyboardInterrupt:
#     pass
