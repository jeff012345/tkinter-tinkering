# -*- coding: utf-8 -*-

from tkinter import Canvas

class Dot:
    
    circle = None
    radius = 25
    fill = "red"
    
    def __init__(self, canvas: Canvas, x, y):
        self.canvas = canvas;
        self.x = x
        self.y = y
        self.circle = self.canvas.create_oval(self.x, 
                                              self.y, 
                                              self.x + self.radius, 
                                              self.y + self.radius, 
                                              fill = self.fill)        
    
    def move(self, dX, dY):
        self.canvas.move(self.circle, dX, dY);