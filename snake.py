from turtle import Turtle

COLOR = 'green'
SHAPE = 'square'
UP = 90
DOWN = 270
LEFT = 180
RIGHT = 0

start_position = [(0,0), (-10,0), (-20,0)]

class Snake:
    def __init__(self):
        self.snks = []
        self.move_distance = 7 # <---- snake speed
        self.create_snake()
        self.head = self.snks[0]
        self.move()


    def create_snake(self):
        for position in start_position:
            self.add_segment(position)


    def add_segment(self, position):
        snk_p = Turtle(SHAPE)
        snk_p.pu()
        snk_p.color(COLOR)
        snk_p.shapesize(0.45, 0.45)
        snk_p.goto(position)
        self.snks.append(snk_p)


    def extend(self):
        self.add_segment(self.snks[-1].position())


    def move(self):
        for snake_block in range(len(self.snks) - 1, 0, -1):
            new_x = self.snks[snake_block - 1].xcor()
            new_y = self.snks[snake_block - 1].ycor()
            self.snks[snake_block].goto(new_x, new_y)
        self.head.forward(self.move_distance)


    def reset(self):
        for segment in self.snks:
            segment.goto(1000, 1000)
        self.snks.clear()
        self.create_snake()
        self.head = self.snks[0]


    def up(self):
        if self.head.heading() != DOWN:
            self.head.setheading(UP)

    def down(self):
        if self.head.heading() != UP:
            self.head.setheading(DOWN)

    def left(self):
        if self.head.heading() != RIGHT:
            self.head.setheading(LEFT)

    def right(self):
        if self.head.heading() != LEFT:
            self.head.setheading(RIGHT)