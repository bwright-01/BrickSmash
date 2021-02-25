# Definition of the game's Player class
#
# This class contains all relevant information related to the paddle
# It sets the paddle's image, speed, initial location as well as the location
# # of the paddle's hit box
#
# The hit box is offset from the image of the paddle so it can more
# accurately track interactions with the ball
import pygame


class Player:
    def __init__(self):
        self.playerImg = pygame.image.load('Img/minus-128.png')
        self.playerSpeed = 8
        self.playerX = (1000 - 128) / 2
        self.playerY = 645
        self.playerX_change = 0
        self.hbOffset = -46
        self.hb = pygame.Rect(self.playerX, self.playerY-self.hbOffset, 128, 2)