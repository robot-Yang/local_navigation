# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-25 14:49:16
# @Last Modified by:   chenyang
# @Last Modified time: 2020-12-27 00:05:49

import matplotlib.pyplot as plt
import numpy as np

DISTANCE = 0.62

def outer_space():
	maimum = 0.3
	v_l_min = - maimum
	v_l_max = maimum
	v_r_min = - maimum
	v_r_max = maimum

	v0 = np.linspace(v_r_min, 0, 100)
	v1 = np.linspace(0, v_r_max, 100)
	v2 = np.linspace(v_r_min, 0, 100)
	v3 = np.linspace(0, v_r_max, 100)

	# w0 = -2/DISTANCE * (v0 - v_r_min)
	# w1 = -2/DISTANCE * (v1 - v_r_max)
	# w2 = 2/DISTANCE * (v2 - v_l_min)
	# w3 = 2/DISTANCE * (v3 - v_l_max)

	w0 = -2/DISTANCE * (v0 - v_r_min)*180/np.pi
	w1 = -2/DISTANCE * (v1 - v_r_max)*180/np.pi
	w2 = 2/DISTANCE * (v2 - v_l_min)*180/np.pi
	w3 = 2/DISTANCE * (v3 - v_l_max)*180/np.pi

	plt.figure('V-W')
	plt.plot(v0, w0, color ='k')
	plt.plot(v1, w1, color ='k')
	plt.plot(v2, w2, color ='k')
	plt.plot(v3, w3, color ='k')
	# plt.plot([0,0],[0,1], color ='gray', linewidth=1.5, linestyle="--")
	# plt.plot([chair_bottom_x, i[0]],[chair_bottom_y,i[1]], color ='gray', linewidth=1.5, linestyle="--")
	plt.xlabel("V")
	plt.ylabel("W")

def inner_space():
	minimum = 0.03
	v_l_min = - minimum
	v_l_max = minimum
	v_r_min = - minimum
	v_r_max = minimum

	v0 = np.linspace(v_r_min, 0, 100)
	v1 = np.linspace(0, v_r_max, 100)
	v2 = np.linspace(v_r_min, 0, 100)
	v3 = np.linspace(0, v_r_max, 100)

	# w0 = -2/DISTANCE * (v0 - v_r_min)
	# w1 = -2/DISTANCE * (v1 - v_r_max)
	# w2 = 2/DISTANCE * (v2 - v_l_min)
	# w3 = 2/DISTANCE * (v3 - v_l_max)

	w0 = -2/DISTANCE * (v0 - v_r_min)*180/np.pi
	w1 = -2/DISTANCE * (v1 - v_r_max)*180/np.pi
	w2 = 2/DISTANCE * (v2 - v_l_min)*180/np.pi
	w3 = 2/DISTANCE * (v3 - v_l_max)*180/np.pi

	plt.figure('V-W')
	plt.plot(v0, w0, color ='k')
	plt.plot(v1, w1, color ='k')
	plt.plot(v2, w2, color ='k')
	plt.plot(v3, w3, color ='k')
	# plt.plot([0,0],[0,1], color ='gray', linewidth=1.5, linestyle="--")
	# plt.plot([chair_bottom_x, i[0]],[chair_bottom_y,i[1]], color ='gray', linewidth=1.5, linestyle="--")
	plt.xlabel(r'$V$''[m/s]', fontsize=16)
	plt.ylabel(r'$W$''[degree/s]', fontsize=16)

def main():
	# outer_space()
	inner_space()
	# plt.plot([0,0],[-7.5,7.5], color ='gray', linewidth=1.5, linestyle="--")
	# plt.plot([-1.5,1.5],[0,0], color ='gray', linewidth=1.5, linestyle="--")

# main()
# plt.show()
