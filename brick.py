# Definition of the game's Brick class
#
# This class contains all relevant information related to the Brick
# It sets the brick's X and Y coordinates when initialized to the input coordinates
# For each Brick object instantiated, a corresponding hit box object (Rect) is created
# to track interactions with the game's ball
#
# The Brick object also contain the variable hit, which keeps track of if the brick has already
# been hit by the player or not
#
import pygame


class Brick:
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y
        self.hit = False
        self.hb = pygame.Rect(x, y, 64, 64)

    def set_x(self, x):
        self.xPos = x

    def set_y(self, y):
        self.xPos = y

    def got_hit(self):
        self.hit = True