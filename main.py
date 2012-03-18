# coding=utf-8

"""

* File Name : main.py

* Created By : Natan Žabkar, natan.zabkar@gmail.com 

* Creation Date : 17-03-2012

* Last Modified : 18.3.2012 14:29:38

"""

from __future__ import division, print_function
import pygame, random, sys
from pygame.locals import *
from colors import *

#dirty = True
dirty = False
count = 0

# Constants
WINDOWWIDTH = 800
WINDOWHEIGHT = 650
WIDTHCHECK = WINDOWWIDTH
HEIGHTCHECK = WINDOWHEIGHT - 50
FPS = 120
GRAVITATION = 100


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
    def __init__(self, x, y, speed, leftKey, rightKey, shootingKey):
        pygame.sprite.Sprite.__init__(self)
        self.image_left = pygame.image.load("images/player/ply1l.png")
        self.image_right = pygame.image.load("images/player/ply1r.png")
        self.image_normal = pygame.image.load("images/player/ply1n.png")
        self.image_shooting = pygame.image.load("images/player/ply1s.png")
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        self.speed = speed
        self.vx = 0
        self.leftKey = leftKey
        self.rightKey = rightKey
        self.shootingKey = shootingKey
        self.move = 0
        self.shooting = False
        self.arrow = None
        self.shooting_speed = 300

    def update(self, time):
        if(self.shooting):
            self.image = self.image_shooting
        elif(self.vx < 0):
            self.image = self.image_left
        elif(self.vx > 0):
            self.image = self.image_right
        elif(self.vx == 0):
            self.image = self.image_normal

        if(not self.shooting):
            self.move += self.speed * self.vx * time
            if(self.move > 1 or self.move < 1):
                # Check if out of bounds
                # Left
                if(self.rect.left + int(self.move) >= 0):
                    self.rect.move_ip(int(self.move), 0)
                    self.move -= int(self.move)
                else:
                    self.rect.left = 0
                    self.move = 0
                # Right
                if(self.rect.right + int(self.move) <= WIDTHCHECK):
                    self.rect.move_ip(int(self.move), 0)
                    self.move -= int(self.move)
                else:
                    self.rect.right = WIDTHCHECK
                    self.move = 0

        if(self.hitBalls(ballGroup)):
            terminate()
        if(self.shooting and self.arrow == None):
            self.shoot()
        if(not self.shooting and self.arrow != None):
            self.shoot_stop()

    def hitBalls(self, balls):
        for b in balls:
#            if self.rect.colliderect(b.rect):
            if(pygame.sprite.collide_mask(self, b)):
                return True
        return False

    def shoot(self):
        global arrowGroup
        self.arrow = Arrow(self, self.rect.centerx, self.rect.top, 5, self.shooting_speed, BLACK)
        arrowGroup.add(self.arrow)

    def shoot_stop(self):
        self.arrow.kill()
#        del self.arrow
        self.arrow = None

class Arrow(pygame.sprite.Sprite):

    def __init__(self, player, x, y, width, vy, color):
        pygame.sprite.Sprite.__init__(self)

        self.player = player
        self.x = x
        self.y = y
        self.image = pygame.Surface((width, 1))
        self.rect = self.image.get_rect()
        self.rect.midbottom = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.image, 0)
        self.mask.fill()
        self.vy = vy
        self.movey = 0

    def update(self, time):
        self.movey += time * self.vy
        if(self.rect.top - int(self.movey) < 0):
            self.player.shoot_stop()
        else:
            self.image = pygame.Surface((self.rect.width, self.rect.height + int(self.movey)))
            self.image.fill(BLACK)
            self.movey -= int(self.movey)
            self.rect = self.image.get_rect()
            self.rect.midbottom = (self.x, self.y)
            self.mask = pygame.mask.from_surface(self.image, 0)
            self.mask.fill()
            self.hitBalls(ballGroup)

    def hitBalls(self, balls):
        for b in balls:
#            if self.rect.colliderect(b.rect):
            if(pygame.sprite.collide_mask(self, b)):
                self.player.shoot_stop()
                b.split()
                return True
        return False

class Ball(pygame.sprite.Sprite):
    image_red = pygame.image.load("images/ball/red.png")
    image_green = pygame.image.load("images/ball/green.png")
    image_blue = pygame.image.load("images/ball/blue.png")

    def __init__(self, x, y, rad, vx, vy, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.vx = vx
        self.vy = vy
        self.movex = 0
        self.movey = 0
        self.rad = rad

        if(color == "red"):
            self.image = pygame.transform.scale(Ball.image_red, (2 * self.rad, 2 * self.rad))
        elif(color == "green"):
            self.image = pygame.transform.scale(Ball.image_green, (2 * self.rad, 2 * self.rad))
        elif(color == "blue"):
            self.image = pygame.transform.scale(Ball.image_blue, (2 * self.rad, 2 * self.rad))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, time):
        self.vy += time * GRAVITATION
        self.move(time * self.vx, time * self.vy)

    def move(self, x, y):
        self.movex += x
        self.movey += y

        self.rect.move_ip(int(self.movex), int(self.movey))
        self.movex -= int(self.movex)
        self.movey -= int(self.movey)
        # Bottom
        if(self.rect.bottom > HEIGHTCHECK):
            self.rect.bottom = HEIGHTCHECK
            self.movey = 0
            self.vy *= -1
        # Top
        if(self.rect.top < 0):
            self.rect.top = 0
            self.movey = 0
            self.vy *= -1
        # Left
        if(self.rect.left < 0):
            self.rect.left = 0
            self.movex = 0
            self.vx *= -1
        # Right
        if(self.rect.right > WIDTHCHECK):
            self.rect.right = WIDTHCHECK
            self.movex = 0
            self.vx *= -1

    def split(self):
        self.kill()

# Pygame stuff setup
pygame.init()
clock = pygame.time.Clock()
surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Ball game")
BACKGROUND = pygame.image.load("images/background/1.png").convert()
if(dirty):
    surface.blit(BACKGROUND, (0,0))
    pygame.display.update()

# Fonts setup
font = pygame.font.SysFont(None, 12)

# Sprite groups
if(dirty):
    playerGroup = pygame.sprite.RenderUpdates()
    ballGroup = pygame.sprite.RenderUpdates()
    arrowGroup = pygame.sprite.RenderUpdates()
else:
    playerGroup = pygame.sprite.RenderPlain()
    ballGroup = pygame.sprite.RenderPlain()
    arrowGroup = pygame.sprite.RenderPlain()



ply = Player(WINDOWWIDTH//2, WINDOWHEIGHT-50, 300, K_LEFT, K_RIGHT, K_SPACE)
playerGroup.add(ply)

color = ["red", "green", "blue"]
for i in range(1):
    r = random.randint(10,100)
    ball = Ball(random.randint(r, WIDTHCHECK-r), random.randint(r, HEIGHTCHECK-r), r, random.randint(-500, 500), random.randint(-500, 500), color[random.randint(0,2)])
    ballGroup.add(ball)

# Game loop
playing = True
while playing:
    time = clock.tick(FPS)
    count += time
    if(count >= 1000):
        print(clock.get_fps())
        count = 0
    for event in pygame.event.get():
        if(event.type == QUIT):
            terminate()
        elif(event.type == KEYDOWN):
            if(event.key == K_ESCAPE):
                terminate()
            for ply in playerGroup:
                if(event.key == ply.leftKey):
                    ply.vx -= 1
                elif(event.key == ply.rightKey):
                    ply.vx += 1
                elif(event.key == ply.shootingKey):
                    ply.shooting = True
        elif(event.type == KEYUP):
            for ply in playerGroup:
                if(event.key == ply.leftKey):
                    ply.vx += 1
                elif(event.key == ply.rightKey):
                    ply.vx -= 1
                elif(event.key == ply.shootingKey):
                    ply.shooting = False
    

    # Update all groups
    ballGroup.update(time/1000)
    playerGroup.update(time/1000)
    arrowGroup.update(time/1000)

    # Drawing
    
    if(dirty):
        rect1 = playerGroup.draw(surface)
        rect2 = ballGroup.draw(surface)
        rect3 = arrowGroup.draw(surface)

        pygame.display.update(rect1 + rect2 + rect3)
        playerGroup.clear(surface, BACKGROUND)
        ballGroup.clear(surface, BACKGROUND)
    else:
        surface.blit(BACKGROUND, (0, 0))
        playerGroup.draw(surface)
        ballGroup.draw(surface)
        arrowGroup.draw(surface)
        pygame.display.update()

