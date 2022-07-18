#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:06:22 2022

@author: jkescher
"""
import tkinter as tk
import tkinter.ttk as ttk
import wheel as whl

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
    names = []
    tickets = []
    lastRow = int(nameTxt.index('end').split('.')[0])-2
    for i in range(lastRow):
        i=i+1#because text seems to be 1-indexed...
        names.append(nameTxt.get(f"{i}.0",f"{i}.end"))
        tickets.append(int(ticketTxt.get(f"{i}.0",f"{i}.end")))
        
    winner = whl.SpinWheel(names, tickets,False)
    # !TODO have to remove one ticket from the winner.
    tickets[names.index(winner)]-=1
    ticketTxt.delete('1.0',tk.END)
    for i in tickets:
        ticketTxt.insert(tk.END,f"{i}\n")
    print(winner)
master = tk.Tk()

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
nameTxt.insert(tk.END,"""a
b
c
""")
ticketTxt.insert(tk.END,"""1
2
3
""")               
master.mainloop()
