import random, copy
import numpy as np
from neuralNetwork_API import *

height = 300
width = 600
fps = 40

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

    def update(self):
        self.x -= self.speed

    def offScreen(self):
            return self.x+self.width < 0

saveOrNot = 0

def nextGeneration():
    global  savedFlappies, currentFlappies, pipes,saveOrNot, highscore
    highscore = 0
    for i in range(50):
        currentFlappies.append(Bird(None))
    saveOrNot = 0
    pipes = []
    calculateFitness(savedFlappies)

    for i in range(populationSize):
        currentFlappies.append(pickOne())

    savedFlappies = []

def pickOne():
    global saveOrNot, savedFlappies,run
    parent = savedFlappies[0]

    for flappy in savedFlappies:
        if flappy.fitness > parent.fitness:
            parent = flappy
    bestBirdOfEachGen.append(parent)
    if highscore > 990000 and saveOrNot == 0:
        filename =  "best_of_all.npy"
        parent.brain.saveNetwork(filename)
        print("saved best of all")
        run = False

    saveOrNot+= 1
    child = Bird(parent.brain)
    child.brain.mutate(0.1)
    return child

def calculateFitness(savedFlappies):
    sum = 0
    for bird in savedFlappies:
        sum += bird.score
    for bird in savedFlappies:
        bird.fitness = bird.score / sum


pipes  = []
#pipes.append(Pipe(width*0.6))
closestPipe = 5
populationSize = 1000
savedFlappies = []
currentFlappies = []
highscore = 0
currentGen = 1
bestBirdOfEachGen = []
for i in range(populationSize):
    currentFlappies.append(Bird(None))

i = 0
run = True
while run:
    for x in range(fps):

        if (i % 50 == 0):
            pipes.append(Pipe(width))
            i = 0


        for pipe in reversed(pipes):
            pipe.update()
            if pipe.offScreen():
                 pipes.remove(pipe)

        if len(pipes) > 0:
            if pipes[0].x > 40: #100 - 15 - 45 = bird.x - bird.radius - pipe.width
                closestPipe = pipes[0]
            else:
                closestPipe = pipes[1]

        for bird in currentFlappies:
            bird.score += 1
            if bird.score > highscore:
                highscore = bird.score
            bird.think(closestPipe)
            bird.update()
            if (bird.hitPipe(closestPipe)):
                savedFlappies.append(bird)
                currentFlappies.remove(bird)

        if len(currentFlappies) == 0:
            closestPipe = 5
            nextGeneration()
            currentGen += 1
            print("New Generation!")


        if (highscore % 45) == 0:
            print("highscore:",highscore,"Current Gen:",currentGen)
        i += 1 # frame counter for showing pipes
