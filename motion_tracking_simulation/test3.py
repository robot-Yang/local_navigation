import numpy as np
# L1 = []
# L2 = [20, 30, 40]
# L1.extend(L2)
# print(L1)

# Alphaa = []
# Alpha = np.linspace(-1, 1, 5)
# print (type(Alpha))
# Alpha = Alpha.tolist()
# # print ('Alpha=', Alpha)
# print (type(Alpha))
# # Alpha = [2,3]

# print('Alphaa=', Alphaa)
# # Alphaa.extend(Alpha)
# Alphaa = Alphaa + Alpha
# print('Alphaa=', Alphaa)
# 
# l = [[2, 3], [4, 2], [3, 2]]
# l = np.transpose(l)
# print(l)
# print(l[1][:])
# 
# 
# import matplotlib.pyplot as plt
# import numpy as np

# X = np.arange(-10, 10, 1)
# Y = np.arange(-10, 10, 1)
# U, V = np.meshgrid(X, Y)

# # fig, ax = plt.subplots()
# # q = plt.quiver(X, Y, U, V)
# q = plt.quiver(0, 0, -1, 1)
# plt.quiverkey(q, X=0.3, Y=1.1, U=10,
#              label='Quiver key, length = 10', labelpos='E')

# plt.show()

# lang = ["Python", "C++", "Java", "PHP", "Ruby", "MATLAB"]
# #使用正数索引
# # deleteList = 2,3
# # del lang[deleteList]
# lang.pop([2,3])
# print(lang)
# #使用负数索引
# del lang[-2]
# print(lang)
# 
import sys
sys.path.append('/usr/local/lib/python3.7/site-packages')
# import sympy 
from sympy import *
  
x, y = symbols('x y') 
exp = x**2 + 1
print("Before Substitution : {}".format(exp))  
    
# Use sympy.subs() method 
res_exp = exp.subs(x, 2)  
print(res_exp)  
print("After Substitution : {}".format(res_exp))  