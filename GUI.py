#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:06:22 2022

@author: jkescher
"""
import tkinter as tk
import tkinter.ttk as ttk
from wheel import SpinWheel
import datetime as dt
import pandas as pd
import os

def log_entry(entry):
    if eTick.get().isnumeric():

        nameTxt.insert(tk.END,eName.get())
        nameTxt.insert(tk.END,'\n')
        ticketTxt.insert(tk.END,eTick.get())
        ticketTxt.insert(tk.END,'\n')
        eName.delete(0,tk.END)
        eTick.delete(0,tk.END)
        entry.focus()
    else:
        eTick.delete(0,tk.END)
        eTick.insert(0,"Must be an integer")
        
def run_lottery(entry_list: list):
    names = []
    tickets = []
    lastRow = int(nameTxt.index('end').split('.')[0])-2
    # Creating lists with names and tickets to pass to wheel
    for i in range(lastRow):
        i += 1  # because text seems to be 1-indexed...
        names.append(nameTxt.get(f"{i}.0", f"{i}.end"))
        tickets.append(int(ticketTxt.get(f"{i}.0", f"{i}.end")))
    entries = pd.DataFrame({'Participants': names, 'Tickets': tickets})
    entry_list.append(entries)
    # spinning the wheel and returning the winner
    winner = SpinWheel(names, tickets, pelton= pelton.get(), randomized=True)
    tk.messagebox.showinfo(message=f"The winner is {winner}!")
    
    # removing one ticket from winner
    tickets[names.index(winner)] -= 1
    ticketTxt.delete('1.0', tk.END)
    for i in tickets:
        ticketTxt.insert(tk.END, f"{i}\n")
    print(winner)

def destructor(master, entry_list):
    now = dt.datetime.now()
    excelpath = os.path.join(os.getcwd(),'out',f'lottery_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}')
    if len(entry_list)>1:
        for i, e in enumerate(entry_list):
            e.to_excel(f'{excelpath}_{i}.xlsx')
    else:
        print(f'printing to {excelpath}.xlsx')
        entry_list[0].to_excel(f'{excelpath}.xlsx')
    master.destroy()
    
if __name__ == '__main__':
    entry_list = []
    master = tk.Tk()
    nameText = ttk.Label(master, text="Name")
    nameText.grid(row=0,column=0)
    ticketText = ttk.Label(master, text="Tickets")
    ticketText.grid(row=0,column=1)
    
    eName = ttk.Entry(master)
    eTick = ttk.Entry(master)
    
    eName.grid(row=1, column=0)
    eTick.grid(row=1, column=1)
    
    LogButton = ttk.Button(master, text="Log entry", command=lambda: log_entry(eName))
    LogButton.grid(row=2,column=1, sticky=tk.W)
    
    nameTxt = tk.Text(master, height=20, width=20)
    nameTxt.grid(row=3,column=0)
    
    ticketTxt = tk.Text(master, height=20, width=20)
    ticketTxt.grid(row=3,column=1)
    
    QuitButton = ttk.Button(master, text="Quit", command=lambda: destructor(master, entry_list))
    QuitButton.grid(row=2,column=0, sticky=tk.W)
    RunButton = ttk.Button(master, text="Run lottery!", command=lambda:run_lottery(entry_list))
    RunButton.grid(row=2,column=2)
    pelton = tk.BooleanVar()
    pelton.set(True)
    
    peltonButton = ttk.Checkbutton(master, text = 'Pelton turbine', onvalue=True, offvalue=False, variable=pelton)
    peltonButton.grid(row=2,column=3)
    copyRightText = ttk.Label(master, text="This program was created by Karl Escher (c) 2024",
              font=('Arial', 8), foreground='grey')
    copyRightText.grid(row=4, column=0)
    eName.focus()
    master.mainloop()
