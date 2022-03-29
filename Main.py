from SGO.SGO import SGO

playerNumber = 100
substituteNumber = 5
kicksLimit = 1000000
functionEvaluationLimit = 1000000
numberOfRrh = 25
numberOfVariables = 15
target = 0

sgo = SGO(playerNumber, substituteNumber, kicksLimit, functionEvaluationLimit, numberOfRrh, numberOfVariables, target=target)
sgo.run()
