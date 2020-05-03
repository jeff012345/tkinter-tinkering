# -*- coding: utf-8 -*-
OBSTACTLES = []
BOUNDARY_MIN=0
BOUNDARY_MAX=20

class Position:
    x: int
    y: int
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class PositionState:
    def __init__(self, x: int, y: int, goal: Position):
        self.x = x;
        self.y = y
        self.goal = goal
        
    def atGoal(self):
        return self.x == self.goal.x and self.y == self.goal.y   
    
    def isOutOfBounds(self):
        return self.x < BOUNDARY_MIN or self.x > BOUNDARY_MAX or self.y < BOUNDARY_MIN or self.y > BOUNDARY_MAX
    
def isObstacle(x, y):
    if(x == BOUNDARY_MIN or x == BOUNDARY_MAX or y == BOUNDARY_MIN or y == BOUNDARY_MAX):
        return True
    
    for i in range(0, len(OBSTACTLES)):
        if OBSTACTLES[i][0] == x and OBSTACTLES[i][1] == y:
            return True
    
    return False

