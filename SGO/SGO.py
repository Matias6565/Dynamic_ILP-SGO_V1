#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: meimarcel
"""

from copy import copy
from SGO.Player import Player
import time
import numpy as np
from math import e
from RestrictionAll import Restricao

nodeState = [0,0,0,0,0,0,0]
split_state = [0,0,0,0,0,0,0,0]
rrhs_on_nodes = [0,0,0,0,0,0,0]
lambda_state = [0,0,0,0,0,0,0,0]
act_lambda = 0
global tempo

class SGO:
    def __init__(self, playerNumber, substituteNumber, kicksLimit, functionEvaluationLimit, numberOfRrh, numberOfVariables=[3,8,4],
                 target=None, moveOffProbability=0.1, moveForwardAfterMoveOffProbability=0.05, 
                 substitutionProbability=0.1, inertiaWeight=0.191, cognitiveWeight=0.191, socialWeight=0.618):
        self.playerNumber = playerNumber
        self.substituteNumber = substituteNumber
        self.kicksLimit = kicksLimit
        self.functionEvaluationLimit=functionEvaluationLimit
        self.numberOfRrh=numberOfRrh
        self.numberOfVariables = numberOfVariables
        self.target = target
        self.moveOffProbability = moveOffProbability
        self.moveForwardAfterMoveOffProbability = moveForwardAfterMoveOffProbability
        self.substitutionProbability = substitutionProbability
        self.inertiaWeight = inertiaWeight
        self.cognitiveWeight = cognitiveWeight
        self.socialWeight = socialWeight
        self.dataFit = []
        self.globalBestPosition = []
        self.globalBestEval = 10e1000000000000000
        self.globalBestEvals = []
        self.tempo = 0
    
    def run(self):
        players = []
        substitutePlayers = []
        functionEval = 0
        
        #print("---------------------------EXECUTING---------------------------")
        startTime = time.time()
        
        players = self.__initPopulation()
        substitutePlayers = self.__initSubstitutes(players)
        functionEval += self.playerNumber
        
        for kick in range(self.kicksLimit):
            #print("Iteration :",kick,"BestEval =",self.globalBestEval,"BestPositions =",self.globalBestPosition)
            #print("Evals:",self.globalBestEvals)
            eval,total_cloud,total_fog = self.__evaluate(self.globalBestPosition)
            #print("Cloud", total_cloud, "Fog", total_fog)
            self.dataFit.append(self.globalBestEval)
            
            if(self.target != None and self.globalBestEval <= self.target):
                break;
            
            if(functionEval >= self.functionEvaluationLimit):
                break;
            
            potentialBestEval = 10e1000000000000000
            potentialBestEvals = []
            potentialBestPosition = []
            
            for player in players:
                
                if np.random.rand() <= self.moveOffProbability:
                    self.__move_off(player)
                    
                    if np.random.rand() <= self.moveForwardAfterMoveOffProbability:
                        self.__move_forward(player)

                else:
                    self.__move_forward(player)
                
                evals,*resto = self.__evaluate(player.position)
                functionEval += 1

                for e in range(len(evals)):
                    for q in range(len(eval[e])):
                        if evals[e][q] < player.bestEvals[e][q]:
                            player.bestEvals[e][q] = evals[e][q]
                            player.bestPosition[e][q] = player.position[e][q].copy()
                
                evals,*resto = self.__evaluate(player.bestPosition)
                functionEval += 1
                
                player.bestEvals = [e.copy() for e in evals]

                if player.getBestEval() < potentialBestEval:
                    potentialBestEval = player.getBestEval()
                    potentialBestEvals = [e.copy() for e in player.bestEvals]
                    potentialBestPosition = [[p.copy() for p in pp] for pp in player.bestPosition]
                
                if(functionEval >= self.functionEvaluationLimit):
                    break;
            
            if potentialBestEval < self.globalBestEval:
                self.globalBestEval = potentialBestEval
                self.globalBestEvals = [e.copy() for e in potentialBestEvals]
                self.globalBestPosition = [[p.copy() for p in pp] for pp in potentialBestPosition]
                
            if np.random.rand() <= self.substitutionProbability:
                playerIndex = np.random.randint(self.playerNumber)
                substituteIndex = np.random.randint(self.substituteNumber)
                
                if substitutePlayers[substituteIndex].getBestEval() < players[playerIndex].getBestEval():
                    players[playerIndex].bestEvals = [e.copy() for e in substitutePlayers[substituteIndex].bestEvals]
                    players[playerIndex].position = [[p.copy() for p in pp] for pp in substitutePlayers[substituteIndex].bestPosition]
                    players[playerIndex].bestPosition = [[p.copy() for p in pp] for pp in substitutePlayers[substituteIndex].bestPosition]

            playersSorted = players.copy()
            playersSorted.sort(key=lambda x: x.getBestEval())
            
            playerIndex = 0
            for i in range(self.substituteNumber):
                if playersSorted[playerIndex].getBestEval() < substitutePlayers[i].getBestEval():
                    substitutePlayers.insert(i, Player([[p.copy() for p in pp] for pp in playersSorted[playerIndex].bestPosition], [[p.copy() for p in pp] for pp in playersSorted[playerIndex].bestPosition], [e.copy() for e in playersSorted[playerIndex].bestEvals], playersSorted[playerIndex].numberOfRrh, playersSorted[playerIndex].numberOfVariables))
                    substitutePlayers.pop()
                    playerIndex += 1        

        total = self.globalBestPosition
        #print(total)
        for t in range(len(total)):
            Node_id = total[t][0]
            Lambda_id = total[t][1]
            Split_id = total[t][2]
            print("Node_ID {}; Lambda_ID {}; Split_ID {}; and Antenas {}".format(Node_id, Lambda_id, Split_id, t))


        endTime = time.time()
        self.tempo = float(endTime-startTime)
        #print("")
        #print("Execution Time: %fs" %(endTime-startTime))
        #print("Execution Time2: {}" .format(self.tempo))
        #print("Function Evaluations:",functionEval)
        #print("------------------------------END------------------------------")
        return self.globalBestPosition
                    
                    
            
    def __initPopulation(self):
        players = []
        self.globalBestEval = 10e1000000000000000
    
        
        for i in range(self.playerNumber):
            position = []
            for j in range(self.numberOfRrh):
                position.append([list(np.random.choice([0,1], self.numberOfVariables[x])) for x in range(len(self.numberOfVariables))])
            
            for x in range(self.numberOfRrh):
                position[x][0][0] = 1
                position[x][2][0] = 1
            
            evals,*resto = self.__evaluate(position)
            
            player = Player([[p.copy() for p in pp] for pp in position], [[p.copy() for p in pp] for pp in position], [e.copy() for e in evals], self.numberOfRrh, self.numberOfVariables)
            players.append(player)
            
            if player.getBestEval() < self.globalBestEval:
                self.globalBestEval = player.getBestEval()
                self.globalBestEvals = [e.copy() for e in player.bestEvals]
                self.globalBestPosition = [[p.copy() for p in pp] for pp in position]
            
        return players
            
    def __initSubstitutes(self, players):
        substitutes = []
        
        playersSorted = players.copy()
        playersSorted.sort(key=lambda x: x.getBestEval())
        
        for player in playersSorted[:self.substituteNumber]:
            substitutes.append(Player([[p.copy() for p in pp] for pp in player.bestPosition], [[p.copy() for p in pp] for pp in player.bestPosition], [e.copy() for e in player.bestEvals], player.numberOfRrh, player.numberOfVariables))
        
        return substitutes
    
    def __evaluate(self, position):
        evals = []
        
        total_traffic_cloud = 0
        total_traffic_fog = 0
        traffic_fog1 = 0
        traffic_fog2 = 0
        traffic_wavelength = [0, 0, 0, 0, 0, 0, 0, 0]
        
        for x in range(self.numberOfRrh):
            eval, total_traffic_cloud, total_traffic_fog, traffic_fog1, traffic_fog2, traffic_wavelength = Restricao().energy(total_traffic_cloud, total_traffic_fog, traffic_fog1, traffic_fog2, traffic_wavelength, position[x])
            evals.append(eval)
                         
        return evals, total_traffic_cloud, total_traffic_fog
    
    def __move_off(self, player):
        #player.position = list(np.random.choice([0,1], self.numberOfVariables))
        
        for x in range(self.numberOfRrh):
            for y in range(len(self.numberOfVariables)):
                for k in range(self.numberOfVariables[y]):
                    if np.random.rand() < 0.5:
                        if player.position[x][y][k] == 1:
                            player.position[x][y][k] = 0
                        else:
                            player.position[x][y][k] = 1
        
        for x in range(self.numberOfRrh):
            if player.position[x][0].count(1) == 0 or player.position[x][2].count(1) == 0:
                player.position[x][0][0] = 1
                player.position[x][2][0] = 1
                
    
    def __move_forward(self, player):
        bestPosition = player.bestPosition.copy()
        
        for i in range(self.numberOfRrh):
            for j in range(len(self.numberOfVariables)):
                for k in range(self.numberOfVariables[j]):
                    if bestPosition[i][j][k] == 1:
                        d11 = self.cognitiveWeight * np.random.rand()
                        d01 = self.cognitiveWeight * np.random.rand() * -1
                        d12 = self.socialWeight * np.random.rand()
                        d02 = self.socialWeight * np.random.rand() * -1
                    else:
                        d11 = self.cognitiveWeight * np.random.rand() * -1
                        d01 = self.cognitiveWeight * np.random.rand()
                        d12 = self.socialWeight * np.random.rand() * -1
                        d02 = self.socialWeight * np.random.rand()

                    player.v1[i][j][k] = (self.inertiaWeight * player.v1[i][j][k]) + d11 + d12
                    player.v0[i][j][k] = (self.inertiaWeight * player.v0[i][j][k]) + d01 + d02
                    
                    if player.position[i][j][k] == 0:
                        if np.random.rand() < self.__sig(player.v1[i][j][k]):
                            player.position[i][j][k] = 1
                        else:
                            player.position[i][j][k] = 0
                    else:
                        if np.random.rand() < self.__sig(player.v0[i][j][k]):
                            player.position[i][j][k] = 0
                        else:
                            player.position[i][j][k] = 1
            
            
            if player.position[i][0].count(1) == 0 or player.position[i][2].count(1) == 0:
                player.position[i][0][0] = 1
                player.position[i][2][0] = 1
    
    
    def __sig(self, v):
        return 1 / (1 + (e ** (-v)))

    def updateValues(self):
        total = self.globalBestPosition
        for t in range(len(total)):
            node_id = total[t][0]
            lambda_id = total[t][1]
            split_id = total[t][2]
            for i in range(len(node_id)):
                if node_id[i] ==1:
                    #print("node state de {} é {}".format(i,node_id[i]))
                    if nodeState[i] == 0:
                        nodeState[i] = 1
                        #print("node state de {} é {}".format(i,node_id[i]))
            for j in range(len(lambda_id)):
                if lambda_id[j] ==1:
                    if lambda_state[j] == 0:
                        lambda_state[i] = 1

    def get_Tempo(self):
        return self.tempo

	#compute the power consumption at the moment
    def getPowerConsumption(self):
        netCost = 0.0
        for i in range(len(nodeState)):
            if nodeState[i] == 1:
                if i == 0:
                    netCost += 600.0
                else:
                    netCost += 300.0
        for w in lambda_state:
            if w == 1:
                netCost += 20.0
        #for s in switch_state:
        #    if s == 1:
        #        netCost += 15.0
        return netCost

    def countNodes(self):
        return nodeState.count(1)

    def countlambdas(self):
        return lambda_state.count(1)

    def Cloudprocessing(self):
        cloud = 0
        total = self.globalBestPosition
        for t in range(len(total)):
            split_id = total[t][2]
            if split_id[0]==1:
                cloud+=1966
            if split_id[1]==1:
                cloud+= 675
            if split_id[2]==1:
                cloud+= 119
            if split_id[3]==1:
                cloud+=74
        return cloud

    def Fogprocessing(self):
        fog = 0
        total = self.globalBestPosition
        for t in range(len(total)):
            split_id = total[t][2]
            if split_id[0]==1:
                fog+=0
            if split_id[1]==1:
                fog+= 1966 - 675
            if split_id[2]==1:
                fog+= 1966- 119
            if split_id[3]==1:
                fog+= 1966- 74
        return fog

    def Totalprocessing(self):
        total = 0
        tot = self.globalBestPosition
        for t in range(len(tot)):
            split_id = tot[t][2]
            if split_id[0]==1:
                total+=1966
            if split_id[1]==1:
                total+= 1966
            if split_id[2]==1:
                total+= 1966
            if split_id[3]==1:
                total+= 1966
        return total






