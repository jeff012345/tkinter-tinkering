# -*- coding: utf-8 -*-
from tkinter import *
import time

class Scene:
    
    items = []
    update = []
    canvas: Canvas = None
    
    def __init__(self):
        self.master = Tk()
        self.master.resizable(0, 0);
        
        self.canvas = Canvas(self.master, width=500, height=500)
        self.canvas.pack()

    def run(self):
        print("run the scene")
        self.master.update() # fix geometry
        
        try:
            print("start loop")
            cnt = 0
            while cnt < 10:         
                for dot in self.update:                    
                    dot.move(10,0)
                    self.master.update_idletasks() # redraw
                
                self.master.update() # process events
                time.sleep(0.2)
                cnt = cnt + 1
                
            print("done with loop")
            
        except Exception as err:
            print("error in main loop")
            print(err)
            pass # to avoid errors when the window is closed
        
        try:
            self.master.destroy()
            print("destroyed")
        except TclError:        
            print('failed to destroy')
        
        print("done")
            
