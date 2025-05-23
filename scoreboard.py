from turtle import Turtle

ALIGNMENT = 'center'
FONT = ('Courier', 21, 'normal')


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score=0
        with open('data.txt', 'r') as data:
            self.highest_score = int(data.read())
        self.color('white')
        self.pu()
        self.teleport(0, 268)
        self.hideturtle()
        self.update_scoreboard()


    def update_scoreboard(self):
        self.clear()
        self.write(f"Score: {self.score}    Highest Score: {self.highest_score}", align=ALIGNMENT, font=FONT)


    def reset(self):
        if self.score > self.highest_score:
            self.highest_score = self.score
            with open('data.txt', 'w') as data:
                data.write(f'{self.highest_score}')
        self.score = 0
        self.update_scoreboard()


    # def game_over(self):
    #     self.teleport(0,0)
    #     self.write("GAME OVER", align=ALIGNMENT, font= 'bold')


    def increase_score(self):
        self.score += 1
        self.update_scoreboard()