#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:06:22 2022

@author: jkescher
"""
import tkinter as tk
import tkinter.ttk as ttk
from wheel import SpinWheel

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
        
def run_lottery():
    names = []
    tickets = []
    lastRow = int(nameTxt.index('end').split('.')[0])-2
    # Creating lists with names and tickets to pass to wheel
    for i in range(lastRow):
        i += 1  # because text seems to be 1-indexed...
        names.append(nameTxt.get(f"{i}.0", f"{i}.end"))
        tickets.append(int(ticketTxt.get(f"{i}.0", f"{i}.end")))
    # spinning the wheel and returning the winner
    winner = SpinWheel(names, tickets, pelton= pelton.get())
    tk.messagebox.showinfo(message=f"The winner is {winner}!")
    
    # removing one ticket from winner
    tickets[names.index(winner)] -= 1
    ticketTxt.delete('1.0', tk.END)
    for i in tickets:
        ticketTxt.insert(tk.END, f"{i}\n")
    print(winner)

if __name__ == '__main__':
    master = tk.Tk()
    
    ttk.Label(master, text="Name").grid(row=0,column=0)
    ttk.Label(master, text="Tickets").grid(row=0,column=1)
    
    eName = ttk.Entry(master)
    eTick = ttk.Entry(master)
    
    eName.grid(row=1, column=0)
    eTick.grid(row=1, column=1)
    
    nameTxt = tk.Text(master, height=20, width=20)
    nameTxt.grid(row=3,column=0)
    ticketTxt = tk.Text(master, height=20, width=20)
    ticketTxt.grid(row=3,column=1)
    ttk.Button(master, text="Quit", command=master.destroy).grid(row=2,column=0, sticky=tk.W)
    ttk.Button(master, text="Log entry", command=log_entry).grid(row=2,column=1, sticky=tk.W)
    ttk.Button(master, text="Run lottery!", command=run_lottery).grid(row=2,column=2)
    pelton = tk.BooleanVar()
    pelton.set(True)
    ttk.Checkbutton(master, text = 'Pelton turbine', onvalue=True, offvalue=False, variable=pelton).grid(row=2,column=3)
    ttk.Label(master, text="This program was created by Karl Escher (c) 2024",
              font=('Arial', 8), foreground='grey').grid(row=4, column=0)
    master.mainloop()
