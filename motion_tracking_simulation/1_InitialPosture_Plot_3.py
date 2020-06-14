# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-06-11 22:02:31

# visualize all initial states in 2D/3D space

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import random
import csv

chair_width = 0.5
chair_length = 0.5
safe_distance = 0.45 # distanc between attractor and chair's front edge

Chair = (0, 0, np.pi/2) # this is the location of attractor
StartPoint = []
alpha_bar = 40


k4 = 1.5
samRho = 20 # sampling number/step of rho
samPhi = 20 # sampling number/step of phi
samAlpha = 20 # sampling number/step of alpha

Rhoo = []
Alphaa = []
Phii = []
StartPoint = []

# load initial state points from store csv file, which satisfy no violence of FOV and convergence.
def load_initializePoint(Rhooo,Alphaaa,Phiii):
    global Rhoo
    global Alphaa
    global Phii
    with open('simulation_result_1.csv', encoding = 'gbk', errors='ignore') as f:
        f_csv = csv.reader(f)
        f_csv = list(f_csv)
        Rhoo = f_csv[Rhooo]
        Alphaa = f_csv[Alphaaa]
        Phii = f_csv[Phiii]  
        Rhoo = [float(i) for i in Rhoo]  
        Alphaa = [float(i) for i in Alphaa]  
        Phii = [float(i) for i in Phii]  
    print(len(Rhoo))

# initialize points by a defined inequalities.
def initializePoint():
    for rho in np.linspace(0, 1.5, samRho):
        phi_max = rho**2 / k4**2
        for phi in np.linspace(-phi_max, phi_max, samPhi):
            alpha_max = (1- abs(phi) / phi_max) * (alpha_bar*np.pi/180)
            Alpha = np.linspace(-alpha_max, alpha_max, samAlpha)
            Alpha = Alpha.tolist()

            conRho = [rho] * samAlpha
            conPhi = [phi] * samAlpha
            global Rhoo
            global Alphaa
            global Phii
            Rhoo = Rhoo + conRho
            Phii = Phii + conPhi
            Alphaa.extend(Alpha)

# tranform (rho, alpha, phi) into (x,y,theta)
def transform():
    global StartPoint
    for i in range(len(Rhoo)):
        startPoint_x = - Rhoo[i] * np.sin(Phii[i])
        startPoint_y = - Rhoo[i] * np.cos(Phii[i])
        feasiblePosture = np.pi/2 - Alphaa[i] - Phii[i]
        startPoint = (startPoint_x, startPoint_y, feasiblePosture)
        StartPoint.append(startPoint)
    StartPoint = np.transpose(StartPoint)

#  plot points in 2D space: (x,y,theta)
def TwoDspace(x_start,y_start,theta_start,color):
    plt.figure('2D space')
    ax = plt.gca()
    ax.set_aspect(1)
    plt.scatter(chair_center_x, chair_center_y, s=60, c='r', marker="x")
    plt.arrow(x_goal, y_goal, 0.05*np.cos(theta_goal),
              0.05*np.sin(theta_goal), color='g', width=0.015)
    plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) 
    if color == 'black':
        plt.quiver(x_start, y_start, np.cos(theta_start), np.sin(theta_start), color = 'k', scale =50)
    else:
        plt.quiver(x_start, y_start, np.cos(theta_start), np.sin(theta_start), color = 'r', scale =50)
    # plt.scatter(x_start, y_start, s=60, c='k', marker=".", zorder=30)
    plt.xlim(-2, 2)
    plt.ylim(-2.5, 1)
    plt.xticks(fontsize=16) 
    plt.yticks(fontsize=16) 
    plt.xlabel(r'$x$''[meter]', fontsize=16)
    plt.ylabel(r'$y$''[meter]', fontsize=16)
    plt.axis('equal')
    plt.tight_layout()

#  plot points in 3D space: (rho, alpha, phi)
def ThreeDspace(color):
    if color == 'black':
        ax.scatter(Rhoo, Alphaa, Phii, c='k', marker=".")
    else:
        ax.scatter(Rhoo, Alphaa, Phii, c='r', marker=".")
    ax.set_xlabel(r'$\rho$', fontsize=16)
    ax.set_ylabel(r'$\alpha$', fontsize=16)
    ax.set_zlabel(r'$\phi$', fontsize=16)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=10)

def plot_from_simulation(Rhooo, Alphaaa, Phiii, color):
    load_initializePoint(Rhooo, Alphaaa, Phiii)
    transform()
    x_start = StartPoint[0]
    y_start = StartPoint[1]
    theta_start = StartPoint[2]
    TwoDspace(x_start,y_start,theta_start,color)
    ThreeDspace(color)

# plot using data form initialized
def plot_initializePoint(color):
    initializePoint()
    transform()
    x_start = StartPoint[0]
    y_start = StartPoint[1]
    theta_start = StartPoint[2]
    TwoDspace(x_start,y_start,theta_start,color)
    ThreeDspace(color)

x_goal, y_goal, theta_goal = 0,0,np.pi/2
chair_center_x, chair_center_y = 0,0.7 

if __name__ == '__main__':
    fig = plt.figure('3D space')
    ax = Axes3D(fig)
    plot_initializePoint('black')
    # plot_from_simulation(0,1,2,'black') # left ones
    StartPoint = []
    # plot_from_simulation(5,6,7,'red') # deleted ones

plt.show()



