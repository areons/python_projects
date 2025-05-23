from turtle import Turtle
import random as r

COLOR = 'red'
SHAPE = 'square'

class Food(Turtle):
    def __init__(self):
        super().__init__()
        self.shape(SHAPE)
        self.pu()
        self.shapesize(0.38, 0.38)
        self.color(COLOR)
        self.speed(0)
        self.refresh()


    def refresh(self):
        random_x = r.randint(-265, 265)
        random_y = r.randint(-265, 265)
        self.goto(random_x, random_y)