# Definition of the game's Ball class
#
# This class contains all relevant information related to the ball
# It sets the ball's image, speed, x and y velocities relative to speed,
# initial location as well as the location of the ball's hit box
#
# The frequently updated values of the ball class are stored in the pvl array
# so they can be accessed and manipulated easily
# The pvl array includes the ball's X and Y position, its X and Y velocity
# and the number of lives the player has left
#
# The ball also keeps track of the player's lives
import pygame
import random
import math


class Ball:
    def __init__(self):
        self.ballImg = pygame.image.load('Img/ball.png')
        self.ballX = (1000-32)/2
        self.ballY = 340
        self.ballSpeed = 6
        self.live_count = 0
        self.hb = pygame.Rect(self.ballX, self.ballY, 32, 32)
        self.seed = random.uniform(-1, 1)
        self.xVel = self.seed * self.ballSpeed
        self.yVel = math.sqrt(abs(self.ballSpeed**2 - self.xVel**2))
        self.pvl = [self.ballX, self.ballY, self.xVel, self.yVel, self.live_count]
