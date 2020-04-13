# -*- coding: utf-8 -*-
from typing import List
from DotBrain import DotBrain, Network, NetworkInputsWeights, Position, Neuron
import math 
import numpy as np

obstactles = [[4, 4], [6, 6], [7, 9]]
NUM_OF_INPUTS = 2

def obstactleFn(x: int, y: int):
    for o in obstactles:
        if o[0] == x and 0[1] == y:
            return 0
    
    return 1

def goalDistanceFn(x: int, y: int, goal: Position):
    return (goal.x - x) ** 2 + (goal.y - y) ** 2

def reLU(x: float):
    return max(0, 1 / (1 + math.exp(-1 * x)))

def makeRandomWeights(numberOfInputs: int, numberOfNodes: int): 
    return np.random.rand(numberOfInputs, numberOfNodes)

# make neural network
network = Network()
network.hiddenLayer = [Neuron(reLU), Neuron(reLU)]
network.outputLayer = [Neuron(reLU), Neuron(reLU)]

# create random weights for the network
weights: List[NetworkInputsWeights] = []
for i in range(0, NUM_OF_INPUTS):
    inputWeights = NetworkInputsWeights()
    inputWeights.hiddenLayer = np.random.rand(len(network.hiddenLayer))
    inputWeights.outputLayer = np.random.rand(len(network.outputLayer))
    weights.append(inputWeights)

# create dot brain
goal = Position(10, 10)
dotBrain = DotBrain(None, goal, network, weights)

# evaluate move
x = 1
y = 1

inputs = [obstactleFn(x, y), goalDistanceFn(x, y, goal)]
outputs = dotBrain.evaluateNetwork(inputs)
print(outputs)