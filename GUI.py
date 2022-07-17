#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:06:22 2022

@author: jkescher
"""
import tkinter as tk
import tkinter.ttk as ttk

# class count:
#     def __init__(self, initVal=0):
#         self.counter = initVal
        
#     def increaseCounter(self):
#         self.counter += 1

#     def decreaseCounter(self):
#         self.counter -= 1

#     def getVal(self):
#         return self.counter
    
# def increaseVal():
#     counter.increaseCounter()
#     label["text"]=f"{counter.getVal()}"
    
# def decreaseVal():
#     counter.decreaseCounter()
#     label["text"]=f"{counter.getVal()}"

# root = Tk()

# frm = ttk.Frame(root, padding=10)
# frm.grid()

# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=0, row=1)

# counter = count()

# addBtn = ttk.Button(frm,text="+1",command=increaseVal)#counter.increaseCounter)
# addBtn.grid(column=0, row=2)

# subtractBtn = ttk.Button(frm,text="-1",command=decreaseVal)
# subtractBtn.grid(column=1, row=2)

# frame=ttk.Frame(frm,relief=RAISED)
# frame.grid(column=1,row=1)
# label=ttk.Label(frame,text=f"{counter.getVal()}")
# label.grid(column=1, row=0, sticky="w")

def log_entry():
    if eTick.get().isnumeric():

        nameTxt.insert(tk.END,eName.get())
        nameTxt.insert(tk.END,'\n')
        ticketTxt.insert(tk.END,eTick.get())
        ticketTxt.insert(tk.END,'\n')
        eName.delete(0,tk.END)
        eTick.delete(0,tk.END)
    else:
        eTick.delete(0,tk.END)
        eTick.insert(0,"Must be an integer")
        
def spin_wheel():
    lastRow = int(nameTxt.index('end').split('.')[0])-2
    for i in range(lastRow):
        i=i+1#because text seems to be 1-indexed...
        names.append(nameTxt.get(f"{i}.0",f"{i}.end"))
        tickets.append(ticketTxt.get(f"{i}.0",f"{i}.end"))
    print(names)
    print(tickets)
master = tk.Tk()

names = []
tickets = []

ttk.Label(master, text="Name").grid(row=0,column=0)
ttk.Label(master, text="Tickets").grid(row=0,column=1)

eName = ttk.Entry(master)
eTick = ttk.Entry(master)

eName.grid(row=1, column=0)
eTick.grid(row=1,column=1)

nameTxt = tk.Text(master, height=20, width=20)
nameTxt.grid(row=3,column=0)
ticketTxt = tk.Text(master, height=20, width=20)
ticketTxt.grid(row=3,column=1)
ttk.Button(master, text="Quit", command=master.destroy).grid(row=2,column=0, sticky=tk.W)
ttk.Button(master, text="Log entry", command=log_entry).grid(row=2,column=1, sticky=tk.W)
ttk.Button(master, text="Spin wheel",command=spin_wheel).grid(row=2,column=2)
# nameTxt.insert(tk.END,"""a
# b
# c
# """)
# ticketTxt.insert(tk.END,"""1
# 2
# 3
# """)               
master.mainloop()
