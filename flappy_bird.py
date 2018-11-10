import pygame as game
import random

height = 600
width = 1000
fps = 20

class Bird:
    def __init__(self):
        self.score = 0
        self.gravity = 8
        self.velocity = 0
        self.lift = -35
        self.x = 100
        self.y = height / 2
        self.radius = 15

    def up(self):
        self.velocity += self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if (self.y > height - self.radius):
            self.y = height - self.radius
            self.velocity = 0
        if (self.y < self.radius):
            self.y = self.radius
            self.velocity = 0

        self.score += 1

    def draw(self):
        game.draw.circle(window, (230,230,230),(self.x,int(self.y)),self.radius)

    def think(self):
        pass

    def hitPipe(self,pipe):
        if ((self.y - self.radius) < pipe.top + self.radius or (self.y + self.radius) > (height - pipe.bottom - self.radius)):
            if (self.x + self.radius) > pipe.x and (self.x - self.radius) < (pipe.x + pipe.width):
                return True
        return False

class Pipe:
    def __init__(self):
        self.spacing = random.randint(125,175)
        self.x = width
        self.width = 45
        self.top = random.randint(10,height-self.spacing)
        self.bottom = height - self.top - self.spacing
        self.speed = 5

    def draw(self):
        game.draw.rect(window, (255,255,255),(self.x,  0, self.width, self.top)) # top part of pipe
        game.draw.rect(window, (255,255,255),(self.x,  height - self.bottom, self.width, self.bottom)) # bottom part of pipe

    def update(self):
        self.x -= self.speed

    def offScreen(self):
            return self.x+self.width < 0

game.init()
window =   game.display.set_mode((width,height))
clock = game.time.Clock()
game.display.set_caption("FLAPPY BIRD")
flappy_bird = Bird()
pipes  = []
closestPipe = 5

i = 0
run = True
while run:
    clock.tick(fps)

    if (i % 50 == 0):
        pipes.append(Pipe())
        i = 0

    for event in game.event.get():
        if event.type == game.QUIT:
            run = False

        keys = game.key.get_pressed()
        if keys[game.K_SPACE]:
            flappy_bird.up()

    window.fill((50,50,50))

    flappy_bird.update()
    flappy_bird.draw()
    for pipe in reversed(pipes):
        pipe.update()
        pipe.draw()
        if pipe.offScreen():
             pipes.remove(pipe)

    if len(pipes) > 0:
        if pipes[0].x > 100:
            closestPipe = pipes[0]
        else:
            closestPipe = pipes[1]

    if (flappy_bird.hitPipe(closestPipe)):
        pipes = []
        # print("GAME OVER")
        #run = False


    game.display.update()
    i += 1 # frame counter for showing pipes

game.quit()
