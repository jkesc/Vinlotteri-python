#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 13:10:37 2022

@author: jkescher
"""
def SpinWheel(names, tickets):
    import turtle as ttl
    from turtle import Screen, Turtle
    from colorsys import hsv_to_rgb
    
    try:
        ttl.reset() #god knows why, but the program needs to throw an error 50% of the time to work...
    except:
        print('')
            
    finally:
        #Defining the shape of the wheel, and number of slices
        RADIUS = 200
        NUMBER_OF_WEDGES = 150
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
        line.color(1,1,1)
        line.end_poly()
        
        #Registering all of our shapes to the screen
        screen.register_shape("wedge", turtle.get_poly())
        screen.register_shape("line", line.get_poly())
        screen.register_shape("needle", needle.get_poly())
        
        #Dividing the perimeter by number of tickets bought
        ticketSum = sum(tickets)
        divAng=[90]
        for i in tickets:
            divAng.append(divAng[-1]+i/ticketSum*360)
            divLine = Turtle("line")
            divLine.setheading(divAng[-1])
            
        # Entering names for the sections
        nameTurtle=Turtle(visible=True)
        nameTurtle.penup()
        nameTurtle.sety(nameTurtle.ycor()+RADIUS+30)
        nameTurtle.setheading(180)
        print(divAng)
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
                # turtle.color(*turtles[(index + 1) % NUMBER_OF_WEDGES].color()) # this is probably more efficient, but I had problems updating the needle properly
                turtle.right(SLICE_ANGLE)
                
            needle.right(SLICE_ANGLE)
            screen.update()
            screen.ontimer(draw_circle, 40)
        draw_circle()
        
        screen.exitonclick()
if __name__=='__main__':
    SpinWheel(['Karl','Knut','Vibeke','Panna'], [2,3,3,4])