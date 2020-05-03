# -*- coding: utf-8 -*-
import sys
from typing import List
from Global import Position, PositionState
from Dot import Dot
import numpy as np
import math 

class Neuron:
    def __init__(self, evalFn):
        self.evalFn = evalFn
        
    def eval(self, value):
        return self.evalFn(value)

class Network:
    inputNodes: []
    hiddenLayer: List[Neuron] = []
    outputLayer: List[Neuron] = []
    
class NetworkWeights:
    hiddenLayer: List[List[float]]
    outputLayer: List[List[float]]

def reLU(x: float):
    try:
        return max(0, 1 / (1 + math.exp(-1 * x)))
    except OverflowError:
        return sys.float_info.max
    
def noop(x: float):
    return x

class DotBrain:
    
    fitness = None
        
    def __init__(self, dot: Dot, goal: Position, network: Network, weights: NetworkWeights):
        self.dot = dot
        self.goal = goal
        self.network = network
        self.weights = weights
        
        self.hiddenNodesCount = len(network.hiddenLayer)
        self.outputsCount = len(network.outputLayer)
                
        if weights.hiddenLayer.shape != (len(self.network.inputNodes) + 1, self.hiddenNodesCount):
            raise Exception("Hidden Layer nodes and weights mismatch")
        
        if weights.outputLayer.shape != (self.hiddenNodesCount + 1, self.outputsCount):
            raise Exception("Output Layer nodes and weights mismatch")
            
    def evaluateNetwork(self, state: PositionState):        
        inputValues = list(map(lambda f: f(state), self.network.inputNodes))
        
        hiddenLayerValues = self._evaluateHiddenLayer(inputValues, 
                                                     self.network.hiddenLayer,
                                                     self.weights.hiddenLayer)
        
        outputLayer = self._evaluateHiddenLayer(hiddenLayerValues, 
                                               self.network.outputLayer,
                                               self.weights.outputLayer)
        
        outputLayer = np.exp(outputLayer) / np.sum(np.exp(outputLayer), axis=0) 
        return outputLayer
    
    def _evaluateHiddenLayer(self, values: List[float], layer: List[Neuron], weights: List[List[float]]):
        neuronIndex = 0
        layerValues = np.zeros(len(layer))
        
        for neuron in layer:         
            sum = 0
            valueCnt = len(values)
            for inputNum in range(0, valueCnt):
                sum = sum + values[inputNum] * weights[inputNum][neuronIndex]
            
            bias = weights[valueCnt][neuronIndex]
            layerValues[neuronIndex] = neuron.eval(sum + bias)
            neuronIndex = neuronIndex + 1
            
        return layerValues
        
    def calcFitness(self, moves: int, finalState: PositionState, minMovesToGoal: float, initialDist: float):
        finalDistToGoal = (finalState.goal.x - finalState.x) ** 2 + (finalState.goal.y - finalState.y) ** 2 
        
        self.fitness = (1 - (finalDistToGoal / initialDist))
        
        if finalDistToGoal == 0:        
            self.fitness = self.fitness + (1 - (moves - minMovesToGoal) / minMovesToGoal)
