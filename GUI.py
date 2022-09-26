#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 19:06:22 2022

@author: jkescher
"""
import tkinter as tk
import tkinter.ttk as ttk

def SpinWheel(names, tickets,randomized=True):
    import turtle as ttl
    from turtle import Screen, Turtle
    from colorsys import hsv_to_rgb
    import random as rng
    rng.seed()
    try:
        ttl.reset() #god knows why, but the program needs to throw an error 50% of the time to work...            
    finally:
        #Defining the shape of the wheel, and number of slices
        RADIUS = 200
        NUMBER_OF_WEDGES = sum(tickets)*10
        SLICE_ANGLE = 360 / NUMBER_OF_WEDGES
        
        #Making the screen to draw on
        screen = Screen()
        screen.tracer(False)

        #defining the needle, indicating the winner
        needle = Turtle(visible=False)
        needle.begin_poly()
        needle.penup()
        needle.sety(needle.ycor()+RADIUS+30)
        needle.setheading(90)
        needle.end_poly()
        
        # create a pie wedge-shaped cursor
        turtle = Turtle(visible=False)
        turtle.begin_poly()
        turtle.sety(turtle.ycor() + RADIUS)
        turtle.circle(-RADIUS, extent=SLICE_ANGLE)
        turtle.home()
        turtle.end_poly()
        
        #Defining lines to separate participants
        line = Turtle(visible=False)
        line.sety(turtle.ycor()+RADIUS + 20)
        line.begin_poly()
        line.sety(line.ycor()-20)
        line.end_poly()
        
        #Registering all of our shapes to the screen
        screen.clear()
        screen.tracer(False)
        screen.register_shape("wedge", turtle.get_poly())
        screen.register_shape("line", line.get_poly())
        screen.register_shape("needle", needle.get_poly())
        
        #Dividing the perimeter by number of tickets bought
        ticketSum = sum(tickets)
        divAng=[0]
        for i in tickets:
            divAng.append(divAng[-1]+i/ticketSum*360)
            divLine = Turtle("line")
            divLine.setheading(divAng[-1])
            
        # Entering names for the sections
        nameTurtle=Turtle(visible=False)
        nameTurtle.penup()
        nameTurtle.setx(nameTurtle.xcor()+RADIUS+30)
        nameTurtle.setheading(90)
        for i,n in enumerate(names):
            sector = (divAng[i+1]-divAng[i])/2
            nameTurtle.circle(RADIUS+30, extent=sector)
            nameTurtle.write(n)
            nameTurtle.circle(RADIUS+30, extent=sector)
            
        #setting needle start position to top, in the middle of one slice
        needle=Turtle("needle")
        needle.setheading(90-SLICE_ANGLE/2)
        
        # create a turtle for each wedge in the pie
        turtles = []
        
        # Colouring all of the slices
        for hue in range(NUMBER_OF_WEDGES):
            turtle = Turtle("wedge")
            turtle.color(hsv_to_rgb(hue / NUMBER_OF_WEDGES, 1.0, 1.0))
            turtle.setheading(hue * SLICE_ANGLE+90)
        
            turtles.append(turtle)
        # function for updating the circle
        def draw_circle():
        
            # rotating turtles in clockwise direction
            for index, turtle in enumerate(turtles):
                turtle.right(SLICE_ANGLE/2)
                
            needle.right(SLICE_ANGLE/2)
            screen.update()
            
        #For debugging purposes
        if not randomized:
            timer=1
            head=90
            rotCount=0
            rotMax=1
            randAng =180
            friction=2
            maxTimer = 1000
            
        #For the actual application
        else:
            timer=1
            head=90
            rotCount=0
            rotMax=rng.randint(5,15)
            randAng = rng.randint(1,360)
            friction=rng.random()*0.1+1
            maxTimer =rng.randint(1200,1700)
        #This part slows down the wheel based upon semi-random criteria
        while timer<maxTimer:
            # Counting the number of rotations
            head_old=head
            head=needle.heading()
            if head>head_old:
                rotCount+=1
                
            #Drawing circle with a period of timer milliseconds    
            draw_circle()
            screen.ontimer(draw_circle(),round(timer))
            
            #If the wheel has spun a couple of times, and some amount of one rotation it will slow down, i.e the update period increases.
            if rotCount > rotMax and head < randAng or rotCount > rotMax+1:
                timer*=friction
        # checking who the winner is        
        head = needle.heading()%360
        for i,n in enumerate(names):
            if head > divAng[i] and head < divAng[i+1]:
                # screen.exitonclick()
                return n
            #Terminating the screen.
            ttl.bye()
        ttl.mainloop()

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
        
    winner = SpinWheel(names, tickets)
    tk.messagebox.showinfo(message=f"The winner is {winner}!")
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
# nameTxt.insert(tk.END,"""Karl
# Knut
# Lu
# """)
# ticketTxt.insert(tk.END,"""2
# 2
# 2
# """)               
master.mainloop()
