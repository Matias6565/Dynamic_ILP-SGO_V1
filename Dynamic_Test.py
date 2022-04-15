import simpy
import functools
import random as np
import time
from enum import Enum
import numpy
from scipy.stats import norm
import scipy as sp
import scipy.stats
import matplotlib.pyplot as plt
from SGO.SGO import SGO as plp
import copy
#import dynamic_simulator as sim # Meu é esse
import simulator as sim
import pandas as pd

# ====================
#	Lists
# ====================
#lists of blocking probabilities
simu_blocking_prob = []
#lists of power consumptions means
total_simu_power = []
total_simu_blocking_prob= []
#lists of activated nodes means
total_simu_nodes = []
#lists of activated switches means
total_simu_switches = []
#lists of activated lambdas means
total_simu_lambdas = []
#lists of redirectes RRHs means
total_simu_redir = []
#lists of blocked RRHs means
total_simu_blocked = []
#lists of solutions time means
total_simu_time = []
#lists of bandwidth usage
total_simu_lambda_usage = []
#lists of proc usage
total_simu_proc_usage = []
#lists of cloud use mean
total_simu_cloud = []
#lists of fog use mean
total_simu_fog = []
#amount of external migrations
simu_ext = []
#lists of total requested RRHs
simu_req = []
total_delay = []
avg_cpu = []

total_simu_cloud_proc = []
total_simu_fog_proc = []
total_simu_tot_proc = []
avg_simu_cloud_proc = []
avg_simu_fog_proc = []
avg_simu_tot_proc = []

avg_Block_B = []
avg_total_Block_B = []

total_delay2 = []
avg_total_delay = []
#lists of total service availability
avg_simu_availability = []
#lists of total served rrhs
simu_served = []
cpu = []
avg_total_delay2 = []


total_split_e = []
avg_total_split_e = []
total_split_i = []
avg_total_split_i = []
total_split_d = []
avg_total_split_d = []
total_split_b = []
avg_total_split_b = []
#general function to reload modules
def reloadModule(aModule):
    importlib.reload(aModule)

util = sim.Util()

exec_number = 2 #- Teoria do Limite C. >=30
#exec_number = 2
#number_of_rrhs = 5
number_of_rrhs = 4 #- Nosso cenário

for i in range(exec_number):
	b_mig = []
	print("STARTING SIMULATION")
	print("Execution # {}".format(i))
	env = simpy.Environment()
	cp = sim.Control_Plane(env, util, "batch")
	sim.rrhs = util.createRRHs(number_of_rrhs, env, sim.service_time, cp)
	np.shuffle(sim.rrhs)
	t = sim.Traffic_Generator(env, sim.distribution, sim.service_time, cp)
	print("\Begin at "+str(env.now))
	env.run(until = 86401)
	print("\End at "+str(env.now))
	print("#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|##|#|#|#|")
	print("-------------------------------------")
	print("#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|#|##|#|#|#|")
	total_simu_power.append(sim.batch_average_consumption)
	total_simu_nodes.append(sim.b_average_act_nodes)
	total_simu_lambdas.append(sim.b_average_act_lambdas)
	total_simu_time.append(sim.avg_time_b)
	#print("Tempo salvo{}".format(sim.avg_time_b))
	total_split_e.append(sim.avg_SplitE_usage)
	total_split_i.append(sim.avg_SplitI_usage)
	total_split_d.append(sim.avg_SplitD_usage)
	total_split_b.append(sim.avg_SplitB_usage)
	total_simu_lambda_usage.append(sim.avg_lambda_usage)
	avg_simu_availability.append(sim.avg_service_availability)
	#total_simu_blocked.append(sim.batch_blocking)
	total_simu_blocked.append(sim.total_batch_blocking)
	total_simu_fog_proc.append(sim.avg_Fog_proc)
	total_simu_cloud_proc.append(sim.avg_Cloud_proc)
	total_simu_tot_proc.append(sim.avg_Total_proc)
	#print(sim.avg_Cloud_proc)
	#print(sim.avg_Band_Block)
	avg_Block_B.append(sim.avg_Band_Block)
	#total_batch_blocked.append(sim.total_batch_blocking)
	#print(avg_simu_availability)
	simu_served.append(sim.avg_total_allocated)
	cpu.append(sim.avg_cpu)
	#print(cpu)
	util.resetParams()


def Confidence_interval(data, confidence=0.95):
    a = 1.0*numpy.array(data)
    n = len(a)
    m, se = numpy.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    #return m, m-h, m+h
    return h


avg_total_simu_fog = [float(sum(col))/len(col) for col in zip(*total_simu_fog)]
avg_total_delay = [float(sum(col))/len(col) for col in zip(*total_delay)]
avg_total_delay2 = [float(sum(col))/len(col) for col in zip(*total_delay2)]
total_simu_served = [float(sum(col))/len(col) for col in zip(*simu_served)]
total_average_simu_power = [float(sum(col))/len(col) for col in zip(*total_simu_power)]
total_simu_avai = [float(sum(col))/len(col) for col in zip(*avg_simu_availability)]
avg_total_simu_lambda_usage = [float(sum(col))/len(col) for col in zip(*total_simu_lambda_usage)]
avg_total_simu_cloud = [float(sum(col))/len(col) for col in zip(*total_simu_cloud)]
total_simu_reqs = [float(sum(col))/len(col) for col in zip(*simu_req)]
simu_nodes_mean = [float(sum(col))/len(col) for col in zip(*total_simu_nodes)]
simu_lambdas_mean=	[float(sum(col))/len(col) for col in zip(*total_simu_lambdas)]
simu_redir_mean=	[float(sum(col))/len(col) for col in zip(*total_simu_redir)]
simu_switches_mean=	[float(sum(col))/len(col) for col in zip(*total_simu_switches)]
simu_blocked_mean=	[float(sum(col))/len(col) for col in zip(*total_simu_blocked)]
simu_time_mean=	[float(sum(col))/len(col) for col in zip(*total_simu_time)]
avg_cpu = [float(sum(col))/len(col) for col in zip(*cpu)]

avg_simu_cloud_proc = [float(sum(col))/len(col) for col in zip(*total_simu_cloud_proc)]
avg_simu_fog_proc = [float(sum(col))/len(col) for col in zip(*total_simu_fog_proc)]
avg_simu_tot_proc = [float(sum(col))/len(col) for col in zip(*total_simu_tot_proc)]
avg_total_Block_B = [float(sum(col))/len(col) for col in zip(*avg_Block_B)]



avg_total_split_e = [float(sum(col))/len(col) for col in zip(*total_split_e)]
avg_total_split_i = [float(sum(col))/len(col) for col in zip(*total_split_i)]
avg_total_split_d = [float(sum(col))/len(col) for col in zip(*total_split_d)]
avg_total_split_b = [float(sum(col))/len(col) for col in zip(*total_split_b)]

#confidence intervals
simu_band_block_ci= []
split_e_ci = []
split_i_ci = []
split_d_ci = []
split_b_ci = []
simu_power_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_power)]
simu_lambda_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_lambda_usage)]
simu_blocking_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_blocked)]
#simu_exec_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_time)]
simu_availability_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_simu_availability)]
simu_band_block_ci= [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_Block_B)]

#split_e_ci= [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_total_split_e)]
#split_i_ci= [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_total_split_i)]
#split_d_ci= [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_total_split_d)]
#split_b_ci= [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_total_split_b)]


numpy.random.seed(1)
#dados = pd.DataFrame(data={"Energy_mean" : total_average_simu_power, "Energy_mean_ci":simu_power_ci, "cobertura": total_simu_avai,"Nodes_mean": simu_nodes_mean, "Lambdas_mean": simu_lambdas_mean, "Lambda_ci": simu_lambda_ci, "avg_lambda_usage" : avg_total_simu_lambda_usage,"Band_Block_Mbps"  : avg_total_Block_B, "Band_Block_Mbps_ci": simu_band_block_ci, "Split_E": avg_total_split_e,"Split_I": avg_total_split_i,"Split_D": avg_total_split_d, "Split_B": avg_total_split_b, "Split_E_ci": split_e_ci, "Split_I_ci": split_i_ci, "Split_D_ci": split_d_ci, "Split_B_ci": split_b_ci, "RRH Bloqueio" : simu_blocked_mean, "Solver": simu_time_mean})#,"Traffico_Total":avg_simu_tot_proc,"Cloud_Traffic":avg_simu_cloud_proc, "Fog_Traffic":avg_simu_fog_proc
dados = pd.DataFrame(data={"Energy_mean" : total_average_simu_power, "Energy_mean_ci":simu_power_ci, "cobertura": total_simu_avai,"Nodes_mean": simu_nodes_mean, "Lambdas_mean": simu_lambdas_mean, "Lambda_ci": simu_lambda_ci, "avg_lambda_usage" : avg_total_simu_lambda_usage, "Band_Block_Mbps"  : avg_total_Block_B, "Band_Block_Mbps_ci": simu_band_block_ci, "Split_E": avg_total_split_e,"Split_I": avg_total_split_i,"Split_D": avg_total_split_d, "Split_B": avg_total_split_b, "RRH Bloqueio" : simu_blocked_mean, "Solver": simu_time_mean})#"Cloud_Traffic":avg_simu_cloud_proc, "Fog_Traffic":avg_simu_fog_proc

dados.to_csv("SGO_Results.csv", sep=';',index=False)

with open('CPU.txt','w') as filehandle:  
    filehandle.write("Batch\n\n")
    filehandle.writelines("%s\n" % p for p in avg_cpu)
    filehandle.write("\n")

with open('cloud.txt','w') as filehandle:  
    filehandle.write("Batch\n\n")
    filehandle.writelines("%s\n" % p for p in avg_simu_cloud_proc)
    filehandle.write("\n")

with open('fog.txt','w') as filehandle:  
    filehandle.write("Batch\n\n")
    filehandle.writelines("%s\n" % p for p in avg_simu_fog_proc)
    filehandle.write("\n")


with open('all.txt','w') as filehandle:  
    filehandle.write("Batch\n\n")
    filehandle.writelines("%s\n" % p for p in avg_simu_tot_proc)
    filehandle.write("\n")

#with open('Solver.txt','w') as filehandle:  
#    filehandle.write("Batch\n\n")
#    filehandle.writelines("%s\n" % p for p in simu_time_mean)
#    filehandle.write("\n")

'''
plt.plot(avg_cpu,marker='o', label = "CPU SGO")
#plt.plot(batch_redir_mean,marker='^', label = "PureBatch-nfvILP")
#plt.xticks(numpy.arange(0, 24, 1))
#plt.yticks(numpy.arange(0, 500,50))
plt.ylabel('CPU Usage (%)')
plt.xlabel("Time of the day")
plt.legend(loc="upper left",prop={'size': 6})
plt.savefig('cpu.jpeg', format='jpeg', dpi=800)
plt.show()
'''
