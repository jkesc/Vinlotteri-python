#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:06:22 2022

@author: jkescher
"""
from tkinter import *
from tkinter import ttk

class count:
    def __init__(self, initVal=0):
        self.counter = initVal
        
    def increaseCounter(self):
        self.counter += 1

    def decreaseCounter(self):
        self.counter -= 1

    def getVal(self):
        return self.counter
    
def increaseVal():
    counter.increaseCounter()
    label["text"]=f"{counter.getVal()}"
    
def decreaseVal():
    counter.decreaseCounter()
    label["text"]=f"{counter.getVal()}"

root = Tk()

frm = ttk.Frame(root, padding=10)
frm.grid()

ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)

counter = count()

addBtn = ttk.Button(frm,text="+1",command=increaseVal)#counter.increaseCounter)
addBtn.grid(column=0, row=2)

subtractBtn = ttk.Button(frm,text="-1",command=decreaseVal)
subtractBtn.grid(column=1, row=2)

frame=ttk.Frame(frm,relief=RAISED)
frame.grid(column=1,row=1)
label=ttk.Label(frame,text=f"{counter.getVal()}")
label.grid(column=1, row=0, sticky="w")
root.mainloop()
