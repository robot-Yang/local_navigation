import numpy as np
from scipy.optimize import fsolve, basinhopping
import random
# import mtp_lib1 as mtp_lib
# import mtp_lib_singleDestination as mtp_lib
import mtp_lib_chairIsPoint as mtp_lib

VALUE = []
VALUESOLUTION = []

def main():
	for i in np.linspace(0, 2, num=20):
		for j in np.linspace(1, 10, num=20):
			for k in np.linspace(1, 10, num=20):
				value = - mtp_lib.a.main(i, j, k)
				VALUE.append(value)
				VALUESOLUTION.append([i, j, k])
	# value = - mtp_lib.a.main(16.65, 3.55, 1.77)
	# VALUE.append(value)
	# VALUESOLUTION.append([16.65, 3.55, 1.77])
	# value = - mtp_lib.a.main(6,3,1)
	# VALUE.append(value)
	# VALUESOLUTION.append([6,3,1])
	optimalValue = max(VALUE)
	print ('optimalValue', optimalValue)
	optimalIndex = np.where(VALUE == optimalValue)
	print (optimalIndex[0][0])
	optimalSolution = VALUESOLUTION[optimalIndex[0][0]]
	return optimalSolution, optimalValue

solution, value = main()
# print('最优解: x1, x2')
# print(round(solution[0], 2), round(solution[1], 2))
# print('最优目标函数值:', round(value, 2))
print ("optimalValue =", round(solution[0], 2), round(solution[1], 2), round(solution[2], 2), round(value, 2))
# print (solution, value)