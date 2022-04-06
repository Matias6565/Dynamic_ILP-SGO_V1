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

total_delay2 = []
avg_total_delay = []
#lists of total service availability
avg_simu_availability = []
#lists of total served rrhs
simu_served = []
cpu = []
avg_total_delay2 = []

#general function to reload modules
def reloadModule(aModule):
    importlib.reload(aModule)

util = sim.Util()

#exec_number = 40 - Teoria do Limite C.
exec_number = 2
number_of_rrhs = 5
#number_of_rrhs = 40 - Nosso cenário

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
	#total_simu_time.append(sim.avg_time_b)
	total_simu_lambda_usage.append(sim.avg_lambda_usage)
	avg_simu_availability.append(sim.avg_service_availability)
	#total_simu_blocked.append(sim.batch_blocking)
	total_simu_blocked.append(sim.total_batch_blocking)
	print(sim.total_batch_blocking)
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


#confidence intervals
simu_power_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_power)]
simu_lambda_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_lambda_usage)]
simu_blocking_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_blocked)]
#simu_exec_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_time)]
simu_availability_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*avg_simu_availability)]
#simu_ci = [Confidence_interval(col, confidence = 0.95) for col in zip(*total_simu_power)]


numpy.random.seed(1)
#dados = pd.DataFrame(data={"simu_lambda_ci": simu_lambda_ci, "simu_exec_ci" : simu_exec_ci, "total_average_simu_power" : total_average_simu_power, "avg_total_simu_lambda_usage" : avg_total_simu_lambda_usage,"simu_nodes_mean": simu_nodes_mean, "simu_lambdas_mean": simu_lambdas_mean, "simu_time_mean" : simu_time_mean, "avg_total_simu_cloud": avg_total_simu_cloud, "avg_total_simu_fog":avg_total_simu_fog, "total_simu_served":total_simu_served, "total_simu_reqs":total_simu_reqs,"total_simu_avai":total_simu_avai, "avg_total_delay": avg_total_delay, "DelayCulmulado" : avg_total_delay2})

dados = pd.DataFrame(data={"Energy_mean" : total_average_simu_power, "Energy_mean_ci":simu_power_ci, "cobertura": total_simu_avai,"Nodes_mean": simu_nodes_mean, "Lambdas_mean": simu_lambdas_mean, "Lambda_ci": simu_lambda_ci, "avg_lambda_usage" : avg_total_simu_lambda_usage, "Bloqueio" : simu_blocked_mean})
dados.to_csv("SGO_Results.csv", sep=';',index=False)

with open('CPU.txt','w') as filehandle:  
    filehandle.write("Batch\n\n")
    filehandle.writelines("%s\n" % p for p in avg_cpu)
    filehandle.write("\n")

