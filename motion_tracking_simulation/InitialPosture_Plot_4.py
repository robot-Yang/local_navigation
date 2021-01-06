# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-10 22:40:46
# @Last Modified by:   chenyang
# @Last Modified time: 2020-12-25 23:37:55

'''
visualize all initial states in 2D/3D space
'''

import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import random
import csv
import sympy as sp

chair_width = 0.5
chair_length = 0.5

Chair = (0, 0, np.pi/2) # this is the location of attractor
StartPoint = []
alpha_bar = 40


k4 = 2
k5 = 0.5
samRho = 10 # sampling number/step of rho
samPhi = 5 # sampling number/step of phi
samAlpha = 5 # sampling number/step of alpha

Rhoo = []
Alphaa = []
Phii = []
StartPoint = []

def chair_info(chair):
    x_goal = chair[0] # attractor
    y_goal = chair[1]
    theta_goal = chair[2]
    chair_bottom_x = x_goal + d * np.cos(theta_goal) # objective
    chair_bottom_y = y_goal + d * np.sin(theta_goal)
    F_x_chair = chair_bottom_x - chair_length/2 * np.cos(theta_goal)
    F_y_chair = chair_bottom_y - chair_length/2 * np.sin(theta_goal)
    F_L_x_chair = F_x_chair + chair_width / 2 * np.cos(theta_goal + np.pi/2)
    F_L_y_chair = F_y_chair + chair_width / 2 * np.sin(theta_goal + np.pi/2)
    F_R_x_chair = F_x_chair + chair_width / 2 * np.cos(theta_goal - np.pi/2)
    F_R_y_chair = F_y_chair + chair_width / 2 * np.sin(theta_goal - np.pi/2)
    B_x_chair = chair_bottom_x + chair_length/2 * np.cos(theta_goal)
    B_y_chair = chair_bottom_y + chair_length/2 * np.sin(theta_goal)
    B_L_x_chair = B_x_chair + chair_width / 2 * np.cos(theta_goal + np.pi/2)
    B_L_y_chair = B_y_chair + chair_width / 2 * np.sin(theta_goal + np.pi/2)
    B_R_x_chair = B_x_chair + chair_width / 2 * np.cos(theta_goal - np.pi/2)
    B_R_y_chair = B_y_chair + chair_width / 2 * np.sin(theta_goal - np.pi/2)
    chair_back_x = F_x_chair + chair_length * np.cos(theta_goal)
    chair_back_y = F_y_chair + chair_length  * np.sin(theta_goal)
    plt.plot([F_L_x_chair, F_R_x_chair], [F_L_y_chair, F_R_y_chair], 'k-')
    plt.plot([B_L_x_chair, B_R_x_chair], [B_L_y_chair, B_R_y_chair], 'k-')
    plt.plot([F_L_x_chair, B_L_x_chair], [F_L_y_chair, B_L_y_chair], 'k-')
    plt.plot([F_R_x_chair, B_R_x_chair], [F_R_y_chair, B_R_y_chair], 'k-')
    return F_L_x_chair, F_L_y_chair, F_R_x_chair, F_R_y_chair, B_L_x_chair, B_L_y_chair, B_R_x_chair, B_R_y_chair

# load initial state points from store csv file, which satisfy no violence of FOV and convergence.
def load_initializePoint(Rhooo,Alphaaa,Phiii):
    global Rhoo
    global Alphaa
    global Phii
    with open('simulation_result_ex.csv', encoding = 'gbk', errors='ignore') as f:
        f_csv = csv.reader(f)
        f_csv = list(f_csv)
        Rhoo = f_csv[Rhooo]
        Alphaa = f_csv[Alphaaa]
        Phii = f_csv[Phiii]  
        Rhoo = [float(i) for i in Rhoo]  
        Alphaa = [float(i) for i in Alphaa]  
        Phii = [float(i) for i in Phii]  
    print(len(Rhoo))
    return Rhoo,Alphaa,Phii

# initialize points by a defined inequalities.
def initializePoint():
    for rho in np.linspace(0, 1.5, samRho):
        phi_max = rho**2 / k4**3
        for phi in np.linspace(-phi_max, phi_max, samPhi):
            alpha_max = (1- abs(phi) / phi_max) * (alpha_bar*np.pi/180) * k5 * rho
            # alpha_max = (1- abs(phi) / (rho**3 / k4**2)) * (alpha_bar*np.pi/180)
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
    chair_info(Chair)
    plt.scatter(chair_center_x, chair_center_y, s=60, c='r', marker="x")
    plt.arrow(x_goal, y_goal, 0.05*np.cos(theta_goal),
              0.05*np.sin(theta_goal), color='g', width=0.020)
    plt.scatter(x_goal, y_goal, s=60, c='k', marker=".", zorder=30) 
    if color == 'black':
        plt.quiver(x_start, y_start, np.cos(theta_start), np.sin(theta_start), color = 'k', scale =35, width=0.003)
    else:
        plt.quiver(x_start, y_start, np.cos(theta_start), np.sin(theta_start), color = 'r', scale =35)
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

def plot_initializePoint(color):
    initializePoint()
    transform()
    x_start = StartPoint[0]
    y_start = StartPoint[1]
    theta_start = StartPoint[2]
    TwoDspace(x_start,y_start,theta_start,color)
    ThreeDspace(color)

def calculateVDot():
    k1,k2,k3 = 0.15, 0.6, 0.82
    alphaBar = 40
    # rho, alpha, phi = sp.symbols("rho alpha phi")
    # # rho = sp.MatrixSymbol('rho', len(Rhoo),0)
    # # alpha = sp.MatrixSymbol('alpha', len(Rhoo),0)
    # # phi = sp.MatrixSymbol('phi', len(Rhoo),0)
    # # rho = sp.symarray('rho', len(Rhoo))
    # # alpha = sp.symarray('alpha', len(Rhoo))
    # # phi = sp.symarray('phi', len(Rhoo))
    # alphaStar = alpha + phi - np.pi/2 + sp.atan2(d + rho*sp.cos(phi) + l*sp.sin(alpha - np.pi/2 + phi), rho*sp.sin(phi) - l*sp.cos(alpha - np.pi/2 + phi))

    # v = k1*(rho)*sp.cos(alpha);
    # w = k2*sp.sin(alpha)*sp.cos(alpha) - k3*phi*(sp.sin(alphaBar*np.pi/180)**2 - sp.sin(alphaStar)**2);

    # rhoDot = -v*sp.cos(alpha);
    # alphaDot = v/rho*sp.sin(alpha) - w;
    # phiDot = - v/rho*sp.sin(alpha);

    # # Lyapunov function
    # V1 = 1/2*rho**2;
    # V2 = 1/2*sp.sin(alpha)**2;
    # V3 = 1/2*phi**2;

    # V1_Dot = sp.diff(V1,rho) * rhoDot;
    # V2_Dot = sp.diff(V2,alpha) * alphaDot;
    # V3_Dot = sp.diff(V3,phi) * phiDot;
    # V_Dot = V1_Dot + V2_Dot + V3_Dot;
    # V_Dot = V_Dot.subs([(rho, Rhoo),(alpha, Alphaa),(phi, Phii)])

    # V_Dot = -np.cos(Alphaa)*(k2*(np.cos(Alphaa) - np.cos(Alphaa)**3) + k1*Phii*np.sin(Alphaa) + k1*np.cos(Alphaa)*(np.cos(Alphaa)**2 - 1) + k1*Rhoo**2*np.cos(Alphaa) + k3*Phii*np.cos(Alphaa + Phii + np.arctan2(d - l*np.cos(Alphaa + Phii) + Rhoo*np.cos(Phii), Rhoo*np.sin(Phii) - l*np.sin(Alphaa + Phii)))**2*np.sin(Alphaa) - k3*Phii*np.sin((np.pi*alphaBar)/180)**2*np.sin(Alphaa))
    V_Dot = []
    for i in range(len(Rhoo)):
        rho = Rhoo[i]
        alpha = Alphaa[i]
        phi = Phii[i]
        V_dot = -0.15*phi*np.sin(alpha)*np.cos(alpha) - 0.15*rho**2*np.cos(alpha)**2 + 1.0*(0.82*phi*(0.413175911166535 - np.sin(alpha + phi + np.arctan2(rho*np.cos(phi) + 0.1*np.sin(alpha + phi - 1.5707963267949) + 0.7, rho*np.sin(phi) - 0.1*np.cos(alpha + phi - 1.5707963267949)) - 1.5707963267949)**2) - 0.45*np.sin(alpha)*np.cos(alpha))*np.sin(alpha)*np.cos(alpha) 
        V_Dot.append(V_dot)
    # V_Dot = -0.15*Phii*np.sin(Alphaa)*np.cos(Alphaa) - 0.15*Rhoo**2*np.cos(Alphaa)**2 + 1.0*(0.82*Phii*(0.413175911166535 - np.sin(Alphaa + Phii + atan2(Rhoo*np.cos(Phii) + 0.1*np.sin(Alphaa + Phii - 1.5707963267949) + 0.7, Rhoo*np.sin(Phii) - 0.1*np.cos(Alphaa + Phii - 1.5707963267949)) - 1.5707963267949)**2) - 0.45*np.sin(Alphaa)*np.cos(Alphaa))*np.sin(Alphaa)*np.cos(Alphaa)
    

    # print(V_Dot)
    print('V_Dot type=', type(V_Dot))
    print('V_Dot size=', len(V_Dot))

    max_VDot = max(V_Dot)
    print ('max_VDot =', max_VDot)

l = 0.26
d = 0.9
x_goal, y_goal, theta_goal = 0,0,np.pi/2
chair_center_x, chair_center_y = 0, d

if __name__ == '__main__':
    fig = plt.figure('3D space')
    ax = Axes3D(fig)
    # plot_initializePoint('black')
    # plot_from_simulation(0,1,2,'black') # left ones
    plot_from_simulation(5,6,7,'red') # deleted ones
    StartPoint = []
    # plot_from_simulation(5,6,7,'red') # deleted ones
    plot_from_simulation(0,1,2,'black') # left ones
    calculateVDot()

plt.show()



