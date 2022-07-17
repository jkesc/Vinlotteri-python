#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 13:10:37 2022

@author: jkescher
"""
import turtle as ttl
from turtle import Screen, Turtle
from colorsys import hsv_to_rgb

try:
    ttl.reset() #god knows why, but the program needs to throw an error 50% of the time to work...
finally:
    RADIUS = 200
    NUMBER_OF_WEDGES = 50
    SLICE_ANGLE = 360 / NUMBER_OF_WEDGES
    
    screen = Screen()
    screen.tracer(False)
    
    # create a pie wedge-shaped cursor
    turtle = Turtle(visible=False)
    turtle.begin_poly()
    turtle.sety(turtle.ycor() + RADIUS)
    turtle.circle(-RADIUS, extent=SLICE_ANGLE)
    turtle.home()
    turtle.end_poly()
    line = Turtle(visible=False)
    line.sety(turtle.ycor()+RADIUS + 20)
    line.begin_poly()
    line.sety(line.ycor()-20)
    line.end_poly()
    
    screen.register_shape("wedge", turtle.get_poly())
    screen.register_shape("line", line.get_poly())
    line.color(1,1,1)
    # create a turtle for each wedge in the pie
    turtles = []
    
    for hue in range(NUMBER_OF_WEDGES):
        turtle = Turtle("wedge")
        turtle.color(hsv_to_rgb(hue / NUMBER_OF_WEDGES, 1.0, 1.0))
        turtle.setheading(hue * SLICE_ANGLE+0.5*SLICE_ANGLE+90)
    
        turtles.append(turtle)
    
    def draw_circle():
    
        # have each turtle take on the color of its neighbor
        for index, turtle in enumerate(turtles):
            turtle.color(*turtles[(index + 1) % NUMBER_OF_WEDGES].color())
    
        screen.update()
        screen.ontimer(draw_circle, 40)
    
    draw_circle()
    
    screen.exitonclick()