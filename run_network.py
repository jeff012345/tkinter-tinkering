# -*- coding: utf-8 -*-
from test import readSavedNetwork
from WorldUtil import runNetwork, Position
import Global

Global.OBSTACTLES = [
        [4, 4], 
        [6, 6], 
        [7, 9]
    ]
Global.BOUNDARY_MIN = 0
Global.BOUNDARY_MAX = 30

start = Position(1, 1)
goal = Position(20, 20)

bestNetwork = readSavedNetwork(goal)

runNetwork(start, goal, bestNetwork, verbose = True)


