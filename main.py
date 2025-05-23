from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time


screen=Screen()
screen.setup(600,600)
screen.bgcolor('black')
screen.title("Ariel' Snack Game")
screen.tracer(0)

snake=Snake()
food=Food()
scoreboard=Scoreboard()

screen.listen()
screen.onkey(snake.up,"Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left,"Left")
screen.onkey(snake.right, "Right")


game_on = True
while game_on:
    screen.update()
    SPEED = 0.05
    time.sleep(SPEED)

    snake.move()
    if snake.head.distance(food) < 10:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()
        snake.move_distance += (SPEED * 3)


    #Detect collision statment
    if snake.head.xcor() > 296 or snake.head.xcor() < -296 or snake.head.ycor() > 296 or snake.head.ycor() < -296:
        scoreboard.reset()
        snake.reset()
        snake.move_distance = 7

    #detect collision with its tail
    for segment in snake.snks[1:]:
        if snake.head.distance(segment) < 5:
            scoreboard.reset()
            snake.reset()

screen.exitonclick()