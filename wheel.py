#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 13:10:37 2022

@author: jkescher
"""
import turtle as ttl
from turtle import Screen, Turtle
from colorsys import hsv_to_rgb
import random as rng
import time
    
# function for updating the circle
def draw_circle(turtles, needle, screen, SLICE_ANGLE):

    # rotating turtles in clockwise direction
    for index, turtle in enumerate(turtles):
        turtle.right(SLICE_ANGLE/2)
        
    needle.right(SLICE_ANGLE/2)
    screen.update()


def SpinWheel(names, tickets, randomized=True, pelton=False):
    rng.seed()
    try:
        ttl.reset() #god knows why, but the program needs to throw an error 50% of the time to work...            
    finally:
        #Defining the shape of the wheel, and number of slices
        # Scaling relative to runner diameter by approximate measurements from VKL-coffee-mug
        D_factor = 360/2.54
        # RADIUS = 180
        RADIUS = D_factor*2.54/2
        GOAL_NUMBER_OF_WEDGES=200
        number_of_wedges = sum(tickets)*max(round(GOAL_NUMBER_OF_WEDGES/sum(tickets)),1)
        SLICE_ANGLE = 360 / number_of_wedges

        NUMBER_OF_BUCKETS = 17
        BUCKET_ANGLE = 360 / NUMBER_OF_BUCKETS
        # TODO: make textsize relative to number of participants
        # TODO: make textsize relative to screen size
        # TODO: make popup window fullscreen
        TEXT_SIZE = 30
        if pelton:
            # BUCKET_DIAMETER = RADIUS*0.4
            BUCKET_DIAMETER = D_factor*0.75
        else:
            BUCKET_DIAMETER = 0
        
        NUMBER_OF_HOLES = 12
        # HOLE_RADIUS = RADIUS/10
        HOLE_RADIUS = 0.235*D_factor/2
        # HOLE_RING_RADIUS = RADIUS*0.8
        HOLE_RING_RADIUS = 1.9*D_factor/2
        
        # RING_OUTER_RADIUS = RADIUS/2
        RING_OUTER_RADIUS = D_factor*1.27/2
        RING_THICKNESS = D_factor*0.155
        RING_INNER_RADIUS = RING_OUTER_RADIUS-RING_THICKNESS
        
        ## making max timer for rotations with nozzle, rotations after nozzle stopped, and min time for update interval.
        
        
        #Making the screen to draw on
        screen = Screen()
        screen.tracer(False)

        #defining the needle, indicating the winner
        needle = Turtle(visible=False)
        needle.begin_poly()
        # needle.penup()
        needle.sety(needle.ycor()+RADIUS+BUCKET_DIAMETER+30)
        # needle.setheading(90)
        needle.end_poly()
        
        # create a pie wedge-shaped cursor
        turtle = Turtle(visible=False)
        turtle.begin_poly()
        turtle.sety(turtle.ycor() + RADIUS)
        turtle.circle(-RADIUS, extent=SLICE_ANGLE)
        turtle.home()
        turtle.end_poly()
        
        # create a semi-circular bucket
        bucket = Turtle(visible=False)
        bucket.sety(RADIUS+BUCKET_DIAMETER)
        bucket.begin_poly()
        bucket.circle(-BUCKET_DIAMETER/2, extent=180)
        bucket.sety(RADIUS+BUCKET_DIAMETER)
        bucket.end_poly()
        
        #Defining lines to separate participants
        line = Turtle(visible=False)
        line.sety(turtle.ycor()+RADIUS +BUCKET_DIAMETER+ 20)
        line.begin_poly()
        line.sety(line.ycor()-20)
        line.end_poly()
        

        # Making jet
        jet = Turtle(visible=False)
        jet.setx(-RADIUS)
        jet.begin_poly()
        jet.setx(-RADIUS-BUCKET_DIAMETER)
        jet.sety(-RADIUS-5*BUCKET_DIAMETER)
        jet.setx(-RADIUS)
        jet.sety(0)
        jet.end_poly()
        
        # Making holes
        hole = Turtle(visible=False)
        hole.setx(HOLE_RING_RADIUS)
        hole.begin_poly()
        hole.circle(HOLE_RADIUS)
        hole.end_poly()
        hole.sety(0)
        
        ring = Turtle()
        ring.penup()
        ring.setx(-RING_OUTER_RADIUS)
        ring.begin_poly()
        ring.setheading(-90)
        ring.pendown()
        ring.circle(RING_OUTER_RADIUS)
        ring.penup()
        ring.goto(-RING_INNER_RADIUS,0)
        ring.setheading(-90)
        ring.pendown()
        ring.circle(RING_INNER_RADIUS)
        ring.end_poly()
        

        #Registering all of our shapes to the screen
        screen.clear()
        screen.tracer(False)
        screen.register_shape("jet", jet.get_poly())
        screen.register_shape("wedge", turtle.get_poly())
        screen.register_shape("line", line.get_poly())
        screen.register_shape("needle", needle.get_poly())
        screen.register_shape("bucket", bucket.get_poly())
        screen.register_shape("hole", hole.get_poly())
        screen.register_shape("ring", ring.get_poly())
    
        jetTurtle = Turtle("jet")
        jetTurtle.color((0,0,1))
        if not pelton:
            jetTurtle.hideturtle()
        
        
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
        nameTurtle.setx(nameTurtle.xcor()+RADIUS+BUCKET_DIAMETER+30)
        nameTurtle.setheading(90)
        
        for i,n in enumerate(names):
            sector = (divAng[i+1]-divAng[i])/2
            nameTurtle.circle(RADIUS+BUCKET_DIAMETER+30, extent=sector)
            nameTurtle.write(n, font=("Arial", TEXT_SIZE, "normal"))
            nameTurtle.circle(RADIUS+BUCKET_DIAMETER+30, extent=sector)
            
        #setting needle start position to top, in the middle of one slice
        needle=Turtle("needle")
        needle.setheading(90-SLICE_ANGLE/2)
        
        # create a turtle for each wedge in the pie
        turtles = []
        
        # Colouring all of the slices
        for hue in range(number_of_wedges):
            turtle = Turtle("wedge")
            turtle.color(hsv_to_rgb(hue / number_of_wedges, 1.0, 1.0))
            turtle.setheading(hue * SLICE_ANGLE+90)
        
            turtles.append(turtle)
        
        # Drawing all of the pelton-buckets:
        for hue in range(NUMBER_OF_BUCKETS):
            turtle = Turtle("bucket")
            turtle.color(hsv_to_rgb(hue / NUMBER_OF_BUCKETS, 1.0, 1.0))
            turtle.setheading(hue * BUCKET_ANGLE+90)
        
            turtles.append(turtle)
        # Drawing circles
        for i in range(NUMBER_OF_HOLES):
            turtle = Turtle("hole")
            turtle.color('white')
            turtle.setheading(360/NUMBER_OF_HOLES * i)
            turtles.append(turtle)
        
        turtle = Turtle('ring')
        turtle.color('white')
        turtles.append(turtle)
            
        #For debugging purposes
        if not randomized:
            delay=0.00001 # between 0.0001 and 0.00005
            head=90
            rotCount=0
            rotMax=0
            randAng =180
            friction=1.01 # between 1.005 and 1.01
            max_delay = 0.3
            
        #For the actual application
        else:
            delay=0.00001 + rng.random()*0.00004 # start velocity, between 0.00001 and 0.00005
            head=rng.randint(1,360)  # initial heading between 1 and 360 degrees
            rotCount=0
            rotMax=rng.randint(1,4)  # between 1 and 4 rotations
            randAng = rng.randint(1,360)  # between 1 and 360
            friction=rng.random()*0.005+1.005  # between 1.005 and 1.01
            max_delay = 0.2 + rng.random()*0.1  # between 0.2 and 0.3
        #This part slows down the wheel based upon semi-random criteria

        while delay<max_delay:
            # Counting the number of rotations
            head_old=head
            head=needle.heading()
            if head>head_old:
                rotCount+=1
                
            #Drawing circle with a period of timer milliseconds    
            draw_circle(turtles, needle, screen, SLICE_ANGLE)
            time.sleep(delay)
            
            
            #If the wheel has spun a couple of times, and some amount of one rotation it will slow down, i.e the update period increases.
            if (rotCount > rotMax and head < randAng) or rotCount > rotMax+1:
                delay*=friction
                if not randomized:
                    print(delay)
                jetTurtle.hideturtle()
        # checking who the winner is        
        head = needle.heading()%360
        for i,n in enumerate(names):
            if head >= divAng[i] and head < divAng[i+1]:
                print(f"the winner is {n}")
                return n
            #Terminating the screen.
        ttl.bye()

# %%
if __name__=='__main__':
    names=['a','b','c']
    tickets=[1,2,3]
    winner=SpinWheel(names,tickets,False, True)
