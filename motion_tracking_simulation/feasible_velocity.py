# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-25 14:49:16
# @Last Modified by:   chenyang
# @Last Modified time: 2020-01-07 00:26:23

import matplotlib.pyplot as plt
import numpy as np

DISTANCE = 0.62

v_l_min = -3
v_l_max = 6
v_r_min = -3
v_r_max = 6

v = np.linspace(v_r_min, v_r_max, 100)

w0 = -2/DISTANCE * (v - v_r_min)
w1 = -2/DISTANCE * (v - v_r_max)
w2 = 2/DISTANCE * (v - v_l_min)
w3 = 2/DISTANCE * (v - v_l_max)

plt.figure('V-W')
plt.plot(v, w0)
plt.plot(v, w1)
plt.plot(v, w2)
plt.plot(v, w3)
# plt.plot([chair_bottom_x, i[0]],[chair_bottom_y,i[1]], color ='gray', linewidth=1.5, linestyle="--")
# plt.plot([chair_bottom_x, i[0]],[chair_bottom_y,i[1]], color ='gray', linewidth=1.5, linestyle="--")
plt.xlabel("V")
plt.ylabel("W")

plt.show()
