from SGO.SGO import SGO

playerNumber = 15
substituteNumber = 2
kicksLimit = 1000000
functionEvaluationLimit = 100000
numberOfRrh = 20
target = 0
moveOffProbability = 0.3

sgo = SGO(playerNumber, substituteNumber, kicksLimit, functionEvaluationLimit, numberOfRrh, target=target, moveOffProbability=moveOffProbability)

resultado = sgo.run()
