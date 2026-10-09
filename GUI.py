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
from playsound3 import playsound
import random as rng
rng.seed()

def log_entry(entry):
    if eTick.get().isnumeric():

        nameTxt.insert(tk.END, eName.get())
        nameTxt.insert(tk.END, '\n')
        ticketTxt.insert(tk.END, eTick.get())
        ticketTxt.insert(tk.END, '\n')
        eName.delete(0, tk.END)
        eTick.delete(0, tk.END)
        entry.focus()
    else:
        eTick.delete(0,tk.END)
        eTick.insert(0,"Must be an integer")


def run_lottery(entry_list: list, music_var:dict, music_list = []):   
    cwd = os.getcwd()
    music_var['path'] = os.path.join(cwd, 'music','spinning')
    stop_all_music(music_list)
    music_list.append(pick_music(music_var))
    names = []
    tickets = []
    lastRow = int(nameTxt.index('end').split('.')[0])-2
    # Creating lists with names and tickets to pass to wheel
    for i in range(lastRow):
        i += 1  # because text seems to be 1-indexed...
        names.append(nameTxt.get(f"{i}.0", f"{i}.end"))
        tickets.append(int(ticketTxt.get(f"{i}.0", f"{i}.end")))
    if len(names)==0:
        names = ['Emma',
                 'Olivia',
                 'Nora',
                 'Sofie',
                 'Leah',
                 'Ella',
                 'Frida',
                 'Sofia',
                 'Ellinor',
                 'Astrid',
                 'Noah',
                 'Jakob',
                 'Lucas',
                 'Emil',
                 'Oscar',
                 'William',
                 'Elias',
                 'Isak',
                 'Oliver',
                 'Ludvig']
        for _ in names:
            tickets.append(rng.randint(1,7))

    randindex = [i for i in range(len(names))]
    rand_names = []
    rand_tickets = []
    rng.shuffle(randindex)
    for i in randindex:
        rand_names.append(names[i])
        rand_tickets.append(tickets[i])
    entries = pd.DataFrame({'Participants': names, 'Tickets': tickets})
    entry_list.append(entries)
    write_to_excel(entry_list)   
    # spinning the wheel and returning the winner
    winner = SpinWheel(rand_names, rand_tickets, pelton = pelton.get(), randomized=True)
    tk.messagebox.showinfo(message=f"The winner is {winner}!")
    
    # removing one ticket from winner
    tickets[names.index(winner)] -= 1
    ticketTxt.delete('1.0', tk.END)
    for i in tickets:
        ticketTxt.insert(tk.END, f"{i}\n")
    print(winner)
    stop_all_music(music_list)
    music_var['path'] = os.path.join(cwd, 'music','selection')
    music_list.append(pick_music(music_var))


def pick_music(music_var):
    music_path = music_var['path']
    if os.path.exists(music_path):
        music_files = os.listdir(music_path)
        music_files = [f for f in music_files if f.endswith('.mp3')]
        music_name = rng.choice(music_files)
        music_object = playsound(os.path.join(music_path, music_name), block=False)
    else: 
        music_object = None
    return music_object


def stop_all_music(music_list):
    for m in music_list:
        try:
            if m.is_alive():
                m.stop()
        except Exception:
            continue
        music_list.pop()

def write_to_excel(entry_list):
    print('saving participant entries')
    now = dt.datetime.now()
    outpath = os.path.join(os.getcwd(),'out')
    excelpath = os.path.join(outpath,f'lottery_{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}')
    os.makedirs(outpath,exist_ok=True)
    if len(entry_list)>1:
        for i, e in enumerate(entry_list):
            e.to_excel(f'{excelpath}_{i}.xlsx')
    elif len(entry_list) == 1:
        print(f'printing to {excelpath}.xlsx')
        entry_list[0].to_excel(f'{excelpath}.xlsx')
    else:
        print('no entries, nothing written to excel-file')

def destructor(master, entry_list, music_list):
    write_to_excel(entry_list)
    stop_all_music(music_list)
    master.destroy()

def repeatMusic(music_list, music_var, master):
    try:
        for i, m in enumerate(music_list):
            if not m.is_alive():
                music_list.pop(i)
                music_list.append(pick_music(music_var))
        master.after(1000,
                     repeatMusic,
                     music_list,
                     music_var,
                     master)
    except:
        return
    
 

if __name__ == '__main__':      
    entry_list = []
    music_list = []
    cwd = os.getcwd()
    master = tk.Tk()
    music_var = {'path':os.path.join(cwd, 'music','selection')}
    stop_all_music(music_list)
    music_list.append(pick_music(music_var))
    master.after(1000,
                 repeatMusic,
                 music_list,
                 music_var,
                 master)
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
    
    QuitButton = ttk.Button(master, text="Quit", command=lambda: destructor(master, entry_list, music_list))
    QuitButton.grid(row=2,column=0, sticky=tk.W)
    RunButton = ttk.Button(master, text="Run lottery!", command=lambda:run_lottery(entry_list, music_var, music_list))
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
