import pygame as game
import numpy as np
from neuralNetwork_API import *
import time,copy,random

height = 600
width = 1000
fps = 50

class Bird:
    def __init__(self,brain):
        self.score = 0
        self.gravity = 8
        self.velocity = 0
        self.lift = -35
        self.x = 100
        self.y = height / 2
        self.radius = 15
        self.fitness = 0
        self.brain = 0
        if (brain != None):
            self.brain = copy.copy(brain)
        else:
            self.brain = neuralNetwork(5,10,2,0.15)

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
        game.draw.circle(window, (230,0,0),(self.x,int(self.y)),self.radius)

    def think(self,closestPipe):
        inputArray = []
        inputArray.append(self.velocity / 100.0)
        inputArray.append(self.y / 1000.0)
        if (closestPipe == 5): # no pipe
            inputArray.append(0.01)
            inputArray.append(0.01)
            inputArray.append(0.01)
        else:
            inputArray.append(closestPipe.x / 1000.0)
            inputArray.append(closestPipe.top / 1000.0)
            inputArray.append(closestPipe.bottom / 1000.0)
        outputs = self.brain.query(inputArray)
        if (outputs[1] > outputs[0]):
            self.up()

    def hitPipe(self,pipe):
        if pipe != 5: #no pipe
            if ((self.y - self.radius) < pipe.top + self.radius or (self.y + self.radius) > (height - pipe.bottom - self.radius)):
                if (self.x + self.radius) > pipe.x and (self.x - self.radius) < (pipe.x + pipe.width):
                    return True
        return False

class Pipe:
    def __init__(self,startPos):
        self.spacing = random.randint(125,175)
        self.x = startPos
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
myfont = game.font.SysFont("Comic Sans MS", 40)
pipes  = []
pipes.append(Pipe(width*0.6))
nn = neuralNetwork(1,2,3,0.4)
best_birds_brain = nn.loadNetwork("genData/best_of_all.npy")
bestBird = Bird(best_birds_brain)

failed = False
i = 1
run = True
while run:
    clock.tick(fps)

    textsurface = myfont.render("Score: "+str(bestBird.score), False, (0,200,200))
    gameover = myfont.render("", False, (0,200,200))

    if (i % 70 == 0):
        pipes.append(Pipe(width))
        i = 0

    for event in game.event.get():
        if event.type == game.QUIT:
            run = False

    window.fill((50,50,50))

    for pipe in reversed(pipes):
        pipe.update()
        pipe.draw()
        if pipe.offScreen():
             pipes.remove(pipe)

    if len(pipes) > 0:
        if pipes[0].x > 40: #100 - 15 - 45 = bird.x - bird.radius - pipe.width
            closestPipe = pipes[0]
        else:
            closestPipe = pipes[1]

    bestBird.think(closestPipe)
    bestBird.update()
    bestBird.draw()
    if (bestBird.hitPipe(closestPipe)):
        bestBird = Bird(best_birds_brain)
        pipes = []
        gameover = myfont.render("GAME OVER", False, (0,200,200))
        failed = True

    window.blit(textsurface,(width *0.7,height/20))
    window.blit(gameover,(width / 2 ,height/2-5))


    game.display.update()
    if failed:
        time.sleep(10)
        failed = False
    i += 1 # frame counter for showing pipes

game.quit()
