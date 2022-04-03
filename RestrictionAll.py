#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import itertools
import operator


class Restricao:

	def __init__(self):
		self.node_id = []
		self.lambda_id = []
		self.split_id= []
		self.State = []
		self.Node_Capacity = [40000, 20000, 20000]
		self.ecpri_split = [1966, 74, 119, 675] #largura de banda demandada por split

	def energy(self, total_traffic_cloud, total_traffic_fog, traffic_fog1, traffic_fog2, traffic_wavelength, sol):
		#print(i)		
		self.node_id = sol[0]
		self.lambda_id = sol[1]
		self.split_id = sol[2]
		cost1 = 0
		cost2 = 0
		cost3 = 0

		####################################################### RESTRIÇÃO SPLIT ==============================================
		if self.split_id.count(1) == 1:
			cost3 += 0
		if self.split_id.count(1) == 2:
			cost3 += 10000
		if self.split_id.count(1) == 3:
			cost3 += 20000
		if self.split_id.count(1) == 4:
			cost3 += 30000
		if self.split_id.count(1) == 0:
			cost3 += 40000
  		
		if total_traffic_cloud+1966<=37000:
			if self.split_id[0]==1:
				cost3+=0
			if self.split_id[1]==1:
				cost3+=100
			if self.split_id[2]==1:
				cost3+=99
			if self.split_id[3]==1:
				cost3+=98
    
			if self.node_id[0]==1:
				cost1+=0
			if self.node_id[1]==1:
				cost1+=97
			if self.node_id[2]==1:
				cost1+=96
    
			for i in range(4,8):
				if self.lambda_id[i] == 1:
					cost2+=95

			traffic = 1966
			if self.lambda_id[0] == 1:
				if traffic_wavelength[0] >= 10000:
					cost2+=94
				elif traffic_wavelength[0] + traffic < 10000:
					traffic_wavelength[0] += traffic
					traffic = 0
				else:
					traffic = (10000 - traffic_wavelength[0])
					traffic_wavelength[0] = 10000
			elif traffic_wavelength[0] < 10000:
				cost2+=94
    
			if self.lambda_id[1] == 1 and traffic != 0:
				if traffic_wavelength[1] >= 10000:
					cost2+=93
				elif traffic_wavelength[1] + traffic < 10000:
					traffic_wavelength[1] += traffic
					traffic = 0
				else:
					traffic = (10000 - traffic_wavelength[1])
					traffic_wavelength[1] = 10000
			elif (traffic > 0 and traffic_wavelength[1] < 10000) or (self.lambda_id[1] == 1 and traffic == 0):
				cost2+=93

			if self.lambda_id[2] == 1 and traffic != 0:
				if traffic_wavelength[2] >= 10000:
					cost2+=92
				elif traffic_wavelength[2] + traffic < 10000:
					traffic_wavelength[2] += traffic
					traffic = 0
				else:
					traffic = (10000 - traffic_wavelength[2])
					traffic_wavelength[2] = 10000
			elif (traffic > 0 and traffic_wavelength[2] < 10000) or (self.lambda_id[2] == 1 and traffic == 0):
				cost2+=92
    
			if self.lambda_id[3] == 1 and traffic != 0:
				traffic_wavelength[3] += traffic
				traffic = 0
				if traffic_wavelength[3] > 10000:
					cost2 += 91
			elif (traffic > 0 and traffic_wavelength[3] < 10000) or (self.lambda_id[3] == 1 and traffic == 0):
				cost2+=91

			if traffic > 0:
				cost2+=90
   
			total_traffic_cloud += 1966
		else:
			for i in range(0,3):
				if self.lambda_id[i] == 1:
					cost2+=80
      
			# Split 1
			if self.split_id[0]==1:
				cost3+=79

			if total_traffic_cloud + 674.4 <= 40000:
				total_traffic_cloud += 674.4
				total_traffic_fog += 1291.6
				
				if self.split_id[1] != 1:
					cost3 += 78
				if self.split_id[2] == 1:
					cost3 += 77
				if self.split_id[3] == 1:
					cost3 += 76
     
				total_traffic = 1291.6
				traffic1 = 0
				traffic2 = 0
    
				if self.node_id[0] == 0:
					cost1 += 75
				if self.lambda_id[3] == 0:
					cost2 += 74
				else:
					traffic_wavelength[3] += 674.4
					if traffic_wavelength[3] > 10000:
						cost2 += 73

				if traffic_fog1 < 20000:
					if self.node_id[1] != 1:
						cost1+=72
					if traffic_fog1 + total_traffic < 20000:
						traffic_fog1 += total_traffic
						traffic1 = total_traffic
						traffic2 = 0
						total_traffic = 0
					else:
						total_traffic -= (20000 - traffic_fog1)
						traffic1 = (20000 - traffic_fog1)
						traffic2 = total_traffic
						traffic_fog1 = 20000
				elif self.node_id[1] == 1:
					cost1+=72				

				if total_traffic > 0:
					if self.node_id[2] != 1:
						cost1+=71
					traffic_fog2 += total_traffic
					traffic2 = total_traffic
				elif self.node_id[2]==1:
					cost1+=71

				if traffic_fog1 < 20000:
					if traffic_wavelength[4] < 10000:
						if self.lambda_id[4] != 1:
							cost2+=70
						if traffic_wavelength[4] + traffic1 < 10000:
							traffic_wavelength[4] += traffic1
							traffic1 = 0
						else:
							traffic1 = (10000 - traffic_wavelength[4])
							traffic_wavelength[4] = 10000
					elif self.lambda_id[4] == 1:
						cost2+=70
		
					if traffic1 > 0:
						if self.lambda_id[5] != 1:
							cost2+=69
						traffic_wavelength[5] += traffic1
						traffic1 = 0
						if traffic_wavelength[5] > 10000:
							cost+= 69
					elif self.lambda_id[5] == 1:
						cost2+=69
				else:
					if self.lambda_id[4] == 1 or self.lambda_id[5] == 1:
						cost2+=68

				if traffic2 > 0:
					if traffic_wavelength[6] < 10000:
						if self.lambda_id[6] != 1:
							cost2+=67
						if traffic_wavelength[6] + traffic2 < 10000:
							traffic_wavelength[6] += traffic2
							traffic2 = 0
						else:
							traffic2 = (10000 - traffic_wavelength[6])
							traffic_wavelength[6] = 10000
					elif self.lambda_id[6] == 1:
						cost2+=67
		
					if traffic2 > 0:
						if self.lambda_id[7] != 1:
							cost2+=66
						traffic_wavelength[7] += traffic2
						traffic2 = 0
						if traffic_wavelength[7] > 10000:
							cost+= 69
					elif self.lambda_id[7] == 1:
						cost2+=66
				else:
					if self.lambda_id[6] == 1 or self.lambda_id[7] == 1:
						cost2+=65
     
     
     
			elif total_traffic_cloud + 119 <= 40000:
				total_traffic_cloud += 119
				total_traffic_fog += 1847
				
				if self.split_id[1] == 1:
					cost3 += 78
				if self.split_id[2] != 1:
					cost3 += 77
				if self.split_id[3] == 1:
					cost3 += 76
     
				total_traffic = 1847
				traffic1 = 0
				traffic2 = 0
    
				if self.node_id[0] == 0:
					cost1 += 75
				if self.lambda_id[3] == 0:
					cost2 += 74
				else:
					traffic_wavelength[3] += 119
					if traffic_wavelength[3] > 10000:
						cost2 += 73

				if traffic_fog1 < 20000:
					if self.node_id[1] != 1:
						cost1+=72
					if traffic_fog1 + total_traffic < 20000:
						traffic_fog1 += total_traffic
						traffic1 = total_traffic
						traffic2 = 0
						total_traffic = 0
					else:
						total_traffic -= (20000 - traffic_fog1)
						traffic1 = (20000 - traffic_fog1)
						traffic2 = total_traffic
						traffic_fog1 = 20000
				elif self.node_id[1] == 1:
					cost1+=72				

				if total_traffic > 0:
					if self.node_id[2] != 1:
						cost1+=71
					traffic_fog2 += total_traffic
					traffic2 = total_traffic
				elif self.node_id[2]==1:
					cost1+=71

				if traffic_fog1 < 20000:
					if traffic_wavelength[4] < 10000:
						if self.lambda_id[4] != 1:
							cost2+=70
						if traffic_wavelength[4] + traffic1 < 10000:
							traffic_wavelength[4] += traffic1
							traffic1 = 0
						else:
							traffic1 = (10000 - traffic_wavelength[4])
							traffic_wavelength[4] = 10000
					elif self.lambda_id[4] == 1:
						cost2+=70
		
					if traffic1 > 0:
						if self.lambda_id[5] != 1:
							cost2+=69
						traffic_wavelength[5] += traffic1
						traffic1 = 0
						if traffic_wavelength[5] > 10000:
							cost+= 69
					elif self.lambda_id[5] == 1:
						cost2+=69
				else:
					if self.lambda_id[4] == 1 or self.lambda_id[5] == 1:
						cost2+=68

				if traffic2 > 0:
					if traffic_wavelength[6] < 10000:
						if self.lambda_id[6] != 1:
							cost2+=67
						if traffic_wavelength[6] + traffic2 < 10000:
							traffic_wavelength[6] += traffic2
							traffic2 = 0
						else:
							traffic2 = (10000 - traffic_wavelength[6])
							traffic_wavelength[6] = 10000
					elif self.lambda_id[6] == 1:
						cost2+=67
		
					if traffic2 > 0:
						if self.lambda_id[7] != 1:
							cost2+=66
						traffic_wavelength[7] += traffic2
						traffic2 = 0
						if traffic_wavelength[7] > 10000:
							cost+= 66
					elif self.lambda_id[7] == 1:
						cost2+=66
				else:
					if self.lambda_id[6] == 1 or self.lambda_id[7] == 1:
						cost2+=65

			else:
				total_traffic_cloud += 0
				total_traffic_fog += 1966
				
				if self.split_id[1] == 1:
					cost3 += 78
				if self.split_id[2] == 1:
					cost3 += 77
				if self.split_id[3] != 1:
					cost3 += 76
     
				total_traffic = 1966
				traffic1 = 0
				traffic2 = 0
    
				if self.node_id[0] != 0:
					cost1 += 75
				if self.lambda_id[3] != 0:
					cost2 += 74

				if traffic_fog1 < 20000:
					if self.node_id[1] != 1:
						cost1+=72
					if traffic_fog1 + total_traffic < 20000:
						traffic_fog1 += total_traffic
						traffic1 = total_traffic
						traffic2 = 0
						total_traffic = 0
					else:
						total_traffic -= (20000 - traffic_fog1)
						traffic1 = (20000 - traffic_fog1)
						traffic2 = total_traffic
						traffic_fog1 = 20000
				elif self.node_id[1] == 1:
					cost1+=72				

				if total_traffic > 0:
					if self.node_id[2] != 1:
						cost1+=71
					traffic_fog2 += total_traffic
					traffic2 = total_traffic
				elif self.node_id[2]==1:
					cost1+=71

				if traffic_fog1 < 20000:
					if traffic_wavelength[4] < 10000:
						if self.lambda_id[4] != 1:
							cost2+=70
						if traffic_wavelength[4] + traffic1 < 10000:
							traffic_wavelength[4] += traffic1
							traffic1 = 0
						else:
							traffic1 = (10000 - traffic_wavelength[4])
							traffic_wavelength[4] = 10000
					elif self.lambda_id[4] == 1:
						cost2+=70
		
					if traffic1 > 0:
						if self.lambda_id[5] != 1:
							cost2+=69
						traffic_wavelength[5] += traffic1
						traffic1 = 0
						if traffic_wavelength[5] > 10000:
							cost+= 69
					elif self.lambda_id[5] == 1:
						cost2+=69
				else:
					if self.lambda_id[4] == 1 or self.lambda_id[5] == 1:
						cost2+=68

				if traffic2 > 0:
					if traffic_wavelength[6] < 10000:
						if self.lambda_id[6] != 1:
							cost2+=67
						if traffic_wavelength[6] + traffic2 < 10000:
							traffic_wavelength[6] += traffic2
							traffic2 = 0
						else:
							traffic2 = (10000 - traffic_wavelength[6])
							traffic_wavelength[6] = 10000
					elif self.lambda_id[6] == 1:
						cost2+=67
		
					if traffic2 > 0:
						if self.lambda_id[7] != 1:
							cost2+=66
						traffic_wavelength[7] += traffic2
						traffic2 = 0
						if traffic_wavelength[7] > 10000:
							cost+= 66
					elif self.lambda_id[7] == 1:
						cost2+=66
				else:
					if self.lambda_id[6] == 1 or self.lambda_id[7] == 1:
						cost2+=66

		return [cost1, cost2, cost3], total_traffic_cloud, total_traffic_fog, traffic_fog1, traffic_fog2, traffic_wavelength


		"""
  Split 0: 1966  to cloud and 0 to fog; Split 3: 74 to cloud and (1966-74) to fog,; Split 2: 119 to cloud and (1966 - 119); Split 1: 674.4 to cloud and (1966-674.4 ) to fog
  
  
		"""
  # [1,2,3,  4,5,6,7,8,9,10,11,  12,13,14,15]
  # [1,0,0   1,0,0,0,0,0,0,0   1,0,0,0]
  # [1,1,0   1,0,1,0,0,0,0,0   0,1,0,0]

"""
40000 = 38034
  	1 - 10000 - 1966 = 8034
	2 - 10000 - 1966 = 8034
	3 - 10000
	4 - 10000

40000
"""
	######################################################### Parâmetros para Teste ###############################################################

#ww = [1,0,1,1,1,0,0,0,0,1,1,0,0,0,1,1,0,1,1,1,0,0,0,0,1,1,0,1,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,1,0,0,1,1,1,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1]# 
ww = [[[1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [1, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 1, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 1, 1, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 1, 0, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 0, 0, 0], [0, 0, 1, 0]], [[1, 1, 0], [0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 0]], [[1, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 1, 0]], [[1, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0], [0, 0, 1, 0]], [[0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1]], [[0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0], [0, 0, 0, 1]], [[0, 1, 1], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1]], [[0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 1]]]
print(len(ww))
if __name__ == "__main__":
	test = Restricao()
	total_traffic_cloud = 0
	total_traffic_fog = 0
	traffic_fog1 = 0
	traffic_fog2 = 0
	traffic_wavelength = [0, 0, 0, 0, 0, 0, 0, 0]
 
	for i in range(len(ww)):
		e,total_traffic_cloud,total_traffic_fog, traffic_fog1, traffic_fog2, traffic_wavelength = test.energy(total_traffic_cloud,total_traffic_fog,traffic_fog1, traffic_fog2,traffic_wavelength, ww[i])
		print(i, e,total_traffic_cloud,total_traffic_fog, traffic_fog1, traffic_fog2, ww[i])
	# tc = 0
	# tf = 0
	# for i in range(len(ww)):
	# 	e,tc,tf = test.energy(tc,tf,ww[i])
	# 	print(i, e,tc,tf)



