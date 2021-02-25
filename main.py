# Main file for Brick Smasher game
#
# In this game you control a paddle and you use it to hit a ball towards a wall of bricks.
# The ball passes through bricks, crushing them as it moves. The goal of the games is to crush all the bricks.
# You have four hearts, which you lose each time you fail to hit the ball.
# If you lose all four hearts, and then miss again, you lose.
#
# The game has four main states: StartScreen, Playing, Win and Lost.
# The program keeps track of all assets, internal variables, user inputs,
# and switches between states when appropriate
#
# Credits for Resources
# Sounds courtesy of https://freesound.org/
# Icons made by
# www.flaticon.com/authors/smashicons Smashicons
# www.flaticon.com/authors/vaadin Vaadin
# www.flaticon.com/authors/pixel-perfect Pixel perfect
# www.flaticon.com/authors/itim2101 itim2101

import pygame
import brick
import heart
import math
import ball
import player

# Initializes pygame as well as variables for keeping track of the games state
pygame.init()
started = False  # Keeps track of if the game has ever been started
playing = False  # Keeps track of if the player is currently playing
win = False  # Keeps track of if the player is currently in a winning state


# Functions for playing each of the games sound effects
#
# Sound for the ball hitting a wall
def s_tennis():
    tennis = pygame.mixer.Sound("Sounds/tennis.wav")
    pygame.mixer.Sound.play(tennis)


# Sound for ball hitting the paddle
def s_clang():
    clang = pygame.mixer.Sound("Sounds/clang.wav")
    pygame.mixer.Sound.play(clang)


# Sound for bricks breaking
def s_crumble():
    crumble = pygame.mixer.Sound("Sounds/crumble.wav")
    pygame.mixer.Sound.play(crumble)


# Sounds for when a life is lost
def s_hit():
    hit = pygame.mixer.Sound("Sounds/hit.wav")
    pygame.mixer.Sound.play(hit)


def s_fanfare():
    metal = pygame.mixer.Sound("Sounds/fanfare.wav")
    pygame.mixer.Sound.play(metal)


# Create the screen
screen = pygame.display.set_mode((1000, 800))

# Set the title and the games icon for the window
pygame.display.set_caption("Brick Smasher")
icon = pygame.image.load('Img/ball.png')
pygame.display.set_icon(icon)

# Initializes the player, an instance of the player class
thePlayer = player.Player()

# Loads the image to be used for the blocks and creates relevant arrays
blockImg = pygame.image.load('Img/lego-64.png')
blockList = []  # An array of blocks which will be displayed on screen
hbList = []  # An array of the corresponding hit boxes of the blocks in blockList

# Loads the image to be used in the lives counter
# Creates an array to keep track of how many lives the player has
heartImg = pygame.image.load('Img/heart.png')
heartList = []

# Initializes the ball, an instance of the Ball class
theBall = ball.Ball()

# Descriptions of the fonts and titles to be used in on the different menu screens
font = pygame.font.SysFont('Calibri', 50, bold=True)
result_font = pygame.font.SysFont('Calibri', 115, bold=True)

you_win = result_font.render('You Win!!', True, (190, 238, 98))
you_lose = result_font.render('You Lose!!', True, (255, 101, 95))
play_text = font.render('Hit the Space Bar to play!', True, (125, 120, 122), (190, 238, 98))

menu_rect = pygame.Rect(200, 350, 600, 100)


# Function to be called to display the start screen
def start_screen():
    pygame.draw.rect(screen, (190, 238, 98), menu_rect, border_radius=100)
    screen.blit(play_text, (238, 377))


# Function to be called to display the games win screen
def win_screen():
    pygame.draw.rect(screen, (190, 238, 98), menu_rect, border_radius=100)
    screen.blit(play_text, (238, 377))
    screen.blit(you_win, (260, 200))


#  Function to be called to display the games losing screen
def lose_screen():
    pygame.draw.rect(screen, (190, 238, 98), menu_rect, border_radius=100)
    screen.blit(play_text, (238, 377))
    screen.blit(you_lose, (260, 200))


# Function for dealing with the hearts counter
#
# Fills the heartList with 4 Heart objects, setting their position
def create_hearts():
    for i in range(4):
        heartList.append(heart.Heart(855+i*35, 760))


# Function for printing the hearts based on how many hearts have been lost
def print_hearts():
    for life in heartList:
        if not life.lost:
            screen.blit(heartImg, (life.xPos, life.yPos))


# Function for indicating a heart is lost
# When a heart is lost, an internal object value is set to true to indicate it
def lose_heart(b):
    if b.pvl[4] <= 4:
        for i in range(b.pvl[4]):
            heartList[i].lose()


# Resets the players hearts so none are lost
def reset_lives():
    for life in heartList:
        life.lost = False


# Creates 5 lines of 15 evenly spaced Block objects and adds them to blockList
# Also creates the corresponding list of hit boxes for all the hit boxes of each block
def create_blocks():
    for i in range(15):
        blockList.append(brick.Brick(5+i*66, 10))

    for i in range(15):
        blockList.append(brick.Brick(5+i*66, 76))

    for i in range(15):
        blockList.append(brick.Brick(5+i*66, 142))

    for i in range(15):
        blockList.append(brick.Brick(5+i*66, 208))

    for i in range(15):
        blockList.append(brick.Brick(5+i*66, 274))

    for b in blockList:
        hbList.append(b.hb)


# Resets the blocks so none are considered to be hit
def reset_blocks():
    for b in blockList:
        b.hit = False


# Goes through all of the block objects and draws them on the screen
# Checks if the blocks "hit" variable is true or false
# If the block's "hit" variable is True, the block is not printed
def print_blocks():
    game_over = False
    for block in blockList:
        if not block.hit:
            game_over = True
            screen.blit(blockImg, (block.xPos, block.yPos))
    return game_over


# Draws the player sprite based on the input x and y coordinate
def draw_player(x, y):
    screen.blit(thePlayer.playerImg, (x, y))


# Draws the ball sprite based on the input x and y coordinate
def ball(b):
    screen.blit(b.ballImg, (b.pvl[0], b.pvl[1]))


# Function which updates the balls position based on its current position
# velocity and depending on what objects it is interacting. It also facilitates
# lives being lost
#
# This function contains the majority of the games physics as it dictates how
# the ball bounces off different object.
def update_ball(b):

    # Creates a list of all of the Brick hitboxes which are currently
    # intersecting with the ball
    col = b.hb.collidelistall(hbList)

    # Checks to see if the ball has hit the paddle
    paddle_hit = thePlayer.hb.colliderect(b.hb)
    # Checks if the ball has hit the left or right side of the paddle
    # To checks this, if the ball has intersected with any of four points
    # located around the paddles side it will be set to true
    hit_left = (b.hb.collidepoint(thePlayer.hb.x, thePlayer.hb.y) or
                b.hb.collidepoint(thePlayer.hb.x, thePlayer.hb.y + 10) or
                b.hb.collidepoint(thePlayer.hb.x + 10, thePlayer.hb.y) or
                b.hb.collidepoint(thePlayer.hb.x, thePlayer.hb.y + 20))

    hit_right = (b.hb.collidepoint(thePlayer.hb.x + 128, thePlayer.hb.y) or
                 b.hb.collidepoint(thePlayer.hb.x + 128, thePlayer.hb.y + 10) or
                 b.hb.collidepoint(thePlayer.hb.x + 118, thePlayer.hb.y) or
                 b.hb.collidepoint(thePlayer.hb.x + 128, thePlayer.hb.y + 20))

    # Goes through the list of all of the hit boxes that are currently intersecting
    # with the ball. If they are not currently marke as hit, mark them as hit and play
    # relevant sound
    if col:
        for c in col:
            if not blockList[c].hit:
                blockList[c].got_hit()
                s_crumble()

    # Conditional statement which dictates how the ball will bounce of the paddle.
    # and also plays the proper sound effect
    #
    # If the ball hits the right side of the paddle, its velocity will be checked
    # If the ball is coming in from the right, the change in its angle will be proportional
    # to the angle at which it hit, the angle will change only a bit if it is close to a 45 degree angle
    # and it will change a lot the closer the velocity gets to directly vertical or horizontal
    # This is the same as what will happen if the left side is hit, coming from the left
    #
    # If the ball hits the right side of the paddle and is coming from the left, its angle will change
    # exactly ninety degrees. This is the same as what will happen if it hits the left side
    # coming from the right
    #
    # If the ball hits the middle of the paddle, its y velocity is simple flipped
    if hit_right and b.pvl[2] > 0:
        s_clang()
        theta = math.acos(abs(b.pvl[2]) / b.ballSpeed)
        delta = math.pi-theta
        b.pvl[2] = abs(math.cos(delta) * b.ballSpeed)
        b.pvl[3] = -math.sqrt(abs(b.ballSpeed**2 - b.pvl[2]**2))
    elif hit_right and b.pvl[2] < 0:
        s_clang()
        theta = math.acos(abs(b.pvl[2]) / b.ballSpeed)
        delta = (math.pi / 2) - theta
        b.pvl[2] = abs(math.cos(delta) * b.ballSpeed)
        b.pvl[3] = -math.sqrt(abs(b.ballSpeed**2 - b.pvl[2]**2))
    elif hit_left and b.pvl[2] > 0:
        s_clang()
        theta = math.acos(abs(b.pvl[2]) / b.ballSpeed)
        delta = (math.pi / 2) - theta
        b.pvl[2] = -abs(math.cos(delta) * b.ballSpeed)
        b.pvl[3] = -math.sqrt(abs(b.ballSpeed**2 - b.pvl[2]**2))
    elif hit_left and b.pvl[2] < 0:
        s_clang()
        theta = math.acos(abs(b.pvl[2]) / b.ballSpeed)
        delta = math.pi-theta
        b.pvl[2] = -abs(math.cos(delta) * b.ballSpeed)
        b.pvl[3] = -math.sqrt(abs(b.ballSpeed**2 - b.pvl[2]**2))
    elif paddle_hit:
        s_clang()
        b.pvl[3] = -b.pvl[3]

    # Checks for intersection with the walls of the game screen
    if b.pvl[0] + b.pvl[2] < 0 or b.pvl[0] + b.pvl[2] > 968:
        s_tennis()
        b.pvl[2] = -b.pvl[2]

    if b.pvl[1] + b.pvl[3] < 0:
        s_tennis()
        b.pvl[3] = -b.pvl[3]

    # If the ball goes below the bottom border of the screen
    # Play the appropriate sound effect
    # Lose a heart, and reset the position of the ball
    if b.pvl[1] + b.pvl[3] > 768:
        s_hit()
        b.pvl[4] += 1
        lose_heart(b)
        b.pvl[0] = b.ballX
        b.pvl[1] = b.ballY
        b.hb.x = b.pvl[0]
        b.hb.y = b.pvl[1]

    # Moves the ball's position based on the above conditionals
    b.pvl[0] += b.pvl[2]
    b.pvl[1] += b.pvl[3]
    b.hb.x = b.pvl[0]
    b.hb.y = b.pvl[1]
    return b


# Sets the game as running
running = True

# Creates list of blocks and hearts
create_blocks()
create_hearts()

# The main game loop
# Runs while "running" is true, and stops when the game is quite
# The main game loop is responsible for tracking all of the key strokes of the player
# Moving the paddle and keeping track of the games state
while running:
    screen.fill((238, 249, 252))

    # Checks if the players has quit the game
    # if not, check all of the in game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checks for keyboard input
        # If the current state of the game is "playing" then the keystroke control the paddle
        # Else, the keystrokes will only effect the game's menus
        if playing:
        # if a keystroke is pressed check whether it is right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    thePlayer.playerX_change = -thePlayer.playerSpeed
                if event.key == pygame.K_RIGHT:
                    thePlayer.playerX_change = thePlayer.playerSpeed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    thePlayer.playerX_change = 0
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = True
                    started = True
                    win = False

    # If the player is currently playing change the paddles location based on the above
    # Entered keystrokes
    if playing:
        thePlayer.playerX += thePlayer.playerX_change
        thePlayer.hb.centerx += thePlayer.playerX_change

        # Keeps the paddle from going out of bounds
        if thePlayer.playerX <= 0:
            thePlayer.playerX = 0
            thePlayer.hb.x = 0
        elif thePlayer.playerX >= (1000-128):
            thePlayer.playerX = (1000-128)
            thePlayer.hb.x = (1000 - 128)

        # Draws the paddle on the screen
        draw_player(thePlayer.playerX, thePlayer.playerY)

        # Checks if all blocks have been hit
        # If they have, switch to winning state and play fanfare
        # Display the winning screen
        # Reset the position of the ball, paddle
        # Reset all the blocks and the player's lives
        if not print_blocks():
            s_fanfare()
            playing = False
            win = True
            reset_blocks()
            reset_lives()
            theBall.pvl[0] = theBall.ballX
            theBall.pvl[1] = theBall.ballY
            theBall.hb.x = theBall.pvl[0]
            theBall.hb.y = theBall.pvl[1]
            thePlayer.playerX = (1000 - 128) / 2
            thePlayer.playerY = 645
            thePlayer.hb.x = (1000 - 128) / 2
            thePlayer.hb.y = 645-thePlayer.hbOffset
            theBall.pvl[4] = 0
            thePlayer.playerX_change = 0

        # Prints the hearts to the screen
        print_hearts()

        # Checks if all lives have been lost
        # If they haven't, update the balls position
        # Else switch to the losing game state
        # Play the appropriate sound effect and display the losing screen
        # Reset the position of the ball, paddle
        # Reset all the blocks and the player's lives
        if theBall.pvl[4] <= 4:
            ball(update_ball(theBall))
        else:
            s_hit()
            playing = False
            win = False
            reset_blocks()
            reset_lives()
            theBall.pvl[0] = theBall.ballX
            theBall.pvl[1] = theBall.ballY
            theBall.hb.x = theBall.pvl[0]
            theBall.hb.y = theBall.pvl[1]
            thePlayer.playerX = (1000 - 128) / 2
            thePlayer.playerY = 645
            thePlayer.hb.x = (1000 - 128) / 2
            thePlayer.hb.y = 645-thePlayer.hbOffset
            theBall.pvl[4] = 0
            thePlayer.playerX_change = 0

    # Display's the start screen if the player is not currently playing and has not started the game yet
    elif not started:
        start_screen()

    # Display's the win screen if the player is not currently playing and the player has won
    elif started and win:
        win_screen()

    # Display's the losing screen if the player is not currently playing and has lost the game
    elif started and not win:
        lose_screen()

    # Update the screen
    pygame.display.update()
    # Create set time delay to avoid random changes in balls velocity based on computer clock
    pygame.time.delay(5)