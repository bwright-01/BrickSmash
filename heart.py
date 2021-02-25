# Definition of the game's Heart class
#
# This class contains all relevant information related to the heart
# It sets the hearts X and Y coordinates when initialized to the input coordinates
#
# The heart class also contains the variable lost, which keeps track of if a heart object
# represents a life the player has lost or not
#
class Heart:
    def __init__(self, x, y):
        self.xPos = x
        self.yPos = y
        self.lost = False

    def set_x(self, x):
        self.xPos = x

    def set_y(self, y):
        self.xPos = y

    def lose(self):
        self.lost = True