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
		self.node_id = sol[0:3]
		self.lambda_id = sol[3:11]
		self.split_id = sol[11:15]
		cost = 0

		####################################################### RESTRIÇÃO SPLIT ==============================================		
		#Restrição 1 - Um Split por Antena - Se mais de 1 ou não tiver pelo menos 1 -> custo alto

		if self.split_id.count(1) == 1:
			cost += 0
		if self.split_id.count(1) == 2:
			cost += 20000
		if self.split_id.count(1) == 3:
			cost += 50000
		if self.split_id.count(1) == 4:
			cost += 100000

		if self.split_id[0] == 1:
			if self.node_id[0] != 1:
				cost += 3000
			if self.node_id[1] == 1:
				cost += 1000
			if self.node_id[2] == 1:
				cost += 1000

		if self.split_id[1] == 1:
			if self.node_id[0] != 1:
				cost += 3000
			if self.node_id[1] != 1 and self.node_id[2] != 1:
				cost += 3000
		
		if self.split_id[2] == 1:
			if self.node_id[0] != 1:
				cost += 3000
			if self.node_id[1] != 1 and self.node_id[2] != 1:
				cost += 3000
    
		if self.split_id[3] == 1:
			if self.node_id[0] == 1:
				cost += 3000
			if self.node_id[1] == self.node_id[2]:
				cost += 3000
    
		if self.node_id.count(1) > self.lambda_id.count(1):
			cost += 10000

		if self.node_id[0] == 1:
			if self.lambda_id[0:4].count(1) == 0:
				cost += 10000
		
		if self.node_id[1] == 1 or self.node_id[2] == 1 or self.node_id[3] == 1:
			if self.lambda_id[4:8].count(1) == 0:
				cost += 10000
   
		if total_traffic_cloud+1966<=37000:
			if self.split_id[0]==1:
				cost+=0
			if self.split_id[1]==1:
				cost+=100
			if self.split_id[2]==1:
				cost+=500
			if self.split_id[3]==1:
				cost+=1000
    
			if self.lambda_id[0:4].count(1) == 1:
				traffic_wavelength[self.lambda_id[0:4].index(1)] += 1966
				if traffic_wavelength[self.lambda_id[0:4].index(1)] > 10000:
					cost += 20000
    
			if self.lambda_id[0:4].count(1) > 1:
				trafic = 1966
				for i in range(4):
					if trafic == 0 and self.lambda_id[i] == 1:
						cost += 20000
					elif self.lambda_id[i] == 1:
						if traffic_wavelength[i] + trafic < 10000:
							traffic_wavelength[i] += trafic
							trafic = 0
						else:
							trafic -= (10000 - traffic_wavelength[i])
							traffic_wavelength[i] = 10000

			total_traffic_cloud += 1966
		else:
			if self.split_id[0]==1:
				total_traffic_cloud += 1966
				cost+=100000

			if self.split_id[1]==1:
				total_traffic_cloud += 674.4
				total_traffic_fog += 1291.6
    
				if self.node_id[1] == 1:
					traffic_fog1 += 1291.6
				if traffic_fog1 > 20000:
					cost += 1000
     
				if self.node_id[2] == 1:
					traffic_fog2 += 1291.6
				if traffic_fog2 > 20000:
					cost += 1000

				if total_traffic_cloud > 40000 or total_traffic_fog > 40000:
					cost += 1000

				if self.lambda_id[4:8].count(1) == 1:
					traffic_wavelength[self.lambda_id[4:8].index(1)] += 1291.6
     
				if traffic_wavelength[self.lambda_id[4:8].index(1)] > 10000:
					cost += 20000
    
				if self.lambda_id[4:8].count(1) > 1:
					trafic = 1291.6
					for i in range(4,8):
						if trafic == 0 and self.lambda_id[i] == 1:
							cost += 20000
						elif self.lambda_id[i] == 1:
							if traffic_wavelength[i] + trafic < 10000:
								traffic_wavelength[i] += trafic
								trafic = 0
							else:
								trafic -= (10000 - traffic_wavelength[i])
								traffic_wavelength[i] = 10000
     

			if self.split_id[2]==1:
				total_traffic_cloud += 119
				total_traffic_fog += 1847

				if self.node_id[1] == 1:
					traffic_fog1 += 1847
				if traffic_fog1 > 20000:
					cost += 500
     
				if self.node_id[2] == 1:
					traffic_fog2 += 1847
				if traffic_fog2 > 20000:
					cost += 500
     
				if(total_traffic_cloud > 40000 or total_traffic_fog > 40000):
					cost += 500

				if self.lambda_id[4:8].count(1) == 1:
					traffic_wavelength[self.lambda_id[4:8].index(1)] += 1847
     
				if traffic_wavelength[self.lambda_id[4:8].index(1)] > 10000:
					cost += 20000
    
				if self.lambda_id[4:8].count(1) > 1:
					trafic = 1847
					for i in range(4,8):
						if trafic == 0 and self.lambda_id[i] == 1:
							cost += 20000
						elif self.lambda_id[i] == 1:
							if traffic_wavelength[i] + trafic < 10000:
								traffic_wavelength[i] += trafic
								trafic = 0
							else:
								trafic -= (10000 - traffic_wavelength[i])
								traffic_wavelength[i] = 10000
     
     
			if self.split_id[3]==1:
				total_traffic_cloud += 74
				total_traffic_fog += 1892

				if self.node_id[1] == 1:
					traffic_fog1 += 1892
				if traffic_fog1 > 20000:
					cost += 100
     
				if self.node_id[2] == 1:
					traffic_fog2 += 1892
				if traffic_fog2 > 20000:
					cost += 100
    
				if(total_traffic_cloud > 40000 or total_traffic_fog > 40000):
					cost += 100

				if self.lambda_id[4:8].count(1) == 1:
					traffic_wavelength[self.lambda_id[4:8].index(1)] += 1892
     
				if traffic_wavelength[self.lambda_id[4:8].index(1)] > 10000:
					cost += 20000
    
				if self.lambda_id[4:8].count(1) > 1:
					trafic = 1892
					for i in range(4,8):
						if trafic == 0 and self.lambda_id[i] == 1:
							cost += 20000
						elif self.lambda_id[i] == 1:
							if traffic_wavelength[i] + trafic < 10000:
								traffic_wavelength[i] += trafic
								trafic = 0
							else:
								trafic -= (10000 - traffic_wavelength[i])
								traffic_wavelength[i] = 10000
   
		return cost, total_traffic_cloud, total_traffic_fog, traffic_fog1, traffic_fog2, traffic_wavelength


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
ww = [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 1, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0, 1]]
print(len(ww))
if __name__ == "__main__":
	test = Restricao()
	tc = 0
	tf = 0
	for i in range(len(ww)):
		e,tc,tf = test.energy(tc,tf,ww[i])
		print(i, e,tc,tf)
	tc = 0
	tf = 0
	for i in range(len(ww)):
		e,tc,tf = test.energy(tc,tf,ww[i])
		print(i, e,tc,tf)




