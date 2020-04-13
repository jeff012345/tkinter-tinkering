# -*- coding: utf-8 -*-
from tkinter import Tk, Canvas, mainloop, Button
from Dot import Dot

master = Tk()
master.resizable(0, 0);

canvas = Canvas(master, width=500, height=500)
canvas.pack()

dot1 = Dot(canvas, 100, 100)

widget = Button(master, text='Mouse Clicks')
widget.pack();

def start(event):
    print("Single Click, Button-l")
    
    cnt = 0
    while(cnt < 10):
        dot1.move(10, 10)
        cnt = cnt + 1
    
widget.bind('<Button-1>', start)
    

mainloop()