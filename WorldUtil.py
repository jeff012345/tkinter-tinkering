# -*- coding: utf-8 -*-
from typing import List
from Global import Position, PositionState, isObstacle
from DotBrain import DotBrain, Neuron, reLU, noop, Network, NetworkWeights
import numpy as np
import math

def calcObstactleDistance(state: PositionState, move):
    dist = 0
    x = state.x
    y = state.y
    
    while isObstacle(x, y) is False:
        dist = dist + 1
        x = x + move[0]
        y = y + move[1]
    
    return dist

def obstactleNorthFn(state: PositionState):
    return calcObstactleDistance(state, (0, 1))

def obstactleSouthFn(state: PositionState):
    return calcObstactleDistance(state, (0, -1))

def obstactleWestFn(state: PositionState):
    return calcObstactleDistance(state, (-1, 0))

def obstactleEastFn(state: PositionState):
    return calcObstactleDistance(state, (1, 0))

def goalDistanceFn(state: PositionState):
    return (state.goal.x - state.x) ** 2 + (state.goal.y - state.y) ** 2

def makeNetwork():    
    network = Network()
    
    network.inputNodes = [
        obstactleNorthFn, 
        obstactleSouthFn, 
        obstactleWestFn, 
        obstactleEastFn, 
        goalDistanceFn
    ]
    
    network.hiddenLayer = [
        Neuron(reLU), 
        Neuron(reLU), 
        Neuron(reLU), 
        Neuron(reLU), 
        Neuron(reLU), 
        Neuron(reLU), 
        Neuron(reLU), 
        Neuron(reLU),
        Neuron(reLU),
        Neuron(reLU)
    ]
    
    network.outputLayer = [Neuron(noop), Neuron(noop), Neuron(noop), Neuron(noop)]
    
    return network

def makeRandomNetwork(goal: Position, parent: Network, mutationFactor: float):
    # make neural network
    network = makeNetwork()    
    
    # create random weights for the network    
    weights = NetworkWeights()
    
    if parent is None:    
        weights.hiddenLayer = makeRandomWeights(len(network.inputNodes) + 1, len(network.hiddenLayer))
        weights.outputLayer = makeRandomWeights(len(network.hiddenLayer) + 1, len(network.outputLayer))
    else:
        weights.hiddenLayer = addNoiseToWeights(parent.weights.hiddenLayer, mutationFactor)
        weights.outputLayer = addNoiseToWeights(parent.weights.outputLayer, mutationFactor)
    
    # create dot brain    
    return DotBrain(None, goal, network, weights)

def addNoiseToWeights(weights: List[List[float]], factor: float):    
    newWeights = np.zeros(weights.shape)
    
    for i in range(0, weights.shape[0]):
        for j in range(0, weights.shape[1]):            
            newWeights[i][j] = max(-1, min(1, weights[i][j] + (0.5 - np.random.rand()) * factor))
    
    return newWeights


def makeRandomWeights(numberOfInputs: int, numberOfNodes: int): 
    arr = np.random.rand(numberOfInputs, numberOfNodes)
    
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            if np.random.rand(1) >= 0.5:
                arr[i][j] = -1 * arr[i][j]
    
    return arr

def mutateAndRunNetwork(start: Position, goal: Position, parent: DotBrain = None, mutationFactor: float = 1):    
    dotBrain = makeRandomNetwork(goal, parent, mutationFactor)
    return runNetwork(start, goal, dotBrain)
    
def runNetwork(start: Position, goal: Position, dotBrain: DotBrain, verbose = False):
    currentState = PositionState(start.x, start.y, goal)   
    step = 0
    
    initialDist = (goal.x - start.x) ** 2 + (goal.y - start.y) ** 2
    movesToGoal = math.ceil(math.sqrt(initialDist))
    
    while step < 100:
        outputs = dotBrain.evaluateNetwork(currentState)
        move = np.argmax(outputs)
        
        if move == 0:
            currentState.x = currentState.x + 1
        elif move == 1:
            currentState.x = currentState.x - 1
        elif move == 2:
            currentState.y = currentState.y + 1
        else:
            currentState.y = currentState.y - 1     
        
        if verbose:
            print(f'Step = {step}, Postion = {currentState.x},{currentState.y}')
        step = step + 1
        
        if currentState.atGoal():
            if verbose: 
                print("Reached Goal!")
            break
        
        if currentState.isOutOfBounds():
            if verbose: 
                print("Out of bounds!")
            break
        
    dotBrain.calcFitness(step, currentState, movesToGoal, initialDist)
    
    if verbose:
        print(f"Fitness = {dotBrain.fitness}")
    
    return dotBrain
        