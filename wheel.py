#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 13:10:37 2022

@author: jkescher
"""
def SpinWheel(names, tickets,randomized=True, pelton=False):
    import turtle as ttl
    from turtle import Screen, Turtle
    from colorsys import hsv_to_rgb
    import random as rng
    rng.seed()
    try:
        ttl.reset() #god knows why, but the program needs to throw an error 50% of the time to work...            
    finally:
        #Defining the shape of the wheel, and number of slices
        RADIUS = 180
        NUMBER_OF_WEDGES = sum(tickets)*10
        SLICE_ANGLE = 360 / NUMBER_OF_WEDGES

        NUMBER_OF_BUCKETS = 17
        BUCKET_ANGLE = 360 / NUMBER_OF_BUCKETS
        if pelton:
            BUCKET_DIAMETER = RADIUS*0.4
        else:
            BUCKET_DIAMETER = 0
        
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

        #Registering all of our shapes to the screen
        screen.clear()
        screen.tracer(False)
        screen.register_shape("jet", jet.get_poly())
        screen.register_shape("wedge", turtle.get_poly())
        screen.register_shape("line", line.get_poly())
        screen.register_shape("needle", needle.get_poly())
        screen.register_shape("bucket", bucket.get_poly())
    
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
            nameTurtle.write(n)
            nameTurtle.circle(RADIUS+BUCKET_DIAMETER+30, extent=sector)
            
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
        
        # Drawing all of the pelton-buckets:
        for hue in range(NUMBER_OF_BUCKETS):
            turtle = Turtle("bucket")
            turtle.color(hsv_to_rgb(hue / NUMBER_OF_BUCKETS, 1.0, 1.0))
            turtle.pencolor((0,0,0))
            turtle.setheading(hue * BUCKET_ANGLE+90)
        
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
                jetTurtle.hideturtle()
        # checking who the winner is        
        head = needle.heading()%360
        for i,n in enumerate(names):
            if head > divAng[i] and head < divAng[i+1]:
                # screen.exitonclick()
                return n
            #Terminating the screen.
            ttl.bye()
        ttl.mainloop()
if __name__=='__main__':
    names=['a','b','c']
    tickets=[1,2,3]
    winner=SpinWheel(names,tickets,False, True)
