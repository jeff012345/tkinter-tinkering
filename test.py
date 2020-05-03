# -*- coding: utf-8 -*-
import json
from os import path
import numpy as np
import Global
from WorldUtil import Position, makeNetwork, mutateAndRunNetwork
from DotBrain import DotBrain, NetworkWeights

SCALE_FACTOR = 1000000

def saveWeights(brain: DotBrain, start: Position):
    data = readWeights()
    if data is not None and data['fitness'] / SCALE_FACTOR > brain.fitness:
        return False
    
    data = {}
    data['hidden'] = brain.weights.hiddenLayer.tolist()
    data['output'] = brain.weights.outputLayer.tolist()
    data['fitness'] = brain.fitness * SCALE_FACTOR
    data['start'] = {'x': start.x, 'y': start.y }
    data['goal'] = {'x': brain.goal.x, 'y': brain.goal.y }
    
    with open('checkpoint.txt', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    
    print("Saving weights")
    return True
        
def readWeights():
    data = None
    
    if path.exists("checkpoint.txt"):
        with open('checkpoint.txt') as json_file:
            data = json.load(json_file)
            
    return data

def readSavedNetwork(goal: Position):
    savedData = readWeights()

    if savedData is None:
        return None

    # read weights
    weights = NetworkWeights()
    weights.hiddenLayer = np.asarray(savedData['hidden'])
    weights.outputLayer = np.asarray(savedData['output'])
    
    # make a network from the weights
    network = DotBrain(None, goal, makeNetwork(), weights)
    network.fitness = savedData['fitness'] / SCALE_FACTOR
    
    print(f'Loaded network with fitness = {network.fitness}')
    return network

def randomPosition():
    x = np.random.randint(Global.BOUNDARY_MIN + 1, Global.BOUNDARY_MAX)
    y = np.random.randint(Global.BOUNDARY_MIN + 1, Global.BOUNDARY_MAX)
    
    return Position(x, y)

if __name__ == '__main__':
    Global.OBSTACTLES = [
        [4, 4], 
        [6, 6], 
        [7, 9]
    ]
    Global.BOUNDARY_MIN = 0
    Global.BOUNDARY_MAX = 30
    
    tests = 0
    while tests < 10:
        #start = Position(1, 1)
        #goal = Position(15, 15)
        start = randomPosition()
        goal = randomPosition()
        
        print(f'Start = ({start.x}, {start.y})')
        print(f'Goal = ({goal.x}, {goal.y})')
        
        bestNetwork = None    
        if path.exists("checkpoint.txt"):
            bestNetwork = readSavedNetwork(goal)        
        else:
            bestNetwork = mutateAndRunNetwork(start, goal)
            print(f"Starting fitness = {bestNetwork.fitness}")
            
        trial = 0
        foundBetter = False
        trialsSinceBetter = 0
        
        while trial < 10:
            round = 0
            mutationBase = np.random.normal(0, 0.5, 1)[0]
            print(f'Mutation Base = {mutationBase}')
            
            while round < 10000:    
                network = mutateAndRunNetwork(start, goal, bestNetwork, np.random.rand() * mutationBase)
                            
                if bestNetwork.fitness < network.fitness:
                    print(f"New winner! Fitness = {network.fitness}")
                    bestNetwork = network
                    result = saveWeights(bestNetwork, start)
                    foundBetter = True
                    
                    if result is False:
                        # there's already a better saved network
                        bestNetwork = readSavedNetwork(goal)
                
                round = round + 1
                
            if foundBetter:
                trialsSinceBetter = 0
            else:
                trialsSinceBetter = trialsSinceBetter + 1
                
            if trialsSinceBetter == 3:
                print("Haven't found something better in 5 trials")
                break
            
            bestSaved = readSavedNetwork(goal)
            if bestSaved is not None:
                print(f"Loaded better saved. Fitness = {bestSaved.fitness}")
                bestNetwork = bestSaved
                trialsSinceBetter = 0
                
            trial = trial + 1
            
        print(f"Best Network Fitness = {bestNetwork.fitness}")
        tests = tests + 1

