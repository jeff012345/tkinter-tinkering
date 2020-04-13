# -*- coding: utf-8 -*-
from typing import List
from Dot import Dot
import numpy as np

class Position:
    x: int
    y: int
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# , weights, obstactles
# obsFn = Neuron(lambda p, obstactles : obstactleEval(dot, obstactles))
# goalFn = Neuron(lambda p : (self.goal.x - p.x, 2) ** 2 + (self.goal.y - p.y, 2) ** 2)
#def obstactleEval(dot: Dot, obstacles):
    #return 0

class Neuron:
    def __init__(self, evalFn):
        self.evalFn = evalFn
        
    def eval(self, value, weight: float):
        return self.evalFn(value) * weight

class Network:
    hiddenLayer: List[Neuron] = []
    outputLayer: List[Neuron] = []
    
class NetworkInputsWeights:
    hiddenLayer: List[float]
    outputLayer: List[float]

class DotBrain:
        
    def __init__(self, dot: Dot, goal: Position, network: Network, weights: List[NetworkInputsWeights]):
        self.dot = dot
        self.goal = goal
        self.network = network
        self.weights = weights
        
        self.hiddenNodesCount = len(network.hiddenLayer)
        self.outputsCount = len(network.outputLayer)

# =============================================================================        
#    def nextMove(self, current: Position):        
#        values = []
#        positions =[]
#         value = self.evalMove(current.x + 1, current.y)
#         values.append(value.shift())
#         positions.append(value)
#         
#         self.evalMove(current.x - 1, current.y)
#         values.append(value.shift())
#         positions.append(value)
#         
#         self.evalMove(current.x, current.y + 1)
#         values.append(value.shift())
#         positions.append(value)
#         
#         self.evalMove(current.x, current.y - 1)
#         values.append(value.shift())
#         positions.append(value)
#         
#         return positions[np.argmax(values)]
# =============================================================================
            
    def evaluateNetwork(self, inputValues: List[float]):
        hidden = lambda weights : weights.hiddenLayer
        output = lambda weights : weights.outputLayer
        
        hiddenWeightsByInput = list(map(hidden, self.weights))
        outputWeightsByInput = list(map(output, self.weights))
        
        hiddenLayerValues = self._evaluateHiddenLayer(inputValues, 
                                                     self.network.hiddenLayer,
                                                     hiddenWeightsByInput)
        
        outputLayer = self._evaluateHiddenLayer(hiddenLayerValues, 
                                               self.network.outputLayer,
                                               outputWeightsByInput)
        
        return outputLayer
    
    def _evaluateHiddenLayer(self, values: List[float], layer: List[Neuron], weights: List[List[float]]):
        neuronIndex = 0
        layerValues = np.zeros(len(layer))
        
        for neuron in layer:                        
            sum = 0
            for inputNum in range(0, len(values)):
                sum = sum + neuron.eval(values[inputNum], weights[inputNum][neuronIndex])
            
            layerValues[neuronIndex] = sum
            neuronIndex = neuronIndex + 1
            
        return layerValues
        
    def fitness(moves: int, reachedGoal: bool):
        reachedGoalValue = 1
        if not reachedGoal:
            reachedGoalValue = -1;
            
        return 1 / (moves * reachedGoalValue)
        

    
