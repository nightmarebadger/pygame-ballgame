# coding=utf-8

"""

* File Name : main.py

* Created By : Natan Žabkar, natan.zabkar@gmail.com 

* Creation Date : 17-03-2012

* Last Modified : 18.3.2012 0:47:52

"""

from __future__ import division, print_function
import pygame, random, sys
from pygame.locals import *
from colors import *

# Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 650
WIDTHCHECK = WINDOWWIDTH
HEIGHTCHECK = WINDOWHEIGHT - 50
BACKGROUND = PURPLE
FPS = 120


# Functions
def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y, color):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, leftKey, rightKey):
        pygame.sprite.Sprite.__init__(self)
        self.image_left = pygame.image.load("sprite/ply1l.png")
        self.image_right = pygame.image.load("sprite/ply1r.png")
        self.image_normal = pygame.image.load("sprite/ply1n.png")
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.vx = 0
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.move = 0

    def update(self, time):
        if(self.vx < 0):
            self.image = self.image_left
        elif(self.vx > 0):
            self.image = self.image_right
        elif(self.vx == 0):
            self.image = self.image_normal

        self.move += self.speed * self.vx * time
        if(self.move > 1 or self.move < 1):
            # Check if out of bounds
            # Left
            if(self.rect.left + int(self.move) > 0):
                self.rect.move_ip(int(self.move), 0)
                self.move -= int(self.move)
            else:
                self.rect.move_ip(-self.rect.left, 0)
                self.move = 0
            if(self.rect.right + int(self.move) < WIDTHCHECK):
                self.rect.move_ip(int(self.move), 0)
                self.move -= int(self.move)
            else:
                self.rect.move_ip(WIDTHCHECK - self.rect.right, 0)
                self.move = 0 



# Pygame stuff setup
pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Ball game")
background = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
background.fill(PURPLE)
surface.blit(background, (0,0))
pygame.display.update()

# Fonts setup
font = pygame.font.SysFont(None, 12)

# Sprite groups
playerGroup = pygame.sprite.RenderPlain()

ply = Player(400, 300, 300, K_LEFT, K_RIGHT)
playerGroup.add(ply)

# Game loop
playing = True
while playing:
    time = clock.tick(FPS)
    for event in pygame.event.get():
        if(event.type == QUIT):
            terminate()
        if(event.type == KEYDOWN):
            if(event.key == K_ESCAPE):
                terminate()
            for ply in playerGroup:
                if(event.key == ply.leftKey):
                    ply.vx -= 1
                if(event.key == ply.rightKey):
                    ply.vx += 1
        if(event.type == KEYUP):
            for ply in playerGroup:
                if(event.key == ply.leftKey):
                    ply.vx += 1
                if(event.key == ply.rightKey):
                    ply.vx -= 1
    
    surface.fill(PURPLE)
    playerGroup.update(time/1000)
    playerGroup.draw(surface)
    pygame.display.update()

