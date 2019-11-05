# -*- coding: utf-8 -*-
# @Author: Yang Chen
# @Date:   2019-10-14 18:06:49
# @Last Modified by:   chenyang
# @Last Modified time: 2019-10-15 10:39:59

import sympy
import numpy as np

l = 0.1
d = 0.2

rho, alpha, beta, alphaStar, v, w, rhoDot, alphaDot, betaDot = sympy.symbols("rho, alpha, beta, alphaStar, v, w, rhoDot, alphaDot, betaDot")

alphaStar = np.arcsin(d*np.sin(beta)/(d**2 + rho**2 + 2*d*rho*np.cos(beta)))

v = k1*rho*np.cos(alpha)
w = k2*np.sin(alpha)*np.cos(alphaStar)

rhoDot = -v*np.cos(alpha) - w*l*np.sin(alpha)
alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1)
betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha))

funcs = sympy.Matrix([rhoDot, alphaDot, betaDot])
args = sympy.Matrix([rho, alpha, beta])
res = funcs.jacobian(args)
