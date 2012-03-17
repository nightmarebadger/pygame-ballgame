# coding=utf-8

"""

* File Name : main.py

* Created By : Natan Žabkar, natan.zabkar@gmail.com 

* Creation Date : 17-03-2012

* Last Modified : 17.3.2012 23:44:50

"""

import pygame, random, sys
from pygame.locals import *
from colors import *

# Constants
WINDOWWIDTH = 600
WINDOWHEIGHT = 600
BACKGROUND = BLACK
FPS = 60


# Functions
def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


# Pygame stuff setup
pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Ball game")

# Fonts setup
font = pygame.font.SysFont(None, 12)


# Game loop
playing = True
while playing:
    for event in pygame.event.get():
        if(event.type == QUIT):
            terminate()
        if(event.type == KEYDOWN):
            if(event.key == K_ESCAPE):
                terminate()

    clock.tick(FPS)
